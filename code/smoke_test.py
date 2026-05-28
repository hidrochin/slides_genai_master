"""Numpy-only smoke test (no torch): validates data/meta-path/leakage logic."""
import numpy as np
from mpham.config import Config
from mpham.metapaths import build_H0, build_metapath_adjs, mask_test_edges
from mpham.data import gip_kernel, _topk_sparsify, _fuse
from mpham.data import sample_negatives

# tiny synthetic HIN
nR, nD, nP = 8, 10, 12
cfg = Config(n_drug=nR, n_dis=nD, n_prot=nP, sim_topk=3)
rng = np.random.default_rng(0)
A_rd = (rng.random((nR, nD)) < 0.3).astype(np.float32)
A_rp = (rng.random((nR, nP)) < 0.3).astype(np.float32)
A_pd = (rng.random((nP, nD)) < 0.3).astype(np.float32)
S_rr = _topk_sparsify(rng.random((nR, nR)).astype(np.float32), 3, 0)
S_dd = _topk_sparsify(rng.random((nD, nD)).astype(np.float32), 3, 0)
S_pp = _topk_sparsify(rng.random((nP, nP)).astype(np.float32), 3, 0)

N = nR + nD + nP
H0 = build_H0(A_rd, A_rp, A_pd, S_rr, S_dd, S_pp)
assert H0.shape == (N, N), H0.shape
# off-diagonal block equals A_rd
assert np.allclose(H0[:nR, nR:nR+nD], A_rd)

adjs = build_metapath_adjs(cfg, A_rd, A_rp, A_pd, S_rr, S_dd, S_pp)
assert set(adjs.keys()) == {1, 2, 3}
for k, lst in adjs.items():
    for name, A in lst:
        assert A.shape == (N, N)
        assert np.allclose(A, A.T), f"{name} not symmetric"
        assert np.all(np.diag(A) == 0)

# leakage check: masking test edges must remove them from H0 AND meta-paths
test_pairs = np.argwhere(A_rd > 0)[:3]
A_tr = mask_test_edges(A_rd, test_pairs)
assert A_tr[test_pairs[:, 0], test_pairs[:, 1]].sum() == 0
H0m = build_H0(A_tr, A_rp, A_pd, S_rr, S_dd, S_pp)
for (r, d) in test_pairs:
    assert H0m[r, nR + d] == 0 and H0m[nR + d, r] == 0
# RD meta-path adj must also lose the edge
adjs_m = build_metapath_adjs(cfg, A_tr, A_rp, A_pd, S_rr, S_dd, S_pp)
rd_adj = dict(adjs_m[1])["RD"]
for (r, d) in test_pairs:
    assert rd_adj[r, nR + d] == 0

# GIP kernel sanity
G = gip_kernel(A_rd)
assert G.shape == (nR, nR) and np.allclose(np.diag(G), 1.0, atol=1e-5)
assert G.min() >= 0 and G.max() <= 1.0 + 1e-5

# negative sampling never returns a positive
pos_set = set((np.argwhere(A_rd > 0)[:, 0] * nD + np.argwhere(A_rd > 0)[:, 1]).tolist())
neg = sample_negatives(pos_set, 20, nR, nD, rng)
for a, b in neg:
    assert (a * nD + b) not in pos_set

print("SMOKE TEST PASSED: shapes, symmetry, leakage masking, GIP, neg sampling all OK")
