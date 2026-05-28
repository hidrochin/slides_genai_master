"""
MPHAM model.

Three-level hierarchical attention per node, faithful to eqs (2)-(14):

  node-level     (eq 3-6) : GAT over neighbours within one meta-path
  pattern-level  (eq 7-9) : attention over meta-paths of the SAME distance k
  distance-level (eq 10-12): attention over distances k

Implemented densely (N=1888, NxN ~14MB/path) for clarity; switch to sparse if
you scale to Hetero-A (N~7800).
"""
import torch
import torch.nn as nn
import torch.nn.functional as F


NEG_INF = -9e15


class MPHAMLayer(nn.Module):
    def __init__(self, in_dim, out_dim, n_distances, cfg):
        super().__init__()
        self.cfg = cfg
        # node-level (shared across meta-paths, eq.3 single W)
        self.node_W = nn.Linear(in_dim, out_dim, bias=False)
        self.a_src = nn.Parameter(torch.empty(out_dim))
        self.a_dst = nn.Parameter(torch.empty(out_dim))
        # pattern-level (eq.7) and distance-level (eq.10) transforms + contexts
        self.pat_lin = nn.Linear(out_dim, out_dim)
        self.u_a = nn.Parameter(torch.empty(out_dim))
        self.dist_lin = nn.Linear(out_dim, out_dim)
        self.u_b = nn.Parameter(torch.empty(out_dim))
        self.drop = nn.Dropout(cfg.dropout)
        self.norm = nn.LayerNorm(out_dim) if cfg.layernorm else nn.Identity()
        self.res_proj = (nn.Linear(in_dim, out_dim, bias=False)
                         if (cfg.residual and in_dim != out_dim) else None)
        self.reset_parameters()

    def reset_parameters(self):
        nn.init.xavier_uniform_(self.node_W.weight)  # eq: Xavier init
        nn.init.xavier_uniform_(self.pat_lin.weight)
        nn.init.xavier_uniform_(self.dist_lin.weight)
        for p in (self.a_src, self.a_dst, self.u_a, self.u_b):
            nn.init.normal_(p, std=0.1)
        if self.res_proj is not None:
            nn.init.xavier_uniform_(self.res_proj.weight)

    def _node_attention(self, Wh, adj):
        """GAT aggregation over one binary adjacency `adj` (N,N). Returns (N,d)."""
        if self.cfg.node_attn == "paper":          # literal eq.4: e_ij = a.Wh_j
            e_dst = Wh @ self.a_dst                  # (N,)
            scores = e_dst.unsqueeze(0).expand(adj.size(0), -1)
        else:                                        # standard GAT
            e_src = Wh @ self.a_src                  # (N,)
            e_dst = Wh @ self.a_dst                  # (N,)
            scores = e_src.unsqueeze(1) + e_dst.unsqueeze(0)
            scores = F.leaky_relu(scores, 0.2)
        scores = scores.masked_fill(adj == 0, NEG_INF)
        alpha = torch.softmax(scores, dim=1)
        # zero-out rows with no neighbours (softmax of all -inf -> nan)
        no_nb = (adj.sum(1, keepdim=True) == 0)
        alpha = torch.where(no_nb, torch.zeros_like(alpha), alpha)
        return alpha @ Wh

    def forward(self, H, adjs):
        Wh = F.relu(self.node_W(H))                  # eq.3
        Wh = self.drop(Wh)
        Hk_list = []
        for dist in sorted(adjs.keys()):
            Hkm = [self._node_attention(Wh, adj) for _, adj in adjs[dist]]
            # pattern-level attention (eq.7-9), per node, softmax over patterns
            U = [torch.tanh(self.pat_lin(h)) for h in Hkm]     # each (N,d)
            s = torch.stack([u @ self.u_a for u in U], dim=1)  # (N, M)
            beta = torch.softmax(s, dim=1)
            Hk = sum(beta[:, m:m + 1] * Hkm[m] for m in range(len(Hkm)))
            Hk_list.append(Hk)
        # distance-level attention (eq.10-12), softmax over distances
        Ud = [torch.tanh(self.dist_lin(h)) for h in Hk_list]
        sd = torch.stack([u @ self.u_b for u in Ud], dim=1)    # (N, K)
        gamma = torch.softmax(sd, dim=1)
        out = sum(gamma[:, k:k + 1] * Hk_list[k] for k in range(len(Hk_list)))
        # residual + norm (INFERRED; helps over-smoothing on the dense 11% graph)
        if self.cfg.residual:
            res = H if self.res_proj is None else self.res_proj(H)
            out = out + res
        out = self.norm(out)
        return out


class MPHAM(nn.Module):
    def __init__(self, cfg, in_dim, n_distances):
        super().__init__()
        self.cfg = cfg
        dims = [in_dim] + [cfg.emb_dim] * cfg.n_layers
        self.layers = nn.ModuleList([
            MPHAMLayer(dims[i], dims[i + 1], n_distances, cfg)
            for i in range(cfg.n_layers)
        ])
        # predictor (eq.14): concat drug & disease embeddings -> MLP -> logit
        self.predictor = nn.Sequential(
            nn.Linear(2 * cfg.emb_dim, cfg.predictor_hidden),
            nn.ReLU(),
            nn.Dropout(cfg.dropout),
            nn.Linear(cfg.predictor_hidden, 1),
        )

    def encode(self, H0, adjs):
        H = H0
        for layer in self.layers:
            H = layer(H, adjs)
        return H                                     # (N, d), eq.13 stacked

    def score(self, H, drug_idx, dis_idx):
        nR = self.cfg.n_drug
        hr = H[drug_idx]
        hd = H[nR + dis_idx]
        return self.predictor(torch.cat([hr, hd], dim=1)).squeeze(-1)  # logits
