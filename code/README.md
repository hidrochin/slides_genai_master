# MPHAM reproduction (B-dataset) — reverse-engineered

A from-scratch PyTorch reproduction of *"A Novel Drug Repositioning Method Using
Meta-Path Aggregating via Hierarchical Attention Mechanism" (MPHAM)*, targeted at
the **protein-augmented B-dataset** described in your `dataset.txt`.

```
mpham/config.py     every omitted detail as an explicit, ablatable knob
mpham/data.py       B-dataset csv loader, similarity fusion, per-fold GIP, neg sampling
mpham/metapaths.py  H0 block matrix, commuting matrices, test-edge masking
mpham/model.py      3-level hierarchical attention + predictor (eqs 2-14)
mpham/train.py      leakage-aware 5-fold CV, balanced/full eval, AUC/AUPR
smoke_test.py       numpy-only correctness checks (passes)
```

Run: put the csvs in `data/`, then `python -m mpham.train`.

> The data/meta-path/masking/GIP/neg-sampling logic is verified by `smoke_test.py`.
> The torch graph wasn't executed in the authoring sandbox (no torch); it is built
> against the same verified tensors.

---

## 1. Inferred implementation details (what the paper omits)

| Aspect | Paper says | Inferred choice (and why) |
|---|---|---|
| **Feature init `H0`** | Eq.1 block matrix | Diagonal blocks need a *fusion* of struct-sim + GIP — unspecified. Default `mean`. Off-diagonals are the binary association matrices. |
| **Similarity fusion** | "generalized Jaccard / MeSH for disease sim" only | Drug=fingerprint⊕GIP, disease=PS⊕GIP, protein=sequence⊕(GIP_drug,GIP_dis). `mean` default; `gip_fill`/`gip_only` exposed. |
| **Meta-path set** | Lists ~5 drug-centric paths "to some extent" (non-exhaustive) | Concrete set in `config.metapaths`, grouped by distance 1/2/3. Edit for ablation. |
| **Commuting-matrix scale** | not mentioned | Products like `A_rp·A_pd` have large integer entries → must **binarise** (for GAT) or **row-normalise** (for sum). Done. |
| **Similarity density** | not mentioned | `S_rr/S_dd/S_pp` are dense → naïve adjacency = near-complete graph = over-smoothing. **top-k=15** sparsify. |
| **Node attention** | Eq.4 `e_ij = a·Wh_j` (j-only) | Literal eq.4 is degenerate (i-independent). Default `gat` (`a_src·Wh_i + a_dst·Wh_j`); `paper` form kept for ablation. |
| **Pattern/distance attn** | Eqs.7-12, per-node softmax | Implemented per-node, shared transform + learnable context (`u_a`,`u_b`), HAN-style. |
| **# layers L** | "layer l", L never given | Default **2** (K=3 distances × deep L over-smooths a 11%-dense graph). |
| **Residual / norm** | none | Added (toggle). Without them, ≥3 layers collapse embeddings. |
| **Negative sampling** | "random sampling from unlabeled pairs" (Conclusion) | 1:1, **resampled every epoch**, excluded from positives *and* fixed test negatives. |
| **Training** | Adam, Xavier, BCE | + grad-clip 5.0, wd 5e-4, early stop on fold AUC. |
| **Eval composition** | "threshold on score → pos/neg" | **balanced** test set (pos + equal random neg). This is the big AUPR lever; `full` mode also provided. |

---

## 2. Likely mismatches / hidden assumptions / leakage in a typical repro

These are keyed to the components you listed (graph construction, meta-path agg,
hierarchical attention, neg sampling, CV, BCE, AUC/AUPR).

**Data leakage (most damaging, and most likely to make *your* AUC look fine while
masking real bugs):**
1. **`H0` still contains test drug-disease edges.** `H0` literally embeds `Y_{r-d}`
   (eq.1). If you build it once from the full matrix, the label is an input
   feature. → `metapaths.mask_test_edges` rebuilds `H0` per fold from train-only.
2. **Meta-paths traverse test edges.** `RD`, `RDR`, `RPD`, `RPDR`, `RDPD` all use
   `A_rd`. Masking only `H0` but not the commuting matrices still leaks. → all
   adjacencies are rebuilt from `A_rd_train`.
3. **GIP kernels are precomputed on the full matrix** (`DrugGIP.csv`, `DiseaseGIP.csv`).
   They encode every positive, including test. The paper almost certainly used the
   precomputed (leaky) kernels — that's a large part of why AUC≈0.97. `recompute_gip`
   toggles honest per-fold GIP. Expect a drop when you turn it on; that drop is the
   leakage, not your bug.

**Correctness / stability:**
4. **No commuting-matrix normalisation** → exploding activations, NaNs after a few
   epochs, or one meta-path dominating. Binarise or row-normalise.
5. **Dense similarity adjacency** → node-level attention spreads over ~all nodes →
   over-smoothing; the "meta-path locality" the paper sells is lost. top-k fixes it.
6. **Masked-softmax NaNs** for isolated nodes (a row of all `-inf`). Handle by
   zeroing those rows (`model._node_attention`).
7. **Literal eq.4 attention** is i-independent; if you implemented it verbatim, your
   node-attention is basically a global node bias, not real attention.

**Imbalance / evaluation:**
8. **Eval negative ratio drives AUPR more than the model does.** 11.4% density;
   balanced test → AUPR≈AUC≈0.95; full-matrix test → AUPR can fall to ~0.3–0.5.
   If your AUPR is "too low," check this before touching the architecture.
9. **Fixed (not resampled) train negatives** → the model memorises the negative set;
   train loss looks great, test AUC stalls.
10. **Precision/Recall/F1 at 0.5** won't match the paper unless they tuned the
    threshold; report at a swept threshold (e.g. Youden / max-F1).

**Semantics:**
11. **Protein-disease file is stored as `(disease, protein)`** — easy to transpose by
    accident, which silently corrupts `A_pd` and every `*P*` meta-path. Loader handles it.
12. **Wrong cardinalities** — make sure you're on B (269/598/1021), not Hetero-A
    (708/5603/1512). Mixing breaks `H0` blocks.

---

## 3. Top reproduction gaps, ranked by probability × impact

| # | Gap | P(it's your issue) | AUC impact | AUPR impact |
|---|---|---|---|---|
| 1 | Eval negative composition (balanced vs full) | **High** | small | **huge** (0.95↔0.4) |
| 2 | Test edges leak via `H0` + GIP + meta-paths | **High** | **large** (±0.03–0.06) | large |
| 3 | Commuting-matrix normalisation / dense-sim over-smoothing | High | medium–large | medium |
| 4 | Per-epoch negative resampling | Medium-high | medium | medium |
| 5 | Similarity fusion (mean vs gip_fill vs struct) | Medium | small–medium | small–medium |
| 6 | Node-attention form (gat vs literal eq.4) | Medium | small | small |
| 7 | #layers / residual / norm (over-smoothing) | Medium | medium | medium |
| 8 | Embedding dim (128/256 best per heatmaps) | Medium | small–medium | small–medium |
| 9 | Threshold for P/R/F1 | Low (for AUC/AUPR) | none | none |
| 10 | Cardinality / `A_pd` transpose bug | Low but catastrophic if present | breaks run | breaks run |

**Net read:** to *match the paper's headline numbers* you most likely need
`eval_mode="balanced"` + leaky GIP (`recompute_gip=False`) + test edges present in
`H0` (i.e., the paper's leakage). To get an *honest* model, flip those on and expect
AUC≈0.90–0.94 and full-mode AUPR well below the reported 0.95. The delta between
those two configs is your "reproduction gap" and it's mostly evaluation protocol +
leakage, not architecture.

---

## 4. Ablation roadmap (run in this order)

Each step changes exactly one knob so you can attribute the delta.

```
A. PROTOCOL (explains most of the gap)
   A1 eval_mode = balanced  vs  full            -> isolate AUPR collapse
   A2 recompute_gip = False vs True             -> size the GIP leakage
   A3 leave test edges in H0 vs masked          -> size structural leakage
        (compare a "leaky" run to the masked default)

B. AGGREGATION
   B1 binarize_adj True vs row-normalised        -> stability/scale
   B2 sim_topk in {none, 5, 15, 50}              -> over-smoothing vs info
   B3 metapaths: distance {1}, {1,2}, {1,2,3}    -> reproduce paper Fig.4 (len<=3)

C. ATTENTION (the paper's headline contribution; mirror Table IV)
   C1 node_attn = gat vs paper                   -> eq.4 sanity
   C2 full model vs sum-fusion (set all attn=uniform)   -> "w/o Attention" variant
   C3 meta-paths vs plain 1-hop GCN              -> "w/o MP" variant

D. CAPACITY
   D1 emb_dim {32,64,128,256}                    -> reproduce Fig.5/6 heatmaps
   D2 n_layers {1,2,3} × residual/layernorm on/off  -> over-smoothing curve
   D3 neg_ratio {1,5,10} and resample on/off     -> imbalance robustness
```

Expected signatures: A1 moves AUPR by ~0.4–0.5 with AUC nearly flat (confirms it's
protocol). A2/A3 each move AUC by ~0.02–0.05 (confirms leakage). C2/C3 should drop
AUC to ~0.94 and ~0.90 respectively — matching the paper's Table IV ablation
("w/o Attention" 0.943, "w/o MP" 0.906); if your ablations *don't* reproduce that
ordering, your attention or meta-path module is mis-wired.
