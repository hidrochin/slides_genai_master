"""
Proposal 9 — GeoBind-DR (SCAFFOLD): 3D structure-aware binding prior.
Transfers two-tower retrieval + E(3)-equivariant 3D interaction (RecSys two-tower + structural bio).

IDEA: a drug-conformer tower and a protein-pocket (AlphaFold) tower produce a learned,
  LABEL-FREE binding compatibility b(drug, protein). Propagate drug→protein(binding)→disease to a
  structure-grounded prior s_struct, then gate-fuse with a recommender score s_rec.

STATUS:
  * Drug 3D conformer encoder: reuse exp7.Conformer3DEncoder (RDKit) — runnable.
  * Protein 3D tower: needs AlphaFold .pdb per UniProt -> fetch_alphafold_pdb provided (TODO run once).
  * Binding head + propagation + fusion: implemented as a skeleton; wire once protein 3D is cached.

Run:  python exp9_geobind_dr_scaffold.py   (prints what to fetch; runs the s_rec recommender meanwhile)
"""
import os
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
from common import (Config, load_data, FoldData, LightGCNEncoder, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise, _abs_dir)

CACHE_DIR = "experiments/alphafold_cache"


# --------------------------------------------------------------------------- #
# AlphaFold structure fetch (run ONCE; caches .pdb per UniProt). Needs internet.
# --------------------------------------------------------------------------- #
def fetch_alphafold_pdb(uniprot_ids, version="v4", out_dir=None):
    import requests
    out_dir = out_dir or CACHE_DIR
    os.makedirs(out_dir, exist_ok=True)
    ok, miss = 0, 0
    for u in uniprot_ids:
        path = os.path.join(out_dir, f"{u}.pdb")
        if os.path.exists(path):
            ok += 1; continue
        url = f"https://alphafold.ebi.ac.uk/files/AF-{u}-F1-model_{version}.pdb"
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 200:
                open(path, "w").write(r.text); ok += 1
            else:
                miss += 1
        except Exception:
            miss += 1
    print(f"[exp9] AlphaFold: {ok} structures cached, {miss} missing -> {out_dir}")
    return out_dir


def parse_ca_coords(pdb_path, max_res=512):
    """Return Cα coordinates (R,3) and a residue-type index from a .pdb file."""
    coords = []
    for ln in open(pdb_path):
        if ln.startswith("ATOM") and ln[12:16].strip() == "CA":
            coords.append([float(ln[30:38]), float(ln[38:46]), float(ln[46:54])])
            if len(coords) >= max_res:
                break
    return np.array(coords, np.float32) if coords else None


# --------------------------------------------------------------------------- #
# Protein 3D pocket tower (SE(3)-invariant via Cα pairwise distances) — skeleton
# --------------------------------------------------------------------------- #
class ProteinPocketTower(nn.Module):
    def __init__(self, d, n_rbf=16, cutoff=12.0):
        super().__init__()
        self.centers = nn.Parameter(torch.linspace(0, cutoff, n_rbf), requires_grad=False)
        self.node = nn.Parameter(torch.randn(d) * 0.02)              # shared residue token (no seq used here)
        self.msg = nn.Linear(d + n_rbf, d)
        self.out = nn.Linear(d, d)

    def forward(self, coords_list):
        """coords_list: list of (R_i, 3) tensors -> (n_prot, d)."""
        embs = []
        for coords in coords_list:
            if coords is None or len(coords) == 0:
                embs.append(torch.zeros(self.out.out_features, device=self.node.device)); continue
            R = coords.shape[0]
            h = self.node.unsqueeze(0).expand(R, -1)
            dist = torch.cdist(coords, coords)
            rbf = torch.exp(-(dist.unsqueeze(-1) - self.centers) ** 2).sum(1)   # (R, rbf)
            h = F.relu(self.msg(torch.cat([h, rbf], -1)))
            embs.append(self.out(h.mean(0)))
        return torch.stack(embs, 0)


# --------------------------------------------------------------------------- #
# Full model: s_rec recommender (+ optional structural prior fusion)
# --------------------------------------------------------------------------- #
class GeoBindDR(PairwiseDRModel):
    def __init__(self, cfg, fold, struct_prior=None):
        super().__init__()
        self.cfg = cfg
        self.enc = LightGCNEncoder(cfg, fold.feat_dims)
        self.dec = RotatEDecoder(cfg)
        # struct_prior: optional precomputed (nR x nD) numpy prior from drug-conformer × protein-pocket
        self.struct = None
        if struct_prior is not None:
            self.struct = torch.tensor(struct_prior, device=cfg.device)
            self.alpha = nn.Parameter(torch.tensor(0.3))

    def forward(self, fold):
        return self.enc(fold)

    def score(self, H, d_idx, s_idx):
        s_rec = self.dec(H[d_idx], H[self.cfg.n_drug + s_idx])
        if self.struct is not None:
            a = torch.sigmoid(self.alpha)
            return (1 - a) * s_rec + a * self.struct[d_idx, s_idx]
        return s_rec


def compute_struct_prior(cfg, data):
    """TODO wiring: build s_struct (nR x nD) = drug_conformer × protein_pocket binding, propagated via protein-disease.
       Requires AlphaFold .pdb cache + RDKit conformers. Returns None if structures unavailable."""
    prot_ids = pd.read_csv(os.path.join(_abs_dir(cfg.drmgne_dir), "ProteinID.csv")).iloc[:, 0].tolist()
    if not os.path.isdir(CACHE_DIR) or len(os.listdir(CACHE_DIR)) == 0:
        return None
    # --- skeleton (fill in to enable the structural prior) ---
    #  1) drug_emb = exp7.Conformer3DEncoder over RDKit conformers            -> (nR, d)
    #  2) coords = [parse_ca_coords(f"{CACHE_DIR}/{u}.pdb") for u in prot_ids]
    #     prot_emb = ProteinPocketTower(d)(coords)                            -> (nP, d)
    #  3) b = sigmoid(drug_emb @ prot_emb.T)                                  -> (nR, nP) binding compat
    #  4) s_struct = b @ data.A_pd.T  (protein->disease), row-normalised      -> (nR, nD)
    print("[exp9] AlphaFold cache present — fill in compute_struct_prior() steps 1-4 to enable the prior.")
    return None


def run(cfg: Config = None):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    print("\n=== Proposal 9 — GeoBind-DR (scaffold) ===")
    prior = compute_struct_prior(cfg, data)
    if prior is None:
        print("[exp9] No structural prior yet. To enable: \n"
              "       from exp9_geobind_dr_scaffold import fetch_alphafold_pdb\n"
              "       import pandas as pd, os; from common import _abs_dir\n"
              "       ids = pd.read_csv(os.path.join(_abs_dir('DRMGNE/data/B-dataset'),'ProteinID.csv')).iloc[:,0].tolist()\n"
              "       fetch_alphafold_pdb(ids)   # downloads ~1021 .pdb files\n"
              "       then implement compute_struct_prior() steps 1-4.\n"
              "[exp9] Running the s_rec recommender (two-tower without the structural prior) for now.")
    return run_cv_pairwise(cfg, data, lambda c, f: GeoBindDR(c, f, struct_prior=prior))


if __name__ == "__main__":
    run()
