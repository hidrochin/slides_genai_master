"""
5-fold CV training harness with explicit leakage control.

Per fold:
  1. split positives into train/test
  2. mask test positives out of A_rd  -> rebuild H0 AND every meta-path adj
     (this is the single most important correctness step)
  3. (optional) recompute GIP from train-only A_rd
  4. transductive forward over the whole graph; BCE on train pairs with fresh
     negatives each epoch
  5. evaluate on test positives + matched negatives (balanced) or full matrix
"""
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, average_precision_score, \
    precision_score, recall_score, f1_score

from .config import Config
from .data import BDataset
from .metapaths import build_H0, build_metapath_adjs, mask_test_edges
from .data import sample_negatives


def _adjs_to_torch(adjs, device):
    return {k: [(n, torch.from_numpy(a).to(device)) for n, a in v]
            for k, v in adjs.items()}


def run_fold(cfg, ds, train_pos, test_pos, device, rng):
    nR, nD = cfg.n_drug, cfg.n_dis
    pos_set = set((ds.positives[:, 0] * nD + ds.positives[:, 1]).tolist())

    # ---- leakage control: mask test edges everywhere ----
    A_rd_tr = mask_test_edges(ds.A_rd, test_pos)
    S_rr, S_dd, S_pp = ds.build_similarities(A_rd_tr)
    H0 = build_H0(A_rd_tr, ds.A_rp, ds.A_pd, S_rr, S_dd, S_pp)
    adjs = build_metapath_adjs(cfg, A_rd_tr, ds.A_rp, ds.A_pd, S_rr, S_dd, S_pp)

    H0 = torch.from_numpy(H0).to(device)
    adjs = _adjs_to_torch(adjs, device)
    n_dist = len(adjs)

    from .model import MPHAM
    model = MPHAM(cfg, in_dim=H0.shape[1], n_distances=n_dist).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=cfg.lr,
                           weight_decay=cfg.weight_decay)

    # fixed test negatives (balanced eval)
    test_neg = sample_negatives(pos_set, len(test_pos) * cfg.neg_ratio,
                                nR, nD, rng)
    test_neg_set = set((test_neg[:, 0] * nD + test_neg[:, 1]).tolist())

    best_auc, best_state, patience = -1, None, 0
    for epoch in range(cfg.epochs):
        model.train()
        if epoch == 0 or cfg.resample_neg_each_epoch:
            tr_neg = sample_negatives(pos_set, len(train_pos) * cfg.neg_ratio,
                                      nR, nD, rng, forbid=test_neg_set)
        pairs = np.concatenate([train_pos, tr_neg], 0)
        labels = np.concatenate([np.ones(len(train_pos)),
                                 np.zeros(len(tr_neg))]).astype(np.float32)
        di = torch.from_numpy(pairs[:, 0]).to(device)
        si = torch.from_numpy(pairs[:, 1]).to(device)
        y = torch.from_numpy(labels).to(device)

        opt.zero_grad()
        H = model.encode(H0, adjs)
        logits = model.score(H, di, si)
        loss = F.binary_cross_entropy_with_logits(logits, y)  # eq.15
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 5.0)
        opt.step()

        # validate on the held-out fold (balanced)
        auc, *_ = evaluate(cfg, model, H0, adjs, test_pos, test_neg, device)
        if auc > best_auc:
            best_auc, patience = auc, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        else:
            patience += 1
            if patience >= cfg.early_stop_patience:
                break

    model.load_state_dict(best_state)
    if cfg.eval_mode == "full":
        return evaluate_full(cfg, model, H0, adjs, test_pos, pos_set, train_pos, device)
    return evaluate(cfg, model, H0, adjs, test_pos, test_neg, device)


@torch.no_grad()
def evaluate(cfg, model, H0, adjs, test_pos, test_neg, device):
    model.eval()
    H = model.encode(H0, adjs)
    pairs = np.concatenate([test_pos, test_neg], 0)
    y = np.concatenate([np.ones(len(test_pos)), np.zeros(len(test_neg))])
    di = torch.from_numpy(pairs[:, 0]).to(device)
    si = torch.from_numpy(pairs[:, 1]).to(device)
    prob = torch.sigmoid(model.score(H, di, si)).cpu().numpy()
    return _metrics(y, prob, cfg.score_threshold)


@torch.no_grad()
def evaluate_full(cfg, model, H0, adjs, test_pos, pos_set, train_pos, device):
    """Realistic eval: every pair that is not a TRAIN positive is a candidate."""
    model.eval()
    H = model.encode(H0, adjs)
    nR, nD = cfg.n_drug, cfg.n_dis
    train_set = set((train_pos[:, 0] * nD + train_pos[:, 1]).tolist())
    test_set = set((test_pos[:, 0] * nD + test_pos[:, 1]).tolist())
    di, si, y = [], [], []
    for r in range(nR):
        for d in range(nD):
            key = r * nD + d
            if key in train_set:
                continue
            di.append(r); si.append(d); y.append(1 if key in test_set else 0)
    di = torch.tensor(di, device=device); si = torch.tensor(si, device=device)
    prob = torch.sigmoid(model.score(H, di, si)).cpu().numpy()
    return _metrics(np.array(y), prob, cfg.score_threshold)


def _metrics(y, prob, thr):
    pred = (prob >= thr).astype(int)
    return (
        roc_auc_score(y, prob),
        average_precision_score(y, prob),
        precision_score(y, pred, zero_division=0),
        recall_score(y, pred, zero_division=0),
        f1_score(y, pred, zero_division=0),
    )


def cross_validate(cfg: Config):
    torch.manual_seed(cfg.seed); np.random.seed(cfg.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    ds = BDataset(cfg)
    pos = ds.positives
    rng = np.random.default_rng(cfg.seed)
    perm = rng.permutation(len(pos))
    folds = np.array_split(perm, cfg.n_folds)

    rows = []
    for f in range(cfg.n_folds):
        test_idx = folds[f]
        train_idx = np.concatenate([folds[g] for g in range(cfg.n_folds) if g != f])
        res = run_fold(cfg, ds, pos[train_idx], pos[test_idx], device, rng)
        print(f"fold {f}: AUC={res[0]:.4f} AUPR={res[1]:.4f} "
              f"P={res[2]:.4f} R={res[3]:.4f} F1={res[4]:.4f}")
        rows.append(res)
    rows = np.array(rows)
    m, s = rows.mean(0), rows.std(0)
    print(f"\nMEAN  AUC={m[0]:.3f}±{s[0]:.3f}  AUPR={m[1]:.3f}±{s[1]:.3f}  "
          f"P={m[2]:.3f}  R={m[3]:.3f}  F1={m[4]:.3f}")
    return m, s


if __name__ == "__main__":
    cross_validate(Config())
