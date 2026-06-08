"""
Proposal 7 — M³-DR (SCAFFOLD): Tri-modal drug + bi-modal protein via Modality-MoE.
Transfers MAMEX / FREEDOM / BM3 (multi-modal recommendation) + MolMix (bio).

STATUS:
  * 1D drug (ECFP from SMILES) + 2D drug (RDKit molecular graph, dense message passing) -> FULLY RUNNABLE if RDKit installed.
  * 3D drug (RDKit ETKDG conformer)  -> module provided, marked OPTIONAL (set use_3d=True).
  * protein 3D (AlphaFold)           -> TODO: see fetch_alphafold_pdb in exp9; not wired here.
  * Modality-MoE fusion              -> implemented.
The disease/protein sides reuse common's content (MeSH/ESM). Drug node features are the fused modalities.

Run:  python exp7_m3dr_scaffold.py     (needs `pip install rdkit`)
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd, os
from common import (Config, load_data, FoldData, ContentProjector, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise, _abs_dir, _find)


# --------------------------------------------------------------------------- #
# 2D molecular graphs from SMILES (dense, no torch_geometric needed)
# --------------------------------------------------------------------------- #
ATOM_LIST = [6, 7, 8, 9, 15, 16, 17, 35, 53, 5, 14, 1]   # C N O F P S Cl Br I B Si H


def build_2d_graphs(smiles_list, max_atoms=80):
    """Return (atom_feats [n, max_atoms, F], adj [n, max_atoms, max_atoms], mask [n, max_atoms]) or None."""
    try:
        from rdkit import Chem
    except Exception:
        print("[exp7] RDKit not installed -> 2D modality disabled. `pip install rdkit`.")
        return None
    n = len(smiles_list); Fdim = len(ATOM_LIST) + 1
    feats = np.zeros((n, max_atoms, Fdim), np.float32)
    adj = np.zeros((n, max_atoms, max_atoms), np.float32)
    mask = np.zeros((n, max_atoms), np.float32)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
        if mol is None:
            continue
        atoms = mol.GetAtoms()[:max_atoms]
        for a in atoms:
            j = a.GetIdx()
            if j >= max_atoms:
                continue
            z = a.GetAtomicNum()
            feats[i, j, ATOM_LIST.index(z) if z in ATOM_LIST else -1] = 1.0
            mask[i, j] = 1.0
        for b in mol.GetBonds():
            u, v = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
            if u < max_atoms and v < max_atoms:
                adj[i, u, v] = adj[i, v, u] = 1.0
        adj[i] += np.eye(max_atoms, dtype=np.float32) * mask[i][:, None] * mask[i][None, :]
    return feats, adj, mask


class Dense2DEncoder(nn.Module):
    """Two dense GIN-like layers + masked mean pool -> per-drug 2D embedding."""
    def __init__(self, in_dim, d, layers=2):
        super().__init__()
        self.inp = nn.Linear(in_dim, d)
        self.gnn = nn.ModuleList([nn.Linear(d, d) for _ in range(layers)])

    def forward(self, feats, adj, mask):
        deg = adj.sum(-1, keepdim=True).clamp(min=1)
        h = self.inp(feats)
        for lin in self.gnn:
            h = F.relu(lin(torch.bmm(adj, h) / deg))
        h = h * mask.unsqueeze(-1)
        return h.sum(1) / mask.sum(1, keepdim=True).clamp(min=1)      # (n, d)


# --------------------------------------------------------------------------- #
# OPTIONAL 3D conformer encoder (E(3)-invariant via pairwise distances)
# --------------------------------------------------------------------------- #
def build_3d_coords(smiles_list, max_atoms=80):
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except Exception:
        print("[exp7] RDKit not installed -> 3D modality disabled.")
        return None
    n = len(smiles_list)
    coords = np.zeros((n, max_atoms, 3), np.float32); mask = np.zeros((n, max_atoms), np.float32)
    znum = np.zeros((n, max_atoms), np.int64)
    for i, smi in enumerate(smiles_list):
        mol = Chem.MolFromSmiles(smi) if isinstance(smi, str) else None
        if mol is None:
            continue
        mol = Chem.AddHs(mol)
        if AllChem.EmbedMolecule(mol, randomSeed=42) != 0:
            continue
        try:
            AllChem.MMFFOptimizeMolecule(mol)
        except Exception:
            pass
        conf = mol.GetConformer()
        for a in mol.GetAtoms()[:max_atoms]:
            j = a.GetIdx()
            if j >= max_atoms:
                continue
            p = conf.GetAtomPosition(j)
            coords[i, j] = [p.x, p.y, p.z]; mask[i, j] = 1.0
            znum[i, j] = ATOM_LIST.index(a.GetAtomicNum()) if a.GetAtomicNum() in ATOM_LIST else len(ATOM_LIST)
    return coords, znum, mask


class Conformer3DEncoder(nn.Module):
    """Invariant: radial-basis of pairwise distances aggregated per atom, then pooled."""
    def __init__(self, d, n_types=len(ATOM_LIST) + 1, n_rbf=16, cutoff=5.0):
        super().__init__()
        self.emb = nn.Embedding(n_types, d)
        self.centers = nn.Parameter(torch.linspace(0, cutoff, n_rbf), requires_grad=False)
        self.msg = nn.Linear(d + n_rbf, d)
        self.out = nn.Linear(d, d)

    def forward(self, coords, znum, mask):
        h = self.emb(znum)                                            # (n,A,d)
        dist = torch.cdist(coords, coords)                            # (n,A,A)
        rbf = torch.exp(-(dist.unsqueeze(-1) - self.centers) ** 2)    # (n,A,A,rbf)
        pair_mask = (mask.unsqueeze(1) * mask.unsqueeze(2)).unsqueeze(-1)
        agg = (rbf * pair_mask).sum(2)                                # (n,A,rbf)
        h = F.relu(self.msg(torch.cat([h, agg], -1)))
        h = h * mask.unsqueeze(-1)
        return self.out(h.sum(1) / mask.sum(1, keepdim=True).clamp(min=1))


# --------------------------------------------------------------------------- #
# Modality-MoE fusion (MAMEX-style): gate over modality embeddings
# --------------------------------------------------------------------------- #
class ModalityMoE(nn.Module):
    def __init__(self, d, n_modalities):
        super().__init__()
        self.gate = nn.Linear(d, n_modalities)

    def forward(self, mod_list):
        stack = torch.stack(mod_list, dim=1)                          # (n, M, d)
        w = F.softmax(self.gate(stack.mean(1)), dim=-1).unsqueeze(-1) # (n, M, 1)
        return (w * stack).sum(1)                                     # (n, d)


# --------------------------------------------------------------------------- #
# Full model
# --------------------------------------------------------------------------- #
class M3DR(PairwiseDRModel):
    def __init__(self, cfg, fold, graphs2d, conf3d, use_3d=False):
        super().__init__()
        self.cfg = cfg
        d = cfg.emb_dim
        # 1D: ECFP (fold.X_drug) projected
        self.enc_1d = nn.Sequential(nn.Linear(fold.feat_dims[0], d), nn.ReLU(), nn.Dropout(cfg.dropout))
        mods = 1
        self.use_2d = graphs2d is not None
        self.use_3d = use_3d and conf3d is not None
        if self.use_2d:
            self.enc_2d = Dense2DEncoder(graphs2d[0].shape[-1], d); mods += 1
            self.g2 = [torch.tensor(x, device=cfg.device) for x in graphs2d]
        if self.use_3d:
            self.enc_3d = Conformer3DEncoder(d); mods += 1
            self.c3 = [torch.tensor(conf3d[0], device=cfg.device),
                       torch.tensor(conf3d[1], device=cfg.device),
                       torch.tensor(conf3d[2], device=cfg.device)]
        self.moe = ModalityMoE(d, mods)
        # disease/protein content projector (reuse) — only need disease for scoring; keep proteins for graph
        self.proj = ContentProjector(cfg, fold.feat_dims)
        self.dec = RotatEDecoder(cfg)

    def forward(self, fold):
        mods = [self.enc_1d(fold.X_drug)]
        if self.use_2d:
            mods.append(self.enc_2d(self.g2[0], self.g2[1], self.g2[2]))
        if self.use_3d:
            mods.append(self.enc_3d(self.c3[0], self.c3[1], self.c3[2]))
        z_drug = self.moe(mods)                                       # (nR, d) fused drug
        # diseases/proteins from content; drugs = fused modality embedding (cat avoids in-place autograd issues)
        X_full = self.proj(fold)                                      # (N, d)
        X = torch.cat([z_drug, X_full[self.cfg.n_drug:]], dim=0)      # (N, d)
        # one propagation hop over the masked graph to inject collaborative signal
        H = torch.sparse.mm(fold.A_hat, X) + X
        return H

    def score(self, H, d_idx, s_idx):
        return self.dec(H[d_idx], H[self.cfg.n_drug + s_idx])


def run(cfg: Config = None, use_3d=False):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    d = _abs_dir(cfg.drmgne_dir)
    smiles = pd.read_csv(os.path.join(d, "DrugInformation.csv"))["smiles"].tolist()
    print("\n=== Proposal 7 — M³-DR (scaffold) ===")
    graphs2d = build_2d_graphs(smiles)
    conf3d = build_3d_coords(smiles) if use_3d else None
    if graphs2d is None and not use_3d:
        print("[exp7] No extra modalities available (RDKit missing). Falling back to 1D-only "
              "(≈ a content+graph baseline). Install rdkit to enable 2D/3D.")
    return run_cv_pairwise(cfg, data, lambda c, f: M3DR(c, f, graphs2d, conf3d, use_3d=use_3d))


# ----------------------------- EXTENSIONS / TODO ---------------------------- #
# (1) Protein 3D via AlphaFold: download AF-{UNIPROT}-F1-model_v4.pdb (see exp9.fetch_alphafold_pdb),
#     build a residue Cα k-NN graph, encode with an SE(3)/GearNet-style net, add as a protein modality.
# (2) Drug 1D LM: replace ECFP with ChemBERTa/MolFormer embeddings (HuggingFace) for a stronger 1D view.
# (3) BM3 self-supervision: add dropout-view intra/inter-modality alignment loss (no negative sampling).
if __name__ == "__main__":
    run()
