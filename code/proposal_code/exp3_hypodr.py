"""
Proposal 3 — HypoDR: Disentangled hyperbolic Mechanism-of-Action factors.
Transfers DHCF / GDCF / intent-disentangled GCL (RecSys) to DR.

  K mechanism channels, each a Poincaré ball 𝔻^{d/K}.
  Per channel: content -> tangent -> expmap0 -> tangent-space graph propagation (HGCN-lite).
  Pair score s = Σ_k ρ_k(d,s) · (− d_𝔻(h_d^k, h_s^k)) ;  ρ = softmax routing over channels (MoA attribution).
  Loss = BCE(a·s+b) + λ_disc·cross-channel-correlation.

Run:  python exp3_hypodr.py
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from common import Config, load_data, FoldData, ContentProjector, PairwiseDRModel, run_cv_pairwise

EPS = 1e-5


# --- Poincaré ball ops (curvature c>0) ---
def expmap0(v, c):
    vn = v.norm(dim=-1, keepdim=True).clamp_min(EPS)
    return torch.tanh((c ** 0.5) * vn) * v / ((c ** 0.5) * vn)


def logmap0(y, c):
    yn = y.norm(dim=-1, keepdim=True).clamp(EPS, 1.0 / (c ** 0.5) - EPS)
    return torch.atanh((c ** 0.5) * yn) * y / ((c ** 0.5) * yn)


def mobius_add(x, y, c):
    xy = (x * y).sum(-1, keepdim=True)
    x2 = (x * x).sum(-1, keepdim=True)
    y2 = (y * y).sum(-1, keepdim=True)
    num = (1 + 2 * c * xy + c * y2) * x + (1 - c * x2) * y
    den = 1 + 2 * c * xy + (c ** 2) * x2 * y2
    return num / den.clamp_min(EPS)


def hyp_dist(x, y, c):
    add = mobius_add(-x, y, c).norm(dim=-1).clamp(EPS, 1.0 / (c ** 0.5) - EPS)
    return (2.0 / (c ** 0.5)) * torch.atanh((c ** 0.5) * add)


class HypoDR(PairwiseDRModel):
    def __init__(self, cfg: Config, fold: FoldData, K: int = 4, layers: int = 2):
        super().__init__()
        self.cfg = cfg
        self.K = K
        self.layers = layers
        self.dk = cfg.emb_dim // K
        assert cfg.emb_dim % K == 0
        self.proj = ContentProjector(cfg, fold.feat_dims)
        self.c = nn.Parameter(torch.tensor(1.0))                 # learnable curvature
        self.route = nn.Sequential(nn.Linear(K, K), nn.Tanh(), nn.Linear(K, K))
        self.scale = nn.Parameter(torch.tensor(1.0))
        self.bias = nn.Parameter(torch.tensor(0.0))
        self.lam_disc = 1e-2

    def forward(self, fold: FoldData) -> torch.Tensor:
        c = self.c.clamp_min(0.1)
        X = self.proj(fold)                                      # (N, d)
        chans = X.split(self.dk, dim=-1)                         # K × (N, dk)
        out = []
        for xk in chans:
            h = expmap0(xk, c)                                   # to ball
            for _ in range(self.layers):                        # tangent-space propagation
                t = logmap0(h, c)
                t = torch.sparse.mm(fold.A_hat, t)
                h = expmap0(t, c)
            out.append(h)
        return torch.stack(out, 0)                               # (K, N, dk)

    def score(self, H, d_idx, s_idx) -> torch.Tensor:
        c = self.c.clamp_min(0.1)
        nR = self.cfg.n_drug
        dists = []
        for k in range(self.K):
            hd = H[k][d_idx]; hs = H[k][nR + s_idx]
            dists.append(hyp_dist(hd, hs, c))                    # (B,)
        D = torch.stack(dists, 1)                                # (B, K)
        rho = F.softmax(self.route(-D), dim=1)                   # MoA attribution
        s = (rho * (-D)).sum(1)
        return self.scale * s + self.bias

    def compute_loss(self, fold, H, pos, neg) -> torch.Tensor:
        base = super().compute_loss(fold, H, pos, neg)
        # disentanglement: penalise correlation between channel mean-embeddings (in tangent space)
        c = self.c.clamp_min(0.1)
        feats = torch.stack([logmap0(H[k], c).mean(0) for k in range(self.K)], 0)  # (K, dk)
        feats = F.normalize(feats, dim=1)
        corr = feats @ feats.t()
        off = corr - torch.eye(self.K, device=corr.device)
        return base + self.lam_disc * (off ** 2).sum()


def run(cfg: Config = None, K: int = 4):
    cfg = cfg or Config(epochs=200, gcn_layers=2, emb_dim=256)
    data = load_data(cfg)
    print(f"\n=== Proposal 3 — HypoDR (K={K} mechanism channels) ===")
    return run_cv_pairwise(cfg, data, lambda c, f: HypoDR(c, f, K=K))


if __name__ == "__main__":
    run()
