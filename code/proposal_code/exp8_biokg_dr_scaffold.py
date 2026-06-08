"""
Proposal 8 — BioKG-DR (SCAFFOLD): Knowledge-graph-enhanced DR with KEGG + STRING.
Transfers KGCL / KGRec / KGAT (knowledge-graph-enhanced recommendation) to DR.

IDEA: densify the sparse drug–disease graph by attaching an EXTERNAL biological KG —
  Protein—PPI—Protein (STRING) and Protein—member—Pathway (KEGG) — so drug and disease
  connect through biology even with no direct association. STRING/KEGG are label-independent
  (same status as content) => NOT leakage; the drug–disease target edges remain fold-masked.

STATUS:
  * Data fetchers for STRING + KEGG provided (network + caching). Marked TODO to run once.
  * If cache CSVs exist -> builds an augmented adjacency (adds PPI edges + pathway nodes) and trains
    a LightGCN + contrastive(KGCL-style) + RotatE. Else prints fetch instructions.

Run:  python exp8_biokg_dr_scaffold.py
"""
import os
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from common import (Config, load_data, FoldData, ContentProjector, RotatEDecoder,
                    PairwiseDRModel, run_cv_pairwise, _abs_dir, _topk_sparsify, set_seed)

CACHE_DIR = "experiments/biokg_cache"


# --------------------------------------------------------------------------- #
# Data fetchers (run ONCE on Colab; they cache to CSV). Require internet.
# --------------------------------------------------------------------------- #
def fetch_string_ppi(uniprot_ids, species=9606, score_threshold=700, out=None):
    """STRING PPI network for the given UniProt IDs. score_threshold is 0-1000 (700 = 0.7 high-confidence)."""
    import requests
    out = out or os.path.join(CACHE_DIR, "string_ppi.csv")
    os.makedirs(CACHE_DIR, exist_ok=True)
    ids = "%0d".join(uniprot_ids)
    url = (f"https://string-db.org/api/tsv/network?identifiers={ids}"
           f"&species={species}&required_score={score_threshold}")
    print(f"[exp8] querying STRING for {len(uniprot_ids)} proteins ...")
    r = requests.get(url, timeout=120); r.raise_for_status()
    rows = [ln.split("\t") for ln in r.text.strip().split("\n")[1:]]
    df = pd.DataFrame(rows)
    df.to_csv(out, index=False)
    print(f"[exp8] STRING edges saved -> {out} ({len(df)} rows). Columns include preferredName_A/B, score.")
    return out


def fetch_kegg_pathways(uniprot_ids, out=None):
    """Map UniProt -> KEGG gene -> pathways. Caches a (protein_uniprot, pathway_id) table."""
    import requests, time
    out = out or os.path.join(CACHE_DIR, "kegg_pathways.csv")
    os.makedirs(CACHE_DIR, exist_ok=True)
    # 1) UniProt -> KEGG gene id via KEGG conv
    conv = requests.get("https://rest.kegg.jp/conv/genes/" +
                        "+".join(f"uniprot:{u}" for u in uniprot_ids[:100]), timeout=120).text
    up2kegg = {}
    for ln in conv.strip().split("\n"):
        if "\t" in ln:
            up, kg = ln.split("\t"); up2kegg[up.replace("uniprot:", "")] = kg
    pairs = []
    for up, kg in up2kegg.items():
        link = requests.get(f"https://rest.kegg.jp/link/pathway/{kg}", timeout=60).text
        for ln in link.strip().split("\n"):
            if "\t" in ln:
                pairs.append((up, ln.split("\t")[1]))
        time.sleep(0.34)   # be polite to KEGG
    pd.DataFrame(pairs, columns=["uniprot", "pathway"]).to_csv(out, index=False)
    print(f"[exp8] KEGG pathway memberships saved -> {out} ({len(pairs)} rows).")
    return out


# --------------------------------------------------------------------------- #
# Augmented adjacency: add PPI edges (drug|dis|prot kept) + pathway nodes
# --------------------------------------------------------------------------- #
def build_augmented_adj(cfg, fold, data, ppi_csv, kegg_csv):
    """Returns a normalized sparse adjacency over [drug|dis|prot|pathway] including STRING + KEGG."""
    nR, nD, nP = cfg.n_drug, cfg.n_dis, cfg.n_prot
    oR, oD, oP = 0, nR, nR + nD
    prot_ids = pd.read_csv(os.path.join(_abs_dir(cfg.drmgne_dir), "ProteinID.csv")).iloc[:, 0].tolist()
    uni2idx = {u: i for i, u in enumerate(prot_ids)}

    rows, cols = [], []

    def add(M, ro, co, topk=0):
        Mb = _topk_sparsify(M, topk) if topk else M
        r, c = np.where(Mb > 0)
        rows.extend((r + ro).tolist() + (c + co).tolist()); cols.extend((c + co).tolist() + (r + ro).tolist())

    # base biological edges (test drug-disease already masked in fold.A_rd_np)
    add(fold.A_rd_np, oR, oD); add(data.A_rp, oR, oP); add(data.A_pd.T, oD, oP)
    add(data.S_rr, oR, oR, cfg.sim_topk); add(data.S_dd, oD, oD, cfg.sim_topk); add(data.S_pp, oP, oP, cfg.sim_topk)

    # STRING PPI (NEW)  — match by preferredName/UniProt depending on STRING columns
    n_extra_nodes = 0
    if ppi_csv and os.path.exists(ppi_csv):
        df = pd.read_csv(ppi_csv)
        # STRING returns gene names; if you fetched with UniProt accessions, adapt these column names.
        a_col = "stringId_A" if "stringId_A" in df.columns else df.columns[0]
        b_col = "stringId_B" if "stringId_B" in df.columns else df.columns[1]
        added = 0
        for a, b in zip(df[a_col].astype(str), df[b_col].astype(str)):
            ua = a.split(".")[-1]; ub = b.split(".")[-1]
            if ua in uni2idx and ub in uni2idx:
                rows += [oP + uni2idx[ua], oP + uni2idx[ub]]; cols += [oP + uni2idx[ub], oP + uni2idx[ua]]; added += 1
        print(f"[exp8] added {added} STRING PPI edges.")

    # KEGG pathways (NEW pathway nodes appended after proteins)
    extra = nR + nD + nP
    if kegg_csv and os.path.exists(kegg_csv):
        kg = pd.read_csv(kegg_csv)
        path_ids = {p: extra + i for i, p in enumerate(sorted(kg["pathway"].unique()))}
        n_extra_nodes = len(path_ids)
        for up, pth in zip(kg["uniprot"], kg["pathway"]):
            if up in uni2idx:
                pi = path_ids[pth]
                rows += [oP + uni2idx[up], pi]; cols += [pi, oP + uni2idx[up]]
        print(f"[exp8] added {n_extra_nodes} KEGG pathway nodes.")

    N = nR + nD + nP + n_extra_nodes
    idx = torch.tensor([rows, cols], dtype=torch.long)
    A = torch.sparse_coo_tensor(idx, torch.ones(idx.shape[1]), (N, N)).coalesce()
    eye = torch.sparse_coo_tensor(torch.arange(N).repeat(2, 1), torch.ones(N), (N, N))
    A = (A + eye).coalesce()
    deg = torch.sparse.sum(A, 1).to_dense(); dinv = deg.clamp(min=1).pow(-0.5)
    i = A.indices(); v = A.values() * dinv[i[0]] * dinv[i[1]]
    return torch.sparse_coo_tensor(i, v, (N, N)).coalesce().to(cfg.device), N, n_extra_nodes


class BioKG_DR(PairwiseDRModel):
    def __init__(self, cfg, fold, A_aug, N, n_extra):
        super().__init__()
        self.cfg = cfg
        self.A_aug = A_aug
        self.proj = ContentProjector(cfg, fold.feat_dims)
        self.path_emb = nn.Parameter(torch.randn(n_extra, cfg.emb_dim) * 0.02) if n_extra > 0 else None
        self.dec = RotatEDecoder(cfg)
        self.lam_cl = 0.05

    def forward(self, fold):
        X = self.proj(fold)
        if self.path_emb is not None:
            X = torch.cat([X, self.path_emb], 0)
        H = X
        for _ in range(self.cfg.gcn_layers):
            H = torch.sparse.mm(self.A_aug, H)
        return ((X + H) / 2)

    def score(self, H, d_idx, s_idx):
        return self.dec(H[d_idx], H[self.cfg.n_drug + s_idx])

    def compute_loss(self, fold, H, pos, neg):
        base = super().compute_loss(fold, H, pos, neg)
        # KGCL-style cheap denoising contrastive: two dropout views agree
        v1 = F.dropout(H, 0.1, training=True); v2 = F.dropout(H, 0.1, training=True)
        z1 = F.normalize(v1[:self.cfg.n_drug], dim=1); z2 = F.normalize(v2[:self.cfg.n_drug], dim=1)
        cl = F.cross_entropy(z1 @ z2.t() / 0.2, torch.arange(z1.size(0), device=H.device))
        return base + self.lam_cl * cl


def run(cfg: Config = None):
    cfg = cfg or Config(epochs=200, gcn_layers=2)
    data = load_data(cfg)
    ppi = os.path.join(CACHE_DIR, "string_ppi.csv")
    kegg = os.path.join(CACHE_DIR, "kegg_pathways.csv")
    print("\n=== Proposal 8 — BioKG-DR (scaffold) ===")
    if not (os.path.exists(ppi) or os.path.exists(kegg)):
        print("[exp8] No STRING/KEGG cache found. Run ONCE to fetch (needs internet):")
        print("       from exp8_biokg_dr_scaffold import fetch_string_ppi, fetch_kegg_pathways")
        print("       import pandas as pd, os; from common import _abs_dir")
        print("       ids = pd.read_csv(os.path.join(_abs_dir('DRMGNE/data/B-dataset'),'ProteinID.csv')).iloc[:,0].tolist()")
        print("       fetch_string_ppi(ids); fetch_kegg_pathways(ids)")
        print("[exp8] Then re-run. (Proceeding now with base graph only, no KG augmentation.)")

    def build(c, f):
        A_aug, N, n_extra = build_augmented_adj(c, f, data, ppi, kegg)
        return BioKG_DR(c, f, A_aug, N, n_extra)
    return run_cv_pairwise(cfg, data, build)


if __name__ == "__main__":
    run()
