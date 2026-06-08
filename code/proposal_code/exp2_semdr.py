"""
Proposal 2 — SemDR: Semantic-ID generative retrieval (TIGER for biology).
Transfers TIGER / RQ-VAE semantic IDs (RecSys) to DR.

  Stage A (offline, content-based, leakage-free): RQ-VAE turns drug content (SMILES->ECFP) and
          disease content (MeSH) into 3-token semantic IDs.
  Stage B (per fold): a small encoder-decoder Transformer maps drug SID -> disease SID, trained on
          train-fold pairs only. A (drug,disease) pair is SCORED by the teacher-forced log-likelihood
          of the disease SID given the drug SID -> gives AUROC/AUPR.

Custom CV loop. RQ-VAE is trained ONCE (content is fold-independent); the Transformer is retrained per fold.

Run:  python exp2_semdr.py
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, average_precision_score
from common import Config, load_data, set_seed, make_folds, split_train_val, sample_negatives


# ----------------------------- RQ-VAE tokenizer ----------------------------- #
class RQVAE(nn.Module):
    def __init__(self, in_dim, d=256, n_levels=3, codebook=256, beta=0.25):
        super().__init__()
        self.n_levels = n_levels; self.beta = beta
        self.enc = nn.Sequential(nn.Linear(in_dim, 512), nn.ReLU(), nn.Linear(512, d))
        self.dec = nn.Sequential(nn.Linear(d, 512), nn.ReLU(), nn.Linear(512, in_dim))
        self.codebooks = nn.ParameterList([nn.Parameter(torch.randn(codebook, d) * 0.1) for _ in range(n_levels)])

    def quantize(self, z):
        residual = z; q_total = 0.0; ids = []; commit = 0.0
        for cb in self.codebooks:
            d2 = torch.cdist(residual, cb)            # (B, K)
            idx = d2.argmin(1)
            q = cb[idx]
            commit = commit + F.mse_loss(residual.detach(), q) + self.beta * F.mse_loss(residual, q.detach())
            q_total = q_total + (residual + (q - residual).detach())   # straight-through
            residual = residual - q
            ids.append(idx)
        return q_total, torch.stack(ids, 1), commit

    def forward(self, x):
        z = self.enc(x)
        q, ids, commit = self.quantize(z)
        recon = F.mse_loss(self.dec(q), x)
        return recon + commit, ids

    @torch.no_grad()
    def encode_ids(self, x):
        return self.quantize(self.enc(x))[1]         # (B, n_levels) semantic ids


def train_rqvae(x, cfg, epochs=300, d=256, codebook=256):
    model = RQVAE(x.shape[1], d=d, codebook=codebook).to(cfg.device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    xt = x if torch.is_tensor(x) else torch.tensor(x, device=cfg.device)
    for _ in range(epochs):
        model.train(); opt.zero_grad()
        loss, _ = model(xt); loss.backward(); opt.step()
    model.eval()
    return model.quantize(model.enc(xt))[1].cpu().numpy()    # (B, 3) semantic ids


# ----------------------------- generative model ----------------------------- #
class SemTransformer(nn.Module):
    """Drug SID (3 tok) -> Disease SID (3 tok), encoder-decoder. Single token vocab with offsets."""
    def __init__(self, n_levels=3, codebook=256, d_model=128, nhead=4, layers=2, dropout=0.1):
        super().__init__()
        self.n_levels = n_levels; self.codebook = codebook
        self.base_drug = 0
        self.base_dis = n_levels * codebook
        self.BOS = 2 * n_levels * codebook
        self.EOS = self.BOS + 1
        vocab = self.EOS + 1
        self.vocab = vocab
        self.emb = nn.Embedding(vocab, d_model)
        self.pos = nn.Parameter(torch.randn(16, d_model) * 0.02)
        self.tr = nn.Transformer(d_model, nhead, layers, layers, dim_feedforward=4 * d_model,
                                 dropout=dropout, batch_first=True)
        self.head = nn.Linear(d_model, vocab)

    def drug_tokens(self, ids):      # ids: (B,3) codes -> token ids
        offs = torch.arange(self.n_levels, device=ids.device) * self.codebook + self.base_drug
        return ids + offs

    def dis_tokens(self, ids):
        offs = torch.arange(self.n_levels, device=ids.device) * self.codebook + self.base_dis
        return ids + offs

    def _embed(self, tok):
        return self.emb(tok) + self.pos[:tok.size(1)].unsqueeze(0)

    def forward(self, drug_ids, dis_ids):
        """Return per-step logits for teacher-forced disease tokens. dec_in=[BOS,d0,d1,d2]."""
        B = drug_ids.size(0)
        src = self._embed(self.drug_tokens(drug_ids))
        dis_tok = self.dis_tokens(dis_ids)                           # (B,3)
        bos = torch.full((B, 1), self.BOS, device=drug_ids.device)
        dec_in = torch.cat([bos, dis_tok], 1)                        # (B,4)
        tgt = self._embed(dec_in)
        mask = nn.Transformer.generate_square_subsequent_mask(dec_in.size(1)).to(drug_ids.device)
        out = self.tr(src, tgt, tgt_mask=mask)
        logits = self.head(out)                                      # (B,4,vocab)
        return logits[:, :self.n_levels, :], dis_tok                 # predict positions 0..2 -> d0,d1,d2

    def pair_loglik(self, drug_ids, dis_ids):
        logits, dis_tok = self.forward(drug_ids, dis_ids)
        logp = F.log_softmax(logits, dim=-1)
        ll = logp.gather(-1, dis_tok.unsqueeze(-1)).squeeze(-1).sum(1)   # (B,) sum over 3 levels
        return ll


def _metrics(pos_sc, neg_sc):
    y = np.r_[np.ones(len(pos_sc)), np.zeros(len(neg_sc))]
    s = np.r_[pos_sc, neg_sc]
    return roc_auc_score(y, s), average_precision_score(y, s)


def run(cfg: Config = None, tr_epochs=150):
    cfg = cfg or Config()
    data = load_data(cfg); set_seed(cfg.seed)
    dev = cfg.device

    # Stage A — RQ-VAE semantic IDs (content-based, fold-independent, leakage-free)
    print("\n=== Proposal 2 — SemDR ===\n[stageA] training RQ-VAE tokenizers (drug ECFP, disease MeSH)...")
    drug_ids = torch.tensor(train_rqvae(torch.tensor(data.X_drug, device=dev), cfg), device=dev)   # (nR,3)
    dis_ids = torch.tensor(train_rqvae(torch.tensor(data.X_dis, device=dev), cfg), device=dev)     # (nD,3)
    print(f"[stageA] unique drug SIDs: {len(set(map(tuple, drug_ids.tolist())))}/{cfg.n_drug} | "
          f"unique disease SIDs: {len(set(map(tuple, dis_ids.tolist())))}/{cfg.n_dis}")

    pos = data.positives
    pos_set = set((pos[:, 0] * cfg.n_dis + pos[:, 1]).tolist())
    folds = make_folds(len(pos), cfg.n_folds, cfg.seed)
    rng = np.random.default_rng(cfg.seed)
    rows = []

    for f in range(cfg.n_folds):
        te = folds[f]; tr = np.concatenate([folds[g] for g in range(cfg.n_folds) if g != f])
        test_pos = pos[te]
        train_pos, val_pos = split_train_val(pos[tr], cfg.val_frac, cfg.seed + f)

        model = SemTransformer().to(dev)
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        tp = torch.tensor(train_pos, device=dev)

        def score(pairs):
            with torch.no_grad():
                model.eval()
                d = drug_ids[torch.tensor(pairs[:, 0], device=dev)]
                s = dis_ids[torch.tensor(pairs[:, 1], device=dev)]
                return model.pair_loglik(d, s).cpu().numpy()

        best_val, best_state = -1, None
        for ep in range(tr_epochs):
            model.train(); opt.zero_grad()
            d = drug_ids[tp[:, 0]]; s = dis_ids[tp[:, 1]]
            ll = model.pair_loglik(d, s)
            loss = -ll.mean()                              # maximise likelihood of true pairs
            loss.backward(); opt.step()
            if (ep + 1) % 20 == 0 or ep == tr_epochs - 1:
                vneg = sample_negatives(pos_set, len(val_pos), cfg.n_drug, cfg.n_dis, rng)
                auc, _ = _metrics(score(val_pos), score(vneg))
                if auc > best_val:
                    best_val = auc
                    best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

        model.load_state_dict(best_state)
        neg1 = sample_negatives(pos_set, len(test_pos), cfg.n_drug, cfg.n_dis, rng)
        neg5 = sample_negatives(pos_set, len(test_pos) * cfg.test_neg_ratio_imbalanced, cfg.n_drug, cfg.n_dis, rng)
        pos_sc = score(test_pos)
        auc, aupr = _metrics(pos_sc, score(neg1))
        _, aupr5 = _metrics(pos_sc, score(neg5))
        rows.append({"auroc": auc, "aupr": aupr, "aupr_1to5": aupr5})
        print(f"  fold{f}: AUROC={auc:.4f} AUPR={aupr:.4f} AUPR(1:5)={aupr5:.4f} (best val AUROC={best_val:.4f})")

    out = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
    out.update({k + "_std": float(np.std([r[k] for r in rows])) for k in rows[0]})
    print(f"  MEAN  AUROC={out['auroc']:.4f}±{out['auroc_std']:.4f}  AUPR={out['aupr']:.4f}  AUPR(1:5)={out['aupr_1to5']:.4f}")
    print("  NOTE: SemDR's strength is cold-start/inductive retrieval, not pairwise AUROC. "
          "For the report, also evaluate Recall@k on held-out drugs.")
    return out


if __name__ == "__main__":
    run()
