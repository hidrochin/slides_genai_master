"""
Proposal 6 — NoiseDR: Ultra-cheap noise-perturbation contrastive + degree-aware temperature.
Transfers XSimGCL / SimGCL / Long-tail GCL (RecSys) to DR.

  Encoder -> H ; two noisy views h+Δ (Δ = sign(h)·U(0,ε)) ; InfoNCE between views
  with per-node temperature τ(deg)=τ0·(1+λ/log(deg+e))  (low-degree nodes -> sharper contrast)
  Loss = BCE + λ_cl · InfoNCE(drugs) + InfoNCE(diseases)

Run:  python exp6_noisedr.py
"""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from common import (Config, load_data, FoldData, LightGCNEncoder, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise)


class NoiseDR(PairwiseDRModel):
    def __init__(self, cfg: Config, fold: FoldData):
        super().__init__()
        self.cfg = cfg
        self.enc = LightGCNEncoder(cfg, fold.feat_dims)
        self.dec = RotatEDecoder(cfg)
        self.eps = 0.1
        self.tau0 = 0.2
        self.lam_deg = 0.5
        self.lam_cl = 0.1

    def forward(self, fold: FoldData) -> torch.Tensor:
        self._fold = fold
        return self.enc(fold)

    def score(self, H, d_idx, s_idx) -> torch.Tensor:
        return self.dec(H[d_idx], H[self.cfg.n_drug + s_idx])

    def _noise(self, H):
        delta = torch.sign(H) * torch.rand_like(H) * self.eps
        return H + delta

    def _info_nce_deg(self, z1, z2, deg):
        z1 = F.normalize(z1, dim=1); z2 = F.normalize(z2, dim=1)
        tau = self.tau0 * (1.0 + self.lam_deg / torch.log(deg + math.e))   # (n,)
        logits = (z1 @ z2.t()) / tau.unsqueeze(1)
        labels = torch.arange(z1.size(0), device=z1.device)
        return F.cross_entropy(logits, labels)

    def compute_loss(self, fold, H, pos, neg) -> torch.Tensor:
        base = super().compute_loss(fold, H, pos, neg)        # BCE on clean embeddings
        nR, nD = self.cfg.n_drug, self.cfg.n_dis
        v1, v2 = self._noise(H), self._noise(H)
        l_cl = (self._info_nce_deg(v1[:nR], v2[:nR], fold.drug_deg) +
                self._info_nce_deg(v1[nR:nR + nD], v2[nR:nR + nD], fold.dis_deg))
        return base + self.lam_cl * l_cl


def run(cfg: Config = None):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    print("\n=== Proposal 6 — NoiseDR ===")
    return run_cv_pairwise(cfg, data, NoiseDR)


if __name__ == "__main__":
    run()
