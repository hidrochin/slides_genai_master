"""
Builds (a) the H0 block feature matrix and (b) one NxN adjacency per meta-path,
grouped by distance. All numpy; train.py moves them to torch tensors.

Block order in the 1888-d node space:  [ drugs | diseases | proteins ].
"""
import numpy as np
from .config import Config


def _slices(cfg: Config):
    nR, nD, nP = cfg.n_drug, cfg.n_dis, cfg.n_prot
    return slice(0, nR), slice(nR, nR + nD), slice(nR + nD, nR + nD + nP)


def build_H0(A_rd, A_rp, A_pd, S_rr, S_dd, S_pp):
    """Eq.(1): block matrix of similarities (diag) and associations (off-diag)."""
    nR, nD, nP = A_rd.shape[0], A_rd.shape[1], A_rp.shape[1]
    N = nR + nD + nP
    H0 = np.zeros((N, N), np.float32)
    r, d, p = slice(0, nR), slice(nR, nR + nD), slice(nR + nD, N)
    H0[r, r] = S_rr;            H0[r, d] = A_rd;      H0[r, p] = A_rp
    H0[d, r] = A_rd.T;          H0[d, d] = S_dd;      H0[d, p] = A_pd.T
    H0[p, r] = A_rp.T;          H0[p, d] = A_pd;      H0[p, p] = S_pp
    return H0


def _base_blocks(A_rd, A_rp, A_pd, S_rr, S_dd, S_pp):
    """Edge-type -> matrix lookup used to compose meta-paths."""
    return {
        "RR": S_rr, "DD": S_dd, "PP": S_pp,
        "RD": A_rd, "DR": A_rd.T,
        "RP": A_rp, "PR": A_rp.T,
        "PD": A_pd, "DP": A_pd.T,
    }


def _metapath_commuting(path, blocks):
    """Multiply consecutive edge blocks. 'RPD' -> RP @ PD  (drug x disease)."""
    mats = []
    for a, b in zip(path[:-1], path[1:]):
        mats.append(blocks[a + b])
    M = mats[0]
    for m in mats[1:]:
        M = M @ m
    return M  # shape: (count[path[0]], count[path[-1]])


def build_metapath_adjs(cfg, A_rd, A_rp, A_pd, S_rr, S_dd, S_pp):
    """Return {distance: [(name, NxN float adjacency), ...]}.

    Each meta-path commuting matrix is placed into the full NxN node space at
    the (start-type, end-type) block and symmetrised. Optionally binarised.
    Row-normalised so non-attention variants stay numerically stable.
    """
    nR, nD, nP = cfg.n_drug, cfg.n_dis, cfg.n_prot
    N = nR + nD + nP
    off = {"R": 0, "D": nR, "P": nR + nD}
    cnt = {"R": nR, "D": nD, "P": nP}
    blocks = _base_blocks(A_rd, A_rp, A_pd, S_rr, S_dd, S_pp)

    out = {}
    for dist, names in cfg.metapaths.items():
        if dist > cfg.max_distance:
            continue
        lst = []
        for name in names:
            M = _metapath_commuting(name, blocks)
            s_type, e_type = name[0], name[-1]
            A = np.zeros((N, N), np.float32)
            rs = slice(off[s_type], off[s_type] + cnt[s_type])
            cs = slice(off[e_type], off[e_type] + cnt[e_type])
            A[rs, cs] = M
            A = np.maximum(A, A.T)  # undirected
            if cfg.binarize_adj:
                A = (A > 0).astype(np.float32)
            else:
                deg = A.sum(1, keepdims=True)
                deg[deg == 0] = 1.0
                A = A / deg
            np.fill_diagonal(A, 0.0)
            lst.append((name, A))
        out[dist] = lst
    return out


def mask_test_edges(A_rd, test_pairs):
    """Remove test drug-disease positives so they leak into NEITHER H0 NOR any
    meta-path that traverses a drug-disease edge (RD, RDR, RPD, RPDR, RDPD...).
    This is THE leakage control. Returns a copy."""
    A = A_rd.copy()
    A[test_pairs[:, 0], test_pairs[:, 1]] = 0.0
    return A
