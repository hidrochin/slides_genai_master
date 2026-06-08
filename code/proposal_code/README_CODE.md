# Proposal Code — How to Run

Code implementing the proposals in [`README.md`](README.md). Designed for a **Colab GPU kernel**.

## Files

| File | What |
|---|---|
| `common.py` | Shared foundation: data loading, SMILES→ECFP features, strict per-fold CV with masking, honest val-based selection, metrics (1:1 + 1:5), reusable modules (`ContentProjector`, `LightGCNEncoder`, `RotatEDecoder`), and the generic `run_cv_pairwise` trainer. **Everything imports this.** |
| `exp1_diffudr.py` | **Prop 1 DiffuDR** — conditional diffusion over disease-rows (no negative sampling). Custom loop. |
| `exp2_semdr.py` | **Prop 2 SemDR** — RQ-VAE semantic IDs + generative Transformer (TIGER). Custom loop. |
| `exp3_hypodr.py` | **Prop 3 HypoDR** — disentangled hyperbolic (Poincaré) MoA channels. |
| `exp4_causaldr.py` | **Prop 4 CausalDR** — counterfactual popularity debiasing + IPW. |
| `exp5_momoe_dr.py` | **Prop 5 MoMoE-DR** — sparse mixture-of-experts + load balancing. |
| `exp6_noisedr.py` | **Prop 6 NoiseDR** — XSimGCL noise-contrastive + degree-aware temperature. |
| `exp7_m3dr_scaffold.py` | **Prop 7 M³-DR** (scaffold) — 1D ECFP + 2D RDKit graph (+optional 3D) modality-MoE. Runnable with RDKit. |
| `exp8_biokg_dr_scaffold.py` | **Prop 8 BioKG-DR** (scaffold) — STRING/KEGG fetchers + augmented-KG model. |
| `exp9_geobind_dr_scaffold.py` | **Prop 9 GeoBind-DR** (scaffold) — AlphaFold fetcher + 3D binding-prior skeleton. |
| `run_proposals.ipynb` | Colab notebook: setup + one cell per proposal + results table. |

## Quick start (Colab)

1. Open `run_proposals.ipynb`, connect a GPU runtime.
2. Run the **Setup** cell — it clones DRMGNE (base data + SMILES) and `pip install rdkit scikit-learn requests`.
3. For the richest features, upload the **`GCGB/data`** folder (MeSH `DiseaseFeature.csv` + `Protein_ESM.csv`) next to `DRMGNE/`. If absent, the code auto-falls-back to similarity-row features and still runs.
4. Run the proposal cells. Each prints per-fold + MEAN `AUROC / AUPR / AUPR(1:5)`.

From a plain terminal you can also do `cd <repo>; python experiments/exp6_noisedr.py` (data dirs must be findable; `common._abs_dir` searches cwd, `/content`, `..`).

## What runs today vs needs a fetch

- **Prop 1–6 + Prop 7**: run immediately on the B-dataset (Prop 7 needs `rdkit`).
- **Prop 8 (BioKG-DR)**: run `fetch_string_ppi(ids)` and `fetch_kegg_pathways(ids)` **once** (internet), then re-run — it builds the augmented KG and trains.
- **Prop 9 (GeoBind-DR)**: run `fetch_alphafold_pdb(ids)` **once**, then fill in `compute_struct_prior()` steps 1–4. Until then it runs the two-tower recommender without the structural prior.

## Config knobs (`common.Config`)

`emb_dim` (256), `epochs`, `gcn_layers` (2), `lr` (1e-3), `neg_ratio` (1), `n_folds` (5), `val_frac` (0.1),
`drug_feat` (`"ecfp"` | `"fingerprint"` fallback), `ecfp_bits` (2048), `sim_topk` (10).
Switch dataset by pointing `drmgne_dir`/`gcgb_dir` at `C-dataset`/`F-dataset` and setting `n_drug/n_dis/n_prot`.

## Honesty guarantees (baked in)

- Test drug–disease edges are masked from the propagation graph, degrees, and diffusion target **every fold**.
- Model selection uses a 10% **val** split, never the test fold.
- GIP matrices are never read. Drug features come from SMILES (asserted non-degenerate), never `Drug_mol2vec.csv`.
- Both balanced (1:1) and imbalanced (1:5) metrics are reported. Treat any honest AUROC > 0.93 as a suspected leak.

## Notes & expected behaviour

- These are **research baselines**, not tuned SOTA. Expect them in the rough range of the MPHAM honest baseline (~0.88–0.91 AUROC) before tuning; the point is to demonstrate each *mechanism* cleanly and ablate it.
- `exp2_semdr` is scored by sequence-likelihood for AUROC, but its real strength is **cold-start Recall@k** — add an inductive split (hold out whole drugs) for the report.
- Speed: on a Colab T4, Prop 3/4/5/6/7 ≈ a few minutes each at 200 epochs; Prop 1 (diffusion) and Prop 2 (transformer) are a bit longer. Lower `epochs` for a quick smoke test.
