"""
Proposal 5 — MoMoE-DR: Sparse Mixture-of-Mechanism-Experts.
Transfers M3oE / MoME / Switch-Transformer routing (RecSys/LLM) to DR.

  LightGCN propagation -> h ; per-node gate selects top-k of N experts (specialised MLPs)
  -> fused embedding -> RotatE decoder. Switch-style load-balancing loss removes the need
  for GCGB's custom gradient-balance optimiser (W8).

  NOTE: the full proposal routes per meta-path and shares experts across B/C/F. This single-file
  version implements the core sparse-MoE mechanism on one dataset; cross-dataset sharing is the
  natural extension (instantiate one MoMoE and feed B∪C∪F batches with a dataset-id in the gate).

Run:  python exp5_momoe_dr.py
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from common import (Config, load_data, FoldData, LightGCNEncoder, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise)


class Expert(nn.Module):
    def __init__(self, d, dropout):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, d), nn.ReLU(), nn.Dropout(dropout), nn.Linear(d, d))

    def forward(self, x):
        return self.net(x)


class MoMoE_DR(PairwiseDRModel):
    def __init__(self, cfg: Config, fold: FoldData, n_experts: int = 8, top_k: int = 2):
        super().__init__()
        self.cfg = cfg
        self.n_experts = n_experts
        self.top_k = top_k
        self.enc = LightGCNEncoder(cfg, fold.feat_dims)
        self.gate = nn.Linear(cfg.emb_dim, n_experts)
        self.experts = nn.ModuleList([Expert(cfg.emb_dim, cfg.dropout) for _ in range(n_experts)])
        self.dec = RotatEDecoder(cfg)
        self.alpha_lb = 1e-2
        self._lb = torch.tensor(0.0)

    def forward(self, fold: FoldData) -> torch.Tensor:
        h = self.enc(fold)                                  # (N, d)
        probs = F.softmax(self.gate(h), dim=-1)             # (N, E)
        topv, topi = probs.topk(self.top_k, dim=-1)         # (N, k)
        # sparse top-k gate as a dense (N,E) weight matrix (zeros outside top-k), renormalised
        gate_w = torch.zeros_like(probs).scatter(1, topi, topv)
        gate_w = gate_w / gate_w.sum(-1, keepdim=True).clamp_min(1e-9)

        # dense compute of all experts, combined by the sparse gate (fully differentiable, no in-place)
        expert_outs = torch.stack([e(h) for e in self.experts], dim=1)   # (N, E, d)
        out = (gate_w.unsqueeze(-1) * expert_outs).sum(1)                # (N, d)

        # Switch-style load-balance loss: E * Σ_e f_e · P_e
        with torch.no_grad():
            f_e = F.one_hot(topi.reshape(-1), self.n_experts).float().mean(0)   # routed fraction
        P_e = probs.mean(0)                                                     # mean gate prob
        self._lb = self.n_experts * (f_e * P_e).sum()
        return out

    def score(self, H, d_idx, s_idx) -> torch.Tensor:
        return self.dec(H[d_idx], H[self.cfg.n_drug + s_idx])

    def compute_loss(self, fold, H, pos, neg) -> torch.Tensor:
        base = super().compute_loss(fold, H, pos, neg)
        return base + self.alpha_lb * self._lb


def run(cfg: Config = None, n_experts: int = 8, top_k: int = 2):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    print(f"\n=== Proposal 5 — MoMoE-DR (experts={n_experts}, top_k={top_k}) ===")
    return run_cv_pairwise(cfg, data, lambda c, f: MoMoE_DR(c, f, n_experts=n_experts, top_k=top_k))


if __name__ == "__main__":
    run()
