"""
Central config for the MPHAM reproduction.

Every field that the paper LEAVES UNSPECIFIED is exposed here as an explicit
knob, so you can ablate the inferred choices instead of having them buried in
code. Defaults are set to "paper-faithful where stated, sane where inferred".
Fields whose value is a guess are marked  # INFERRED.
"""
from dataclasses import dataclass, field
from typing import Dict, List


# ---- B-dataset (protein-augmented) cardinalities, derived from your CSVs ----
N_DRUG = 269
N_DIS = 598
N_PROT = 1021
N_TOTAL = N_DRUG + N_DIS + N_PROT  # 1888


@dataclass
class Config:
    # ---------- data ----------
    data_dir: str = "data"            # folder holding the B-dataset csvs
    n_drug: int = N_DRUG
    n_dis: int = N_DIS
    n_prot: int = N_PROT

    # Similarity fusion for the diagonal blocks of H0 (S_rr, S_dd, S_pp).
    # The paper never says how fingerprint/PS/sequence and GIP are combined.
    # "mean"      -> elementwise mean of the available similarity sources
    # "gip_fill"  -> use structural sim where it is >0, else fall back to GIP
    # "gip_only"  -> GIP kernel only
    # "struct_only" -> structural sim only (fingerprint / PS / sequence)
    sim_fusion: str = "mean"          # INFERRED

    # GIP kernels in your csvs are precomputed on the FULL association matrix.
    # That is label leakage under CV. recompute_gip=True rebuilds drug/disease
    # GIP per fold from TRAIN-ONLY drug-disease edges (honest). Set False to
    # reproduce the paper's (leaky) numbers.
    recompute_gip: bool = False       # INFERRED / leakage switch

    # Dense similarity matrices used directly as adjacency => every node attends
    # to ~all nodes => over-smoothing. Keep top-k neighbours per row instead.
    # Set sim_topk<=0 to disable (use all >sim_threshold).
    sim_topk: int = 15                # INFERRED (paper unspecified)
    sim_threshold: float = 0.0        # keep edges with weight > threshold

    # ---------- meta-paths ----------
    # distance (number of edges) -> list of meta-path strings over {R,D,P}.
    # These are a concrete instantiation of the (admittedly non-exhaustive) set
    # the paper enumerates in Sec II-C. Edit freely for ablations.
    metapaths: Dict[int, List[str]] = field(default_factory=lambda: {
        1: ["RR", "DD", "PP", "RD", "RP", "PD"],
        2: ["RPR", "RDR", "DPD", "RPD", "RDP"],
        3: ["RPDR", "RDPD", "RPRP"],
    })
    max_distance: int = 3             # paper: <=3 is enough

    # Binarise commuting matrices for the GAT neighbourhood (recommended).
    # If False, the raw (normalised) commuting weights are used as a non-attn
    # aggregation (Variant-2-like).
    binarize_adj: bool = True

    # ---------- model ----------
    emb_dim: int = 128                # paper sweeps {32,64,128,256}; 128/256 best
    n_layers: int = 2                 # INFERRED (paper: "layer l", L unspecified)
    dropout: float = 0.3              # INFERRED
    residual: bool = True             # INFERRED, fights over-smoothing
    layernorm: bool = True            # INFERRED, fights over-smoothing
    # Node-level attention form:
    #   "gat"   -> e_ij = LeakyReLU(a_src.Wh_i + a_dst.Wh_j)   (recommended)
    #   "paper" -> e_ij = a.Wh_j      (literal eq.4, j-only; weak, for ablation)
    node_attn: str = "gat"            # INFERRED reading of eq.4
    predictor_hidden: int = 128

    # ---------- negative sampling ----------
    neg_ratio: int = 1                # train negatives per positive
    resample_neg_each_epoch: bool = True   # INFERRED but important
    # Negatives are drawn ONLY from pairs that are not positive in the FULL
    # matrix (so test positives are never used as train/test negatives twice).

    # ---------- training ----------
    lr: float = 1e-3
    weight_decay: float = 5e-4
    epochs: int = 200
    early_stop_patience: int = 30
    seed: int = 42

    # ---------- evaluation ----------
    n_folds: int = 5
    # "balanced"  -> test set = test positives + equal #random test negatives.
    #                This is almost certainly what the paper reports (AUPR~0.95).
    # "full"      -> all non-train-positive pairs are candidates (realistic,
    #                AUPR will be much lower). Report BOTH.
    eval_mode: str = "balanced"       # INFERRED, drives AUPR massively
    score_threshold: float = 0.5      # for Precision/Recall/F1 only
