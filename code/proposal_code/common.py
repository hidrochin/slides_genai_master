"""
common.py — Shared foundation for all DR proposals (Proposals 1–9).

Honors the project's hard rules:
  * Strict per-fold masking of test drug–disease edges from every graph/feature.
  * Honest val-based model selection (10% of train positives held out as val).
  * Reports balanced (1:1) AND imbalanced (1:5) metrics.
  * GIP matrices are NEVER used (leaky under CV).
  * Drug content comes from SMILES (RDKit ECFP), NOT the degenerate Drug_mol2vec.csv (see ../experiments/README.md §0.5).

Data layout expected on Colab (after cloning DRMGNE and having the GCGB folder):
  DRMGNE/data/B-dataset/  -> adj.csv, DrugProteinAssociationNumber.csv, ProteinDiseaseAssociationNumber.csv,
                             DrugFingerprint.csv, DiseasePS.csv, Protein_sequence.csv, DrugInformation.csv
  GCGB/data/B-dataset/    -> DiseaseFeature.csv (MeSH), Protein_ESM.csv (ESM-2)

Public API used by every exp*.py:
  Config, load_data, make_folds, split_train_val, sample_negatives,
  build_fold (-> FoldData), metrics, evaluate_pairwise,
  ContentProjector, LightGCNEncoder, RotatEDecoder,
  run_cv_pairwise  (generic trainer for pairwise-scoring models, Props 3/4/5/6 + DiffuDR conditioner)
"""

import os
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, average_precision_score

# ----------------------------------------------------------------------------- #
# Constants (B-dataset). Override in Config for C/F.
# ----------------------------------------------------------------------------- #
N_DRUG, N_DIS, N_PROT = 269, 598, 1021


@dataclass
class Config:
    # paths (Colab-friendly; load_data also searches a few candidate roots)
    drmgne_dir: str = "DRMGNE/data/B-dataset"
    gcgb_dir: str = "GCGB/data/B-dataset"
    # dims
    n_drug: int = N_DRUG
    n_dis: int = N_DIS
    n_prot: int = N_PROT
    emb_dim: int = 256
    # features
    drug_feat: str = "ecfp"          # 'ecfp' (RDKit from SMILES) | 'fingerprint' (DrugFingerprint.csv fallback)
    ecfp_bits: int = 2048
    ecfp_radius: int = 2
    sim_topk: int = 10               # top-k similarity edges per row in the propagation graph
    # training
    lr: float = 1e-3
    weight_decay: float = 5e-4
    dropout: float = 0.2
    epochs: int = 200
    neg_ratio: int = 1
    n_folds: int = 5
    val_frac: float = 0.1
    grad_clip: float = 5.0
    gcn_layers: int = 2
    seed: int = 42
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    # eval
    test_neg_ratio_imbalanced: int = 5

    @property
    def n_nodes(self) -> int:
        return self.n_drug + self.n_dis + self.n_prot


# ----------------------------------------------------------------------------- #
# Low-level CSV readers (reused/adapted from mpham_core.py — proven on this data)
# ----------------------------------------------------------------------------- #
def _find(path_candidates: List[str]) -> str:
    for p in path_candidates:
        if os.path.exists(p):
            return p
    raise FileNotFoundError(f"None of these exist: {path_candidates}")


def _read_matrix(path: str, shape=None) -> np.ndarray:
    df = pd.read_csv(path, header=0, index_col=0)
    arr = np.nan_to_num(df.apply(pd.to_numeric, errors="coerce").to_numpy(np.float64), nan=0.0).astype(np.float32)
    if shape:
        assert arr.shape == shape, f"{path}: {arr.shape} != {shape}"
    return arr


def _read_pairs(path: str, m0: int, m1: int) -> np.ndarray:
    p = pd.read_csv(path, header=0).to_numpy(np.int64)
    if p.min() >= 1:
        p = p - 1
    # orient so column 0 indexes the size-m0 entity
    if p[:, 0].max() >= m0 and p[:, 1].max() < m0:
        p = p[:, [1, 0]]
    return p


def _read_content(path: str) -> np.ndarray:
    """Read a content-feature CSV with no header and a label/index in column 0."""
    df = pd.read_csv(path, header=None)
    return df.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").fillna(0.0).to_numpy(np.float32)


# ----------------------------------------------------------------------------- #
# Drug content: SMILES -> ECFP (preferred) with graceful fallback
# ----------------------------------------------------------------------------- #
def smiles_to_ecfp(smiles_list: List[str], n_bits: int, radius: int) -> Optional[np.ndarray]:
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except Exception:
        print("[common] RDKit not available -> falling back to DrugFingerprint.csv rows for drug features.")
        return None
    feats = np.zeros((len(smiles_list), n_bits), np.float32)
    n_fail = 0
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
        if mol is None:
            n_fail += 1
            continue
        fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
        feats[i] = np.frombuffer(fp.ToBitString().encode(), "u1") - ord("0")
    if n_fail:
        print(f"[common] ECFP: {n_fail}/{len(smiles_list)} SMILES failed to parse (left as zero rows).")
    # sanity: ECFP must be non-degenerate (guards against silently bad features)
    n_unique = len(np.unique(feats, axis=0))
    assert n_unique > 0.5 * len(smiles_list), f"ECFP degenerate: only {n_unique} unique rows"
    return feats


def _impute_zero_rows(feat: np.ndarray, sim: np.ndarray, k: int = 10) -> np.ndarray:
    """Fill all-zero feature rows with the mean of their top-k similar rows (by `sim`)."""
    feat = feat.copy()
    zero_rows = np.where(~feat.any(axis=1))[0]
    if len(zero_rows) == 0:
        return feat
    for i in zero_rows:
        order = np.argsort(-sim[i])
        nbrs = [j for j in order if j != i and feat[j].any()][:k]
        if nbrs:
            feat[i] = feat[nbrs].mean(0)
    print(f"[common] imputed {len(zero_rows)} all-zero content rows via top-{k} similarity neighbours.")
    return feat


# ----------------------------------------------------------------------------- #
# Data container
# ----------------------------------------------------------------------------- #
class Data:
    """Holds all fold-independent arrays/tensors. Per-fold masking happens in build_fold()."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        d = _abs_dir(cfg.drmgne_dir)
        g = _abs_dir(cfg.gcgb_dir)
        nR, nD, nP = cfg.n_drug, cfg.n_dis, cfg.n_prot

        # --- associations ---
        self.A_rd = (_read_matrix(_find([os.path.join(d, "adj.csv"), os.path.join(g, "adj.csv")]), (nR, nD)) > 0).astype(np.float32)
        rp = _read_pairs(os.path.join(d, "DrugProteinAssociationNumber.csv"), nR, nP)
        self.A_rp = np.zeros((nR, nP), np.float32); self.A_rp[rp[:, 0], rp[:, 1]] = 1.0
        pdp = _read_pairs(os.path.join(d, "ProteinDiseaseAssociationNumber.csv"), nD, nP)
        self.A_pd = np.zeros((nP, nD), np.float32); self.A_pd[pdp[:, 1], pdp[:, 0]] = 1.0

        # --- content-derived similarities (NO GIP -> leakage-safe, fold-independent) ---
        self.S_rr = _read_matrix(os.path.join(d, "DrugFingerprint.csv"), (nR, nR))
        self.S_dd = _read_matrix(os.path.join(d, "DiseasePS.csv"), (nD, nD))
        self.S_pp = _read_matrix(os.path.join(d, "Protein_sequence.csv"), (nP, nP))

        # --- node content features ---
        info = pd.read_csv(os.path.join(d, "DrugInformation.csv"))
        smiles = info["smiles"].tolist() if "smiles" in info.columns else info.iloc[:, -1].tolist()
        ecfp = smiles_to_ecfp(smiles, cfg.ecfp_bits, cfg.ecfp_radius) if cfg.drug_feat == "ecfp" else None
        self.X_drug = ecfp if ecfp is not None else self.S_rr.copy()   # fallback: fingerprint-similarity rows

        mesh_path = os.path.join(g, "DiseaseFeature.csv")
        esm_path = os.path.join(g, "Protein_ESM.csv")
        if os.path.exists(mesh_path):
            self.X_dis = _impute_zero_rows(_read_content(mesh_path), self.S_dd, k=cfg.sim_topk)  # (598,64)
        else:
            print("[common] DiseaseFeature.csv (MeSH) not found -> falling back to DiseasePS rows as disease features.")
            self.X_dis = self.S_dd.copy()
        if os.path.exists(esm_path):
            self.X_prot = _read_content(esm_path)                       # (1021, 320), clean
        else:
            print("[common] Protein_ESM.csv not found -> falling back to Protein_sequence rows as protein features.")
            self.X_prot = self.S_pp.copy()

        assert self.X_drug.shape[0] == nR and self.X_dis.shape[0] == nD and self.X_prot.shape[0] == nP

        # positives + degrees (degrees recomputed per-fold inside build_fold from masked A_rd)
        r, c = np.where(self.A_rd > 0)
        self.positives = np.stack([r, c], 1)
        print(f"[common] loaded B-dataset: {nR} drugs, {nD} diseases, {nP} proteins, "
              f"{len(self.positives)} positive DDAs | drug_feat dim={self.X_drug.shape[1]}")


def _abs_dir(p: str) -> str:
    """Resolve a data dir against a few candidate roots (cwd, /content, parent)."""
    cands = [p, os.path.join("/content", p), os.path.join("..", p), os.path.join(os.getcwd(), p)]
    for c in cands:
        if os.path.isdir(c):
            return c
    return p  # let downstream _find raise a precise error


def load_data(cfg: Config) -> Data:
    set_seed(cfg.seed)
    return Data(cfg)


# ----------------------------------------------------------------------------- #
# Folds, splits, negative sampling, masking
# ----------------------------------------------------------------------------- #
def set_seed(seed: int):
    np.random.seed(seed); torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def make_folds(n_pos: int, n_folds: int, seed: int) -> List[np.ndarray]:
    rng = np.random.default_rng(seed)
    perm = rng.permutation(n_pos)
    return np.array_split(perm, n_folds)


def split_train_val(train_pos: np.ndarray, val_frac: float, seed: int):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(train_pos))
    n_val = max(1, int(val_frac * len(train_pos)))
    return train_pos[idx[n_val:]], train_pos[idx[:n_val]]


def sample_negatives(pos_set: set, n_neg: int, nR: int, nD: int, rng: np.random.Generator, forbid: set = None) -> np.ndarray:
    forbid = forbid or set()
    out = []
    while len(out) < n_neg:
        r = rng.integers(0, nR, n_neg); d = rng.integers(0, nD, n_neg)
        for a, b in zip(r, d):
            k = int(a) * nD + int(b)
            if k in pos_set or k in forbid:
                continue
            out.append((a, b))
            if len(out) >= n_neg:
                break
    return np.array(out, np.int64)


def _topk_sparsify(S: np.ndarray, k: int) -> np.ndarray:
    S = S.copy(); np.fill_diagonal(S, 0.0)
    if k and k > 0:
        for i in range(S.shape[0]):
            row = S[i]
            if (row > 0).sum() > k:
                kth = np.partition(row, -k)[-k]
                row[row < kth] = 0.0
    return np.maximum(S, S.T)


# ----------------------------------------------------------------------------- #
# FoldData: everything a model might need for ONE fold (test edges masked)
# ----------------------------------------------------------------------------- #
class FoldData:
    def __init__(self, cfg: Config, data: Data, test_pos: np.ndarray):
        self.cfg = cfg
        dev = cfg.device
        nR, nD, nP, N = cfg.n_drug, cfg.n_dis, cfg.n_prot, cfg.n_nodes

        # mask test drug-disease edges
        A_rd = data.A_rd.copy()
        A_rd[test_pos[:, 0], test_pos[:, 1]] = 0.0
        self.A_rd_np = A_rd

        # degrees from the MASKED train graph (popularity proxy for CausalDR)
        self.drug_deg = torch.tensor(A_rd.sum(1) + 1.0, dtype=torch.float32, device=dev)
        self.dis_deg = torch.tensor(A_rd.sum(0) + 1.0, dtype=torch.float32, device=dev)

        # normalized propagation adjacency  A_hat (N x N), sparse, symmetric + self loops
        self.A_hat = _build_norm_adj(cfg, A_rd, data.A_rp, data.A_pd, data.S_rr, data.S_dd, data.S_pp).to(dev)

        # content features as tensors
        self.X_drug = torch.tensor(data.X_drug, device=dev)
        self.X_dis = torch.tensor(data.X_dis, device=dev)
        self.X_prot = torch.tensor(data.X_prot, device=dev)

        # masked drug-disease row matrix (for DiffuDR row reconstruction)
        self.A_rd_t = torch.tensor(A_rd, device=dev)

        # k-NN similarity boolean graphs (for contrastive supervision)
        self.S_rr_knn = torch.tensor((_topk_sparsify(data.S_rr, cfg.sim_topk) > 0).astype(np.float32), device=dev)
        self.S_dd_knn = torch.tensor((_topk_sparsify(data.S_dd, cfg.sim_topk) > 0).astype(np.float32), device=dev)

        self.feat_dims = (data.X_drug.shape[1], data.X_dis.shape[1], data.X_prot.shape[1])


def _build_norm_adj(cfg, A_rd, A_rp, A_pd, S_rr, S_dd, S_pp) -> torch.Tensor:
    """Symmetric normalized sparse adjacency over [drugs|diseases|proteins]."""
    nR, nD, nP, N = cfg.n_drug, cfg.n_dis, cfg.n_prot, cfg.n_nodes
    oR, oD, oP = 0, nR, nR + nD
    rows, cols = [], []

    def add_block(M, ro, co, topk=0):
        Mb = _topk_sparsify(M, topk) if topk else M
        r, c = np.where(Mb > 0)
        rows.extend((r + ro).tolist() + (c + co).tolist())   # symmetric
        cols.extend((c + co).tolist() + (r + ro).tolist())

    add_block(A_rd, oR, oD)                 # drug-disease (masked)
    add_block(A_rp, oR, oP)                 # drug-protein
    add_block(A_pd.T, oD, oP)               # disease-protein  (A_pd is P x D)
    add_block(S_rr, oR, oR, topk=cfg.sim_topk)
    add_block(S_dd, oD, oD, topk=cfg.sim_topk)
    add_block(S_pp, oP, oP, topk=cfg.sim_topk)

    idx = torch.tensor([rows, cols], dtype=torch.long)
    val = torch.ones(idx.shape[1])
    A = torch.sparse_coo_tensor(idx, val, (N, N)).coalesce()
    # add self loops
    eye = torch.sparse_coo_tensor(torch.arange(N).repeat(2, 1), torch.ones(N), (N, N))
    A = (A + eye).coalesce()
    # symmetric normalization D^-1/2 A D^-1/2
    deg = torch.sparse.sum(A, dim=1).to_dense()
    dinv = torch.pow(deg.clamp(min=1), -0.5)
    i = A.indices(); v = A.values() * dinv[i[0]] * dinv[i[1]]
    return torch.sparse_coo_tensor(i, v, (N, N)).coalesce()


# ----------------------------------------------------------------------------- #
# Reusable nn.Modules
# ----------------------------------------------------------------------------- #
class ContentProjector(nn.Module):
    """Project heterogeneous content (drug/dis/prot) into a shared d-dim node matrix X (N x d)."""
    def __init__(self, cfg: Config, feat_dims):
        super().__init__()
        fR, fD, fP = feat_dims
        d = cfg.emb_dim
        self.lin_r = nn.Sequential(nn.Linear(fR, d), nn.ReLU(), nn.Dropout(cfg.dropout))
        self.lin_d = nn.Sequential(nn.Linear(fD, d), nn.ReLU(), nn.Dropout(cfg.dropout))
        self.lin_p = nn.Sequential(nn.Linear(fP, d), nn.ReLU(), nn.Dropout(cfg.dropout))

    def forward(self, fold: FoldData) -> torch.Tensor:
        xr = self.lin_r(fold.X_drug); xd = self.lin_d(fold.X_dis); xp = self.lin_p(fold.X_prot)
        return torch.cat([xr, xd, xp], dim=0)   # (N, d)


class LightGCNEncoder(nn.Module):
    """LightGCN-style propagation: no transform inside layers, mean of layer outputs."""
    def __init__(self, cfg: Config, feat_dims):
        super().__init__()
        self.cfg = cfg
        self.proj = ContentProjector(cfg, feat_dims)
        self.n_layers = cfg.gcn_layers

    def forward(self, fold: FoldData) -> torch.Tensor:
        x = self.proj(fold)                  # (N, d)
        outs = [x]
        for _ in range(self.n_layers):
            x = torch.sparse.mm(fold.A_hat, x)
            outs.append(x)
        return torch.stack(outs, 0).mean(0)  # (N, d)


def rotate_operator(a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
    a_re, a_im = a.chunk(2, dim=-1)
    b_re, b_im = b.chunk(2, dim=-1)
    return torch.cat([a_re * b_re - a_im * b_im, a_re * b_im + a_im * b_re], dim=-1)


class RotatEDecoder(nn.Module):
    """4-way decoder: [h_d || h_s || h_d*h_s || rotate(h_d,h_s)] -> MLP -> logit. emb_dim must be even."""
    def __init__(self, cfg: Config):
        super().__init__()
        d = cfg.emb_dim
        self.mlp = nn.Sequential(
            nn.Linear(4 * d, cfg.emb_dim // 2), nn.ReLU(), nn.Dropout(cfg.dropout),
            nn.Linear(cfg.emb_dim // 2, 1))

    def forward(self, h_d: torch.Tensor, h_s: torch.Tensor) -> torch.Tensor:
        x = torch.cat([h_d, h_s, h_d * h_s, rotate_operator(h_d, h_s)], dim=-1)
        return self.mlp(x).squeeze(-1)


# ----------------------------------------------------------------------------- #
# Metrics + evaluation
# ----------------------------------------------------------------------------- #
def metrics(y_true: np.ndarray, y_score: np.ndarray) -> Dict[str, float]:
    return {"auroc": roc_auc_score(y_true, y_score), "aupr": average_precision_score(y_true, y_score)}


@torch.no_grad()
def evaluate_pairwise(model, fold: FoldData, test_pos: np.ndarray, cfg: Config, rng: np.random.Generator,
                      pos_set: set) -> Dict[str, float]:
    """Standard eval: balanced (1:1) AUROC/AUPR + imbalanced (1:5) AUPR."""
    model.eval()
    H = model(fold)
    nR, nD = cfg.n_drug, cfg.n_dis

    def score(pairs):
        d = torch.tensor(pairs[:, 0], device=cfg.device); s = torch.tensor(pairs[:, 1], device=cfg.device)
        return torch.sigmoid(model.score(H, d, s)).cpu().numpy()

    neg1 = sample_negatives(pos_set, len(test_pos) * 1, nR, nD, rng)
    neg5 = sample_negatives(pos_set, len(test_pos) * cfg.test_neg_ratio_imbalanced, nR, nD, rng)
    pos_sc = score(test_pos)
    m1 = metrics(np.r_[np.ones(len(test_pos)), np.zeros(len(neg1))], np.r_[pos_sc, score(neg1)])
    aupr5 = average_precision_score(np.r_[np.ones(len(test_pos)), np.zeros(len(neg5))], np.r_[pos_sc, score(neg5)])
    return {"auroc": m1["auroc"], "aupr": m1["aupr"], "aupr_1to5": aupr5}


# ----------------------------------------------------------------------------- #
# Generic trainer for pairwise-scoring models (Props 3/4/5/6 + DiffuDR conditioner)
# ----------------------------------------------------------------------------- #
class PairwiseDRModel(nn.Module):
    """Base class. Subclasses implement forward(fold)->H and score(H, d_idx, s_idx)->logits.
       Override compute_loss to add auxiliary losses (contrastive, load-balance, causal, ...)."""
    def forward(self, fold: FoldData) -> torch.Tensor:
        raise NotImplementedError

    def score(self, H, d_idx, s_idx) -> torch.Tensor:
        raise NotImplementedError

    def compute_loss(self, fold, H, pos, neg) -> torch.Tensor:
        d = torch.cat([pos[:, 0], neg[:, 0]]); s = torch.cat([pos[:, 1], neg[:, 1]])
        y = torch.cat([torch.ones(len(pos)), torch.zeros(len(neg))]).to(H.device)
        logits = self.score(H, d, s)
        return F.binary_cross_entropy_with_logits(logits, y)


def run_cv_pairwise(cfg: Config, data: Data, build_model: Callable[[Config, FoldData], PairwiseDRModel],
                    verbose: bool = True) -> Dict[str, float]:
    """5-fold CV with strict masking + honest val-based selection. Returns mean/std of test metrics."""
    set_seed(cfg.seed)
    pos = data.positives
    pos_set = set((pos[:, 0] * cfg.n_dis + pos[:, 1]).tolist())
    folds = make_folds(len(pos), cfg.n_folds, cfg.seed)
    rng = np.random.default_rng(cfg.seed)
    rows = []

    for f in range(cfg.n_folds):
        te_idx = folds[f]
        tr_idx = np.concatenate([folds[g] for g in range(cfg.n_folds) if g != f])
        test_pos = pos[te_idx]
        train_pos_all = pos[tr_idx]
        train_pos, val_pos = split_train_val(train_pos_all, cfg.val_frac, cfg.seed + f)

        fold = FoldData(cfg, data, test_pos)
        model = build_model(cfg, fold).to(cfg.device)
        opt = torch.optim.Adam(model.parameters(), lr=cfg.lr, weight_decay=cfg.weight_decay)

        tp = torch.tensor(train_pos, device=cfg.device)
        best_val, best_state = -1.0, None
        for ep in range(cfg.epochs):
            model.train()
            neg = sample_negatives(pos_set, len(train_pos) * cfg.neg_ratio, cfg.n_drug, cfg.n_dis, rng)
            ntp = torch.tensor(neg, device=cfg.device)
            opt.zero_grad()
            H = model(fold)
            loss = model.compute_loss(fold, H, tp, ntp)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), cfg.grad_clip)
            opt.step()

            # honest selection: val AUROC
            val_m = evaluate_pairwise(model, fold, val_pos, cfg, np.random.default_rng(cfg.seed), pos_set)
            if val_m["auroc"] > best_val:
                best_val = val_m["auroc"]
                best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}

        model.load_state_dict(best_state)
        test_m = evaluate_pairwise(model, fold, test_pos, cfg, np.random.default_rng(cfg.seed + 999), pos_set)
        rows.append(test_m)
        if verbose:
            print(f"  fold{f}: AUROC={test_m['auroc']:.4f} AUPR={test_m['aupr']:.4f} "
                  f"AUPR(1:5)={test_m['aupr_1to5']:.4f}  (best val AUROC={best_val:.4f})")

    out = {k: float(np.mean([r[k] for r in rows])) for k in rows[0]}
    out.update({k + "_std": float(np.std([r[k] for r in rows])) for k in rows[0]})
    print(f"  MEAN  AUROC={out['auroc']:.4f}±{out['auroc_std']:.4f}  "
          f"AUPR={out['aupr']:.4f}±{out['aupr_std']:.4f}  AUPR(1:5)={out['aupr_1to5']:.4f}")
    return out
