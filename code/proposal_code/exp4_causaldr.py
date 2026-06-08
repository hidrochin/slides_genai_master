"""
Proposal 4 — CausalDR: Counterfactual debiasing of research-popularity.
Transfers PPAC / MACR / IPW (causal RecSys) to DR.

  Match path :  M = RotatE_decoder(h_d, h_s)        (the biology we want)
  Popularity :  P_d = g_d(log deg_d),  P_s = g_s(log deg_s)
  Train      :  Ŷ = σ(M + γ_d·P_d + γ_s·P_s), IPW-weighted BCE (down-weight hub edges)
  Deploy     :  debiased score = M   (popularity removed)  <-- this is what score() returns

Run:  python exp4_causaldr.py     (or import run() in the notebook)
"""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from common import (Config, load_data, FoldData, LightGCNEncoder, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise)


class CausalDR(PairwiseDRModel):
    def __init__(self, cfg: Config, fold: FoldData):
        super().__init__()
        self.cfg = cfg
        self.enc = LightGCNEncoder(cfg, fold.feat_dims)
        self.match = RotatEDecoder(cfg)
        self.pop_d = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
        self.pop_s = nn.Sequential(nn.Linear(1, 16), nn.ReLU(), nn.Linear(16, 1))
        self.gamma_d = nn.Parameter(torch.tensor(1.0))
        self.gamma_s = nn.Parameter(torch.tensor(1.0))
        self.eta = 1.0  # IPW exponent

    def forward(self, fold: FoldData) -> torch.Tensor:
        self._fold = fold
        return self.enc(fold)

    def score(self, H, d_idx, s_idx) -> torch.Tensor:
        """Debiased deploy score = match logit M only (popularity counterfactually removed)."""
        h_d = H[d_idx]
        h_s = H[self.cfg.n_drug + s_idx]
        return self.match(h_d, h_s)

    def compute_loss(self, fold, H, pos, neg) -> torch.Tensor:
        d = torch.cat([pos[:, 0], neg[:, 0]]); s = torch.cat([pos[:, 1], neg[:, 1]])
        y = torch.cat([torch.ones(len(pos)), torch.zeros(len(neg))]).to(H.device)

        M = self.score(H, d, s)
        log_deg_d = torch.log(fold.drug_deg[d]).unsqueeze(-1)
        log_deg_s = torch.log(fold.dis_deg[s]).unsqueeze(-1)
        P_d = self.pop_d(log_deg_d).squeeze(-1)
        P_s = self.pop_s(log_deg_s).squeeze(-1)
        logit = M + self.gamma_d * P_d + self.gamma_s * P_s    # biased training world

        # Inverse-propensity weights: down-weight high-degree (hub) drug edges
        w = (1.0 / fold.drug_deg[d]) ** self.eta
        w = w / w.mean()
        return F.binary_cross_entropy_with_logits(logit, y, weight=w)


def run(cfg: Config = None):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    print("\n=== Proposal 4 — CausalDR ===")
    return run_cv_pairwise(cfg, data, CausalDR)


if __name__ == "__main__":
    run()
