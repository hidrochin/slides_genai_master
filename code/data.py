"""
B-dataset loader.

The csv previews you gave show a leading index column and a header row of
column indices, i.e. they were written with `DataFrame.to_csv(index=True)`.
`_read_matrix` strips that defensively and coerces to float. If your real files
differ, the asserts will tell you exactly where.

Matrices returned (all numpy float32):
    A_rd : (n_drug, n_dis)   drug-disease   (from adj.csv, the source of truth)
    A_rp : (n_drug, n_prot)  drug-protein
    A_pd : (n_prot, n_dis)   protein-disease
    S_rr : (n_drug, n_drug)  fused drug similarity
    S_dd : (n_dis,  n_dis)   fused disease similarity
    S_pp : (n_prot, n_prot)  fused protein similarity
"""
import os
import numpy as np
import pandas as pd

from .config import Config


def _read_matrix(path, expected_shape=None):
    """Read a (possibly index+header) numeric matrix and return a float array."""
    df = pd.read_csv(path, header=0, index_col=0)
    # drop any all-NaN first column/row leftovers
    arr = df.apply(pd.to_numeric, errors="coerce").to_numpy(dtype=np.float64)
    if np.isnan(arr).any():
        # a stray NaN in [0,0] is the classic to_csv artefact; fill with 0
        arr = np.nan_to_num(arr, nan=0.0)
    if expected_shape is not None:
        assert arr.shape == expected_shape, (
            f"{os.path.basename(path)}: got {arr.shape}, expected {expected_shape}. "
            f"Adjust header/index_col in _read_matrix.")
    return arr.astype(np.float32)

def _read_matrix(path, shape=None):
    df = pd.read_csv(path, header=0, index_col=0)          # label row + label col
    arr = df.apply(pd.to_numeric, errors="coerce").to_numpy(np.float64)
    arr = np.nan_to_num(arr, nan=0.0).astype(np.float32)
    if shape is not None:
        assert arr.shape == shape, f"{path}: got {arr.shape}, expected {shape}"
    return arr

def _topk_sparsify(S, k, thr):
    """Keep top-k off-diagonal neighbours per row above thr; zero the rest.
    Returns a symmetric (max) sparsified copy. Diagonal forced to 0."""
    S = S.copy()
    np.fill_diagonal(S, 0.0)
    if thr > 0:
        S[S <= thr] = 0.0
    if k and k > 0:
        n = S.shape[0]
        for i in range(n):
            row = S[i]
            if (row > 0).sum() > k:
                kth = np.partition(row, -k)[-k]
                row[row < kth] = 0.0
    S = np.maximum(S, S.T)  # symmetrise
    return S


def _fuse(sources, mode):
    sources = [s for s in sources if s is not None]
    if mode == "struct_only":
        return sources[0]
    if mode == "gip_only":
        return sources[-1]
    if mode == "gip_fill":
        base = sources[0].copy()
        gip = sources[-1]
        mask = base <= 0
        base[mask] = gip[mask]
        return base
    # "mean"
    return np.mean(np.stack(sources, 0), axis=0).astype(np.float32)


def gip_kernel(profiles):
    """Gaussian Interaction Profile kernel over rows of `profiles` (n, d_feat).
    gamma normalised by the mean squared norm of the profiles (Laarhoven 2011)."""
    sq = (profiles ** 2).sum(1)
    gamma = 1.0 / (sq.mean() + 1e-12)
    # ||pi-pj||^2 = sq_i + sq_j - 2 pi.pj
    G = sq[:, None] + sq[None, :] - 2.0 * profiles @ profiles.T
    np.clip(G, 0, None, out=G)
    return np.exp(-gamma * G).astype(np.float32)


class BDataset:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        d = cfg.data_dir
        nR, nD, nP = cfg.n_drug, cfg.n_dis, cfg.n_prot

        # ----- associations -----
        self.A_rd = _read_matrix(os.path.join(d, "adj.csv"), (nR, nD))
        self.A_rd = (self.A_rd > 0).astype(np.float32)

        rp = _read_pairs(os.path.join(d, "DrugProteinAssociationNumber.csv"), nR, nP)
        self.A_rp = np.zeros((nR, nP), np.float32)
        self.A_rp[rp[:, 0], rp[:, 1]] = 1.0

        # NOTE: file columns are (disease, protein)
        pd_ = _read_pairs(os.path.join(d, "ProteinDiseaseAssociationNumber.csv"), nD, nP)
        self.A_pd = np.zeros((nP, nD), np.float32)
        self.A_pd[pd_[:, 1], pd_[:, 0]] = 1.0

        # ----- raw similarity sources -----
        self._drug_struct = _read_matrix(os.path.join(d, "DrugFingerprint.csv"), (nR, nR))
        self._drug_gip = _read_matrix(os.path.join(d, "DrugGIP.csv"), (nR, nR))
        self._dis_struct = _read_matrix(os.path.join(d, "DiseasePS.csv"), (nD, nD))
        self._dis_gip = _read_matrix(os.path.join(d, "DiseaseGIP.csv"), (nD, nD))
        self._prot_seq = _read_matrix(os.path.join(d, "Protein_sequence.csv"), (nP, nP))
        gip_drug = _read_matrix(os.path.join(d, "ProteinGIP_Drug.csv"), (nP, nP))
        gip_dis = _read_matrix(os.path.join(d, "ProteinGIP_Disease.csv"), (nP, nP))
        self._prot_gip = ((gip_drug + gip_dis) / 2.0).astype(np.float32)

    # similarity built per-fold so GIP can be recomputed leak-free
    def build_similarities(self, A_rd_train):
        cfg = self.cfg
        if cfg.recompute_gip:
            # GIP from train-only drug-disease interaction profiles
            drug_gip = gip_kernel(A_rd_train)            # (nR,nR) from drug profiles
            dis_gip = gip_kernel(A_rd_train.T)           # (nD,nD) from disease profiles
        else:
            drug_gip, dis_gip = self._drug_gip, self._dis_gip
        S_rr = _fuse([self._drug_struct, drug_gip], cfg.sim_fusion)
        S_dd = _fuse([self._dis_struct, dis_gip], cfg.sim_fusion)
        S_pp = _fuse([self._prot_seq, self._prot_gip], cfg.sim_fusion)
        S_rr = _topk_sparsify(S_rr, cfg.sim_topk, cfg.sim_threshold)
        S_dd = _topk_sparsify(S_dd, cfg.sim_topk, cfg.sim_threshold)
        S_pp = _topk_sparsify(S_pp, cfg.sim_topk, cfg.sim_threshold)
        return S_rr, S_dd, S_pp

    @property
    def positives(self):
        r, c = np.where(self.A_rd > 0)
        return np.stack([r, c], 1)


def sample_negatives(pos_set, n_neg, nR, nD, rng, forbid=None):
    """Uniformly sample n_neg (drug,disease) pairs absent from pos_set and
    from `forbid`. pos_set/forbid are sets of flattened keys (r*nD + d)."""
    forbid = forbid or set()
    out = []
    while len(out) < n_neg:
        r = rng.integers(0, nR, size=n_neg)
        d = rng.integers(0, nD, size=n_neg)
        for a, b in zip(r, d):
            key = int(a) * nD + int(b)
            if key in pos_set or key in forbid:
                continue
            out.append((a, b))
            if len(out) >= n_neg:
                break
    return np.array(out, dtype=np.int64)
