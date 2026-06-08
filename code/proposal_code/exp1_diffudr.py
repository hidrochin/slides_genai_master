"""
Proposal 1 — DiffuDR: Conditional diffusion as a generative DR engine.
Transfers DiffRec / DiffuRec (RecSys) to DR.

  Target  : each drug's disease-association ROW x0 ∈ {-1,1}^{nD}  (train-fold only) -> NO negative sampling.
  Condition: c_d = LightGCN(masked graph + SMILES/ESM/MeSH content) drug embedding.
  Denoiser: MLP over the disease axis, FiLM-conditioned on (c_d, t).
  Train   : predict the added noise (MSE).  Infer: reverse DDIM from noise -> score row per drug.

Custom CV loop (row-based), but reuses common.load_data / folds / masking / metrics.

Run:  python exp1_diffudr.py
"""
import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, average_precision_score
from common import (Config, load_data, FoldData, LightGCNEncoder, set_seed,
                    make_folds, split_train_val, sample_negatives)


def cosine_abar(T, s=0.008, device="cpu"):
    steps = torch.arange(T + 1, dtype=torch.float32)
    f = torch.cos(((steps / T + s) / (1 + s)) * math.pi / 2) ** 2
    abar = (f / f[0])[1:]            # length T, abar[t] for t=0..T-1
    return abar.to(device)


def timestep_embedding(t, dim):
    half = dim // 2
    freqs = torch.exp(-math.log(10000) * torch.arange(half, device=t.device) / half)
    args = t.float().unsqueeze(-1) * freqs.unsqueeze(0)
    return torch.cat([torch.cos(args), torch.sin(args)], dim=-1)


class Denoiser(nn.Module):
    def __init__(self, n_dis, d, hidden=512, t_dim=128):
        super().__init__()
        self.in_proj = nn.Linear(n_dis, hidden)
        self.c_proj = nn.Linear(d, hidden)
        self.t_proj = nn.Sequential(nn.Linear(t_dim, hidden), nn.SiLU(), nn.Linear(hidden, hidden))
        self.blocks = nn.ModuleList([nn.Sequential(nn.Linear(hidden, hidden), nn.SiLU()) for _ in range(3)])
        self.out = nn.Linear(hidden, n_dis)
        self.t_dim = t_dim

    def forward(self, x_t, t, c):
        h = self.in_proj(x_t) + self.c_proj(c) + self.t_proj(timestep_embedding(t, self.t_dim))
        for blk in self.blocks:
            h = h + blk(h)
        return self.out(h)


class DiffuDR(nn.Module):
    def __init__(self, cfg, fold, T=1000):
        super().__init__()
        self.cfg = cfg
        self.T = T
        self.enc = LightGCNEncoder(cfg, fold.feat_dims)        # condition encoder
        self.denoiser = Denoiser(cfg.n_dis, cfg.emb_dim)
        self.abar = cosine_abar(T, device=cfg.device)

    def condition(self, fold):
        return self.enc(fold)[:self.cfg.n_drug]                # (nR, d)

    def train_loss(self, fold, x0):
        c = self.condition(fold)                               # (nR, d)
        nR = x0.shape[0]
        t = torch.randint(0, self.T, (nR,), device=x0.device)
        ab = self.abar[t].unsqueeze(-1)
        eps = torch.randn_like(x0)
        x_t = ab.sqrt() * x0 + (1 - ab).sqrt() * eps
        eps_hat = self.denoiser(x_t, t, c)
        return F.mse_loss(eps_hat, eps)

    @torch.no_grad()
    def sample(self, fold, steps=50):
        c = self.condition(fold)
        nR, nD = self.cfg.n_drug, self.cfg.n_dis
        x = torch.randn(nR, nD, device=c.device)
        ts = torch.linspace(self.T - 1, 0, steps, device=c.device).long()
        x0 = x
        for i, t in enumerate(ts):
            t_prev = ts[i + 1] if i + 1 < len(ts) else torch.tensor(0, device=c.device)
            a_t = self.abar[t]; a_prev = self.abar[t_prev]
            eps = self.denoiser(x, t.expand(nR), c)
            x0 = ((x - (1 - a_t).sqrt() * eps) / a_t.sqrt()).clamp(-1, 1)
            x = a_prev.sqrt() * x0 + (1 - a_prev).sqrt() * eps
        return x0.cpu().numpy()                                # (nR, nD) score matrix


def _eval_matrix(Shat, test_pos, pos_set, cfg, rng):
    pos_sc = Shat[test_pos[:, 0], test_pos[:, 1]]
    neg1 = sample_negatives(pos_set, len(test_pos), cfg.n_drug, cfg.n_dis, rng)
    neg5 = sample_negatives(pos_set, len(test_pos) * cfg.test_neg_ratio_imbalanced, cfg.n_drug, cfg.n_dis, rng)
    s1 = Shat[neg1[:, 0], neg1[:, 1]]; s5 = Shat[neg5[:, 0], neg5[:, 1]]
    y1 = np.r_[np.ones(len(test_pos)), np.zeros(len(neg1))]
    y5 = np.r_[np.ones(len(test_pos)), np.zeros(len(neg5))]
    return {"auroc": roc_auc_score(y1, np.r_[pos_sc, s1]),
            "aupr": average_precision_score(y1, np.r_[pos_sc, s1]),
            "aupr_1to5": average_precision_score(y5, np.r_[pos_sc, s5])}


def run(cfg: Config = None, val_every=20, infer_steps=30):
    cfg = cfg or Config(epochs=300, gcn_layers=2)
    data = load_data(cfg); set_seed(cfg.seed)
    pos = data.positives
    pos_set = set((pos[:, 0] * cfg.n_dis + pos[:, 1]).tolist())
    folds = make_folds(len(pos), cfg.n_folds, cfg.seed)
    print("\n=== Proposal 1 — DiffuDR ===")
    rows = []
    for f in range(cfg.n_folds):
        te = folds[f]; tr = np.concatenate([folds[g] for g in range(cfg.n_folds) if g != f])
        test_pos = pos[te]
        train_pos, val_pos = split_train_val(pos[tr], cfg.val_frac, cfg.seed + f)
        fold = FoldData(cfg, data, test_pos)

        model = DiffuDR(cfg, fold).to(cfg.device)
        opt = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)
        x0 = (2 * fold.A_rd_t - 1)                              # {-1,1}, test edges already masked

        best_val, best_state = -1, None
        for ep in range(cfg.epochs):
            model.train(); opt.zero_grad()
            loss = model.train_loss(fold, x0)
            loss.backward(); opt.step()
            if (ep + 1) % val_every == 0 or ep == cfg.epochs - 1:
                Shat = model.sample(fold, steps=infer_steps)
                vm = _eval_matrix(Shat, val_pos, pos_set, cfg, np.random.default_rng(cfg.seed))
                if vm["auroc"] > best_val:
                    best_val = vm["auroc"]
                    best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

        model.load_state_dict(best_state)
        Shat = model.sample(fold, steps=max(50, infer_steps))
        tm = _eval_matrix(Shat, test_pos, pos_set, cfg, np.random.default_rng(cfg.seed + 999))
        rows.append(tm)
        print(f"  fold{f}: AUROC={tm['auroc']:.4f} AUPR={tm['aupr']:.4f} AUPR(1:5)={tm['aupr_1to5']:.4f} "
              f"(best val AUROC={best_val:.4f})")

    out = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
    out.update({k + "_std": float(np.std([r[k] for r in rows])) for k in rows[0]})
    print(f"  MEAN  AUROC={out['auroc']:.4f}±{out['auroc_std']:.4f}  AUPR={out['aupr']:.4f}  AUPR(1:5)={out['aupr_1to5']:.4f}")
    return out


if __name__ == "__main__":
    run()
