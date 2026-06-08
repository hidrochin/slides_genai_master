# New Architecture Proposals for Drug Repositioning
## Transferring SOTA from Recommendation Systems

> **Design rule (hard constraint):** Each proposal may resemble existing **Drug Repositioning (DR)** methods (MPHAM, DRMGNE, GCGB, RGLDR, GraphSAGE-DR) by **at most ~15%**. It is allowed — even encouraged — to resemble **Recommendation System (RecSys)** SOTA by *more* than 15%, because the novelty thesis of this work is *"DR is a link-prediction / implicit-feedback problem, so the most advanced RecSys machinery should be ported and adapted to biology."*
>
> Every proposal below therefore (a) names the DR weakness it attacks, (b) names the RecSys SOTA it transfers, (c) gives a concrete architecture, (d) states the leakage guard, and (e) includes a **Novelty Audit** quantifying overlap with DR vs RecSys.

---

## 0. Recap — Weaknesses We Are Attacking

From the parent [`README.md`](../README.md) strength/weakness analysis, the recurring failures across **all** existing DR methods are:

| # | Weakness | Who suffers | Root cause |
|---|----------|-------------|------------|
| W1 | **Transductive only** — no cold-start for unseen drugs/diseases | MPHAM, DRMGNE, GCGB, RGLDR | Embedding table is fixed at train time |
| W2 | **Naive negatives** — "unknown = negative" + ad-hoc hard-neg mixing | MPHAM, DRMGNE | Binary classification framing of a positive-unlabeled (PU) problem |
| W3 | **Research / popularity bias** — aspirin-like hubs dominate; long-tail drugs starved | All | Known associations reflect research attention, not biology |
| W4 | **Data sparsity & imbalance** — C-dataset 0.93%, F-dataset 1.04% density | All | Few positives, no cross-dataset transfer |
| W5 | **Over-smoothing / fixed depth** | MPHAM, DRMGNE | Same propagation depth for hub & peripheral nodes |
| W6 | **Quadratic scaling** — N×N matrices (1888×1888) | MPHAM, GCGB | Full-graph dense operations |
| W7 | **Entangled, uninterpretable embeddings** | All | One vector mixes all mechanisms-of-action |
| W8 | **Gradient conflict** between main + auxiliary tasks | GCGB | Hand-tuned loss weights / custom optimizer |

Each proposal targets one or more of W1–W8.

---

## 0.5 — Data Reality Check (verified by reading the actual files)

Before committing to any content-feature-dependent design, I inspected the downloaded files in `GCGB/data/{B,C,F}-dataset/`. **One finding overrides several earlier assumptions:**

| Content feature | Shape (B / C / F) | Unique rows | Verdict |
|---|---|---|---|
| `Drug_mol2vec.csv` | 300-dim × (269 / 663 / 592) | **2 / 2 / 2** | ❌ **DEGENERATE — DO NOT USE.** 223 drugs share one vector, 46 share another (B-dataset). Same breakage in C and F. Carries ≈1 bit of drug information. |
| `DrugInformation.csv` (**SMILES**) | 269 / 663 / 592 drugs | **269 / 662 / 592 unique** | ✅ **CLEAN — this is the real drug signal.** Includes DrugBank ID + canonical SMILES. |
| `DiseaseFeature.csv` (**MeSH**) | 64-dim × (598 / 409 / 313) | 570 / 393 / 305 | ⚠️ **Usable**, but **29 / 16 / 8 diseases have all-zero (missing) MeSH vectors** → needs imputation. |
| `Protein_ESM.csv` (**ESM-2**) | 320-dim × (1021 / 993 / 2741) | all unique | ✅ **Fully clean** — usable as-is. |

**Implications (these drive the updates below):**
1. **Any proposal that needs drug content MUST derive it from raw SMILES, not `Drug_mol2vec.csv`.** Encode SMILES with a molecular encoder — RDKit ECFP4/Morgan fingerprint (cheap), or a pretrained molecular language model (ChemBERTa / MolFormer / Uni-Mol) for a semantic embedding. **This is not a detour from the thesis — it is the RecSys pattern itself:** TIGER and modern generative recommenders build item representations from a *modality/content encoder* (often an LLM), then quantize. Using a molecular LM as the "drug modality encoder" is the faithful transfer.
2. **Disease content (MeSH) is usable** but impute the 29/16/8 missing rows (e.g., mean of k-NN diseases by name string / DiseasePS similarity).
3. **Protein content (ESM-2) is the strongest clean signal** — lean on it for protein-mediated paths.
4. **Cross-dataset transfer (Proposal 5) is concretely feasible:** disease (64-dim) and protein (320-dim) feature spaces are *identical* across B/C/F, and a SMILES encoder yields a shared drug space — so experts/encoders can be shared across datasets without dimension surgery.
5. **C-dataset ships pre-built 10-fold splits** (`C-dataset/fold/0..9/data_{train,test}.csv`) — use them for honest, reproducible evaluation.

> Net effect: the proposals do not weaken. The broken mol2vec actually **pushes the design further toward RecSys SOTA** (content/modality encoder → quantize / condition), which is exactly the allowed novelty direction.

---

## 0.6 — Shared notation & dimensions (use these when drawing)

Every "Drawable architecture" block below uses these symbols so all diagrams stay consistent. Numbers are for the **B-dataset**; swap the counts for C/F.

| Symbol | Meaning | B value |
|---|---|---|
| `n_R` | # drugs | 269 |
| `n_S` | # diseases | 598 |
| `n_P` | # proteins | 1021 |
| `N` | total nodes (`n_R+n_S+n_P`) | 1888 |
| `d` | main embedding dim | 256 |
| `ECFP` | RDKit Morgan/ECFP4 bit length (drug content, offline-safe) | 2048 |
| `CB` | ChemBERTa/MolFormer dim (drug content, optional LM) | 768 |
| `MeSH` | disease content dim | 64 |
| `ESM` | protein content dim (ESM‑2) | 320 |

**Box colour convention (matches the parent `Architecture.md`):** data/matrix = blue `#dae8fc`; learned module = green `#d5e8d4`; attention/soft = yellow `#fff2cc`; loss/output = orange `#ffe6cc`; deletion/zero = red `#f8cecc`; new RecSys-transferred block = purple `#e1d5e7`.

**Three content encoders are reused by Proposals 1, 2, 3, 5, 6** — draw them once as a shared "Content Encoder" stack:

```
ENC_drug :  SMILES ─► RDKit ECFP4 (2048)  ─► MLP[2048→512→d]  ─► X_R ∈ ℝ^{n_R×d}      (green; NOT mol2vec)
            (optional LM variant: SMILES ─► ChemBERTa (768) ─► MLP[768→d] ─► X_R)
ENC_dis  :  MeSH (64, impute 29 zero-rows) ─► MLP[64→d]       ─► X_S ∈ ℝ^{n_S×d}
ENC_prot :  ESM-2 (320, clean)             ─► MLP[320→d]      ─► X_P ∈ ℝ^{n_P×d}
```
Stack `X = [X_R ; X_S ; X_P] ∈ ℝ^{N×d}` is the shared node-feature matrix wherever a proposal needs initial node features.

---

## Proposal 1 — **DiffuDR**: Conditional Diffusion as a Generative DR Engine

**Targets:** W2 (naive negatives), W3 (popularity bias), W4 (sparsity), + uncertainty quantification.
**Transfers from RecSys:** DiffRec / DiffuRec / DiffGRM — *diffusion recommenders that reconstruct a user's full interaction vector by denoising, instead of scoring sampled negatives.*

### The core re-framing
Every existing DR method scores one `(drug, disease)` pair at a time and **needs negative sampling** — which is exactly W2's root cause (treating unlabeled pairs as negatives is statistically wrong for a PU problem). RecSys diffusion models sidestep this entirely: they treat each user's interaction row `x₀ ∈ {0,1}^{|items|}` as the data point and learn `p(x₀)` via a denoising process. **No negative sampling exists** — the whole row (positives *and* unknowns) is reconstructed as a distribution.

### Architecture
```
For each drug d: target = its disease-association row  x₀ ∈ ℝ^{598}  (train-fold only)
Forward (fixed):   x_t = √ᾱ_t · x₀ + √(1-ᾱ_t) · ε          ε ~ N(0,I)
Condition vector:  c_d = Encoder(content_d, train-graph_d)   # SMILES-LM/ECFP + ESM + masked GNN
                                                            # (NOT mol2vec — it is degenerate, see §0.5)
Reverse (learned): ε_θ(x_t, t, c_d)  →  denoise  →  x̂₀ = predicted association profile
Inference:         start from pure noise, run reverse chain conditioned on c_d
                   → full ranked disease profile for drug d (one shot, no per-pair scoring)
```
- Denoiser is a small **conditional MLP / U-Net over the 598-dim disease axis** (not a graph op → cheap).
- Popularity bias (W3) is attacked structurally: a diffusion model fits the **distribution** of profiles, so rare diseases are generated with calibrated probability rather than crushed by a discriminative loss dominated by hub diseases.
- Sparsity (W4): the denoising objective is dense self-supervision over the entire row every step — far more signal than 1:1 sampled BCE.

### Drawable architecture

**Boxes (modules):**

| # | Module | Type | Input → Output shape | Key params |
|---|---|---|---|---|
| M1 | Content encoders (shared `ENC_drug/dis/prot`) | MLP ×3 | SMILES/MeSH/ESM → `X ∈ ℝ^{N×d}` | see §0.6 |
| M2 | Condition graph encoder | 2-layer LightGCN/GAT on **fold-masked** D–S–P graph | `X (N×d)` → `G ∈ ℝ^{N×d}` | 2 layers, no self-loop |
| M3 | Conditioner fusion | concat + MLP | `[X_R ‖ G_R] (n_R×2d)` → `c ∈ ℝ^{n_R×d}` | `2d→d` |
| M4 | Timestep embed | sinusoidal + MLP | `t (scalar)` → `t_emb ∈ ℝ^{d}` | sinusoid(128)→`d` |
| M5 | Noisy-row input proj | Linear | `x_t ∈ ℝ^{n_R×n_S}` → `ℝ^{n_R×512}` | `n_S→512` |
| M6 | Denoiser core | 3× FiLM residual MLP block | `512 (+c +t_emb)` → `512` | SiLU, cond via FiLM |
| M7 | Noise output head | Linear | `512` → `ε̂ ∈ ℝ^{n_R×n_S}` | `512→n_S` |

**Wiring (training step):**
```
                         ┌──────────────── condition path (per drug) ───────────────┐
 SMILES ─►[M1 ENC_drug]─►X_R(n_R×d)─┐                                                │
                                    ├─►[M3 fuse 2d→d]─►c (n_R×d)──────────┐          │
 D–S–P graph(masked)─►[M2 GNN]─►G_R(n_R×d)┘                               │          │
                                                                         ▼          │
 t ─►[M4 sinusoid+MLP]─► t_emb(d) ─────────────────────────────────► (FiLM cond)    │
                                                                         │          │
 x₀ = drug×disease row  (n_R×n_S, train-only)                            │          │
        │ forward diffusion  q(x_t|x₀)=√ᾱ_t·x₀+√(1-ᾱ_t)·ε                │          │
        ▼                                                                ▼          │
   x_t (n_R×n_S) ─►[M5 Lin n_S→512]─► h(512) ─►[M6 3×ResBlock 512]─►[M7 Lin 512→n_S]─► ε̂ (n_R×n_S)
                                                                                    │
                                              L_diff = ‖ ε − ε̂ ‖²  ◄───────────────┘
```

**Wiring (inference / scoring a drug):**
```
x_T ~ N(0,I) (1×n_S) ─►[reverse DDIM ×50, conditioned on c, t_emb]─► x̂₀ (1×n_S)
                                                                      = ranked disease scores for that drug
```

**Concrete hyper-parameters:** `d=256`; diffusion `T=1000` (train) / `50` DDIM steps (infer); cosine `ᾱ_t` schedule; M6 hidden = 512, 3 blocks; Adam `lr=1e-3`. Output `x̂₀[j]` ∈ ℝ is the score for disease `j`; rank to get predictions.

### Loss
`L = E_{t,ε}[ ‖ε − ε_θ(x_t, t, c_d)‖² ]` + optional ELBO reweighting (DiffRec-style importance sampling of t).

### Leakage guard
Conditioner `c_d` uses only content (SMILES-derived drug embedding + ESM protein context; **mol2vec excluded — degenerate per §0.5**) + **train-fold-masked** graph; the target row `x₀` has test edges zeroed. Test diseases are never in `x₀` during training.

### Novelty Audit
- **vs DR: ~5%** (shares only "use content features + a graph encoder for the condition"). No DR paper uses diffusion or row-wise generative modeling.
- **vs RecSys: ~70%** (DiffRec's denoise-the-interaction-row recipe, adapted to drug→disease rows and biological conditioners).

---

## Proposal 2 — **SemDR**: Semantic-ID Generative Retrieval (TIGER for biology)

**Targets:** W1 (cold-start), W6 (quadratic scaling), W7 (interpretability).
**Transfers from RecSys:** TIGER / RQ-VAE semantic IDs / LIGER / ETEGRec / OneRec — *quantize each item into a short sequence of discrete tokens, then autoregressively generate the IDs of items to recommend.*

### The core re-framing
DR's W1 (transductive) and W6 (N×N) both stem from a fixed embedding table indexed by node ID. RecSys generative retrieval replaces the table with **content-derived discrete codes**: a brand-new item gets a semantic ID *for free* from its features, and retrieval becomes **token generation** over a short sequence — O(L) not O(N²).

> **⚠️ Data-driven correction (see §0.5):** the obvious choice — quantize `Drug_mol2vec.csv` — would be fatal here: with only **2 unique mol2vec vectors**, RQ-VAE would map all 269 drugs to ≈2 semantic IDs and the model would be unable to distinguish drugs at all. The tokenizer is therefore re-specified to run on a **molecular content encoder over raw SMILES**, which is *more* faithful to TIGER anyway (TIGER tokenizes a content/modality encoder's output, not a precomputed degenerate vector).

### Architecture
```
Stage A — Tokenizer (RQ-VAE on a CONTENT ENCODER, not raw mol2vec):
   drug:    SMILES (DrugInformation.csv) → ChemBERTa/MolFormer or RDKit ECFP4
                                          → RQ-VAE → semantic ID  e.g. (c₁=12, c₂=7, c₃=41)
   disease: MeSH 64-dim (impute 29 missing) → RQ-VAE → semantic ID  (c₁=3, c₂=22, c₃=9)
   protein: ESM-2 320-dim (clean)           → RQ-VAE → semantic ID  (used as path context)
   (residual quantization → coarse-to-fine codebooks → similar molecules share prefixes)

Stage B — Generative recommender (encoder-decoder Transformer):
   INPUT  : drug semantic ID  (+ optional known-disease IDs as context)
   OUTPUT : autoregressively generate disease semantic ID(s) → decode to disease
   Beam search over the code tree returns a ranked disease candidate list.
```
- **Cold-start (W1):** a never-seen drug → encode its SMILES → RQ-VAE → instant semantic ID → generate candidates. No retraining, no node in any adjacency matrix. (This works precisely *because* SMILES are clean and unique — 269/269, 662/663, 592/593 across B/C/F.)
- **Scaling (W6):** inference is sequence generation; the model never materializes a 1888×1888 matrix.
- **Interpretability (W7):** shared code prefixes = shared chemotype/ontology branch → a semantic, inspectable hierarchy.

### Drawable architecture

Two diagrams: **(A) RQ-VAE tokenizer** (offline, run once per entity type) and **(B) generative encoder-decoder** (trained on drug→disease pairs).

**(A) Tokenizer boxes:**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| T1 | Content encoder | ChemBERTa(768) or ECFP4(2048)→MLP | drug → `z ∈ ℝ^{256}` | per entity type |
| T2 | RQ encoder | MLP | `768/2048` → `z ∈ ℝ^{256}` | `→256` |
| T3 | Residual quantizer | 3 codebooks `C₁,C₂,C₃ ∈ ℝ^{256×256}` | `z` → SID `(c₁,c₂,c₃) ∈ {0..255}³` | 3 levels × 256 codes |
| T4 | RQ decoder | MLP | `q₁+q₂+q₃ (256)` → `768/2048` | reconstruction |

```
(A) TOKENIZER (per entity, offline):
 SMILES ─►[T1 ChemBERTa 768]─►[T2 MLP→256]─► z(256)
                                              │
              ┌── q₁=NN(z,C₁),  r₁=z−q₁ ──────┤
              ├── q₂=NN(r₁,C₂), r₂=r₁−q₂ ──────┤   (residual quantization)
              └── q₃=NN(r₂,C₃) ───────────────┘
                                              ▼
                       SID = (c₁,c₂,c₃)   and   q=q₁+q₂+q₃ ─►[T4 MLP→768]─► x̂
              L_tok = ‖x − x̂‖²  +  β·Σ_l ‖ rₗ₋₁ − sg(qₗ) ‖²   (commitment)
```
Repeat for disease (MeSH→768) and protein (ESM→768). Output: a lookup table `entity → (c₁,c₂,c₃)` and the inverse `SID → entity`.

**(B) Generative model boxes:**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| G1 | Token embedding | Embedding | `token_id` → `ℝ^{256}` | vocab ≈ 3×256×(types)+specials |
| G2 | Encoder | Transformer ×4 | drug SID seq `(≤6 tok)` → memory `ℝ^{L×256}` | 6 heads, FFN 1024 |
| G3 | Decoder | Transformer ×4 + cross-attn | shifted disease SID → `ℝ^{3×256}` | causal mask |
| G4 | Level heads | 3 × Linear | `256` → `256-way softmax` per level | one head per code level |

```
(B) GENERATIVE RETRIEVAL (per training pair drug→disease):
 drug SID (c₁,c₂,c₃) [+optional known-disease SIDs as history]
        │
        ▼
   [G1 TokEmbed] ─► [G2 Encoder ×4] ─► memory (L×256)
                                          │ cross-attn
 disease SID (shifted right) ─►[G1]─►[G3 Decoder ×4]─►[G4 head₁]─►P(s₁)
                                                     ─►[G4 head₂]─►P(s₂|s₁)
                                                     ─►[G4 head₃]─►P(s₃|s₁,s₂)
        L_gen = CE(s₁)+CE(s₂)+CE(s₃)
 INFER: beam search (beam=20) over 3 steps ─► top disease SIDs ─► inverse table ─► ranked diseases
```

**Concrete hyper-parameters:** codebooks `3 × 256` (so ≤ 256³ ≈ 16.7M addressable entities — far above n_S=598); `d_model=256`, 4+4 layers, 6 heads, FFN=1024; cold-start = run (A) on a new drug's SMILES, then (B) generates. Add a 4th "disambiguation" token if two entities collide on the same `(c₁,c₂,c₃)`.

### Leakage guard
Codebooks are fit on content features only (SMILES-encoder / MeSH / ESM — **not** the association matrix). The Transformer is trained on **train-fold** drug→disease ID pairs; test pairs withheld. Cold-start evaluation uses the inductive split (drugs absent from training). One caveat to watch: because mol2vec is degenerate, do **not** fall back to it as a tokenizer input even for ablations — it would silently merge drugs and corrupt the cold-start metric.

### Novelty Audit
- **vs DR: ~3%** (only "uses content features" overlaps). No DR method tokenizes entities or does autoregressive generation.
- **vs RecSys: ~80%** (this *is* TIGER, re-instantiated with chemical/biological tokenizers and a drug→disease generation target).

---

## Proposal 3 — **HypoDR**: Disentangled **Hyperbolic** Mechanism-of-Action Factors

**Targets:** W7 (entangled embeddings), W5 (over-smoothing), + native modeling of disease ontology hierarchy.
**Transfers from RecSys:** DHCF / GDCF / Intent-Disentangled Graph Contrastive Learning / Hyperbolic Diffusion Rec — *split a user into K intent-specific sub-embeddings, each living in its own hyperbolic space.*

### The core re-framing
A drug treats different diseases through different **mechanisms of action** (MoA) — exactly analogous to RecSys "user intents." Existing DR jams all MoAs into one Euclidean vector (W7). Two upgrades from RecSys:
1. **Disentanglement** — represent each drug/disease as `K` MoA-specific sub-vectors; a routing weight decides which MoA explains a given pair → built-in interpretability.
2. **Hyperbolic geometry** — the **MeSH disease ontology is a tree**, and the drug–protein–disease graph is scale-free/hierarchical. Poincaré-ball embeddings have *exponential* capacity for trees, so low-degree leaf diseases are no longer crushed near hubs → directly mitigates over-smoothing (W5).

> **Data note (§0.5):** the disease MeSH features (`DiseaseFeature.csv`, 570/598 unique) provide a real ontology signal and are well-suited to the hyperbolic prior — impute the 29 all-zero rows first (k-NN by `DiseasePS`). The **drug** channels must be initialized from a **SMILES encoder**, not mol2vec. Protein channels use clean ESM-2. The hierarchy prior can be strengthened by mapping each disease *name* (available in `DiseaseFeature.csv` row labels and `Allnode.csv`) to its true MeSH tree depth.

### Architecture
```
Per node, K disentangled channels:   h = [h⁽¹⁾, …, h⁽ᴷ⁾],  each h⁽ᵏ⁾ ∈ Poincaré ball 𝔻^{d/K}
Channel-k propagation:  hyperbolic GCN (Möbius add + exp/log maps) on a
                        channel-specific neighbor weighting (intent-aware DGCL gating)
Pair score:   s(d,s) = Σₖ  ρₖ(d,s) · ( −d_𝔻( h_d⁽ᵏ⁾ , h_s⁽ᵏ⁾ ) )      # neg. hyperbolic distance
              ρₖ = softmax routing over MoA channels  → which mechanism explains this pair
Disentangle regularizer: minimize cross-channel correlation (independence of MoAs)
```
- Output `ρₖ(d,s)` is an **MoA attribution**: "drug d is predicted to treat disease s mainly via mechanism k" — a clinician-readable hypothesis.

### Drawable architecture

**Design choice:** `K=4` mechanism channels, each a Poincaré ball `𝔻^{d_k}` with `d_k = d/K = 64`, curvature `c` (learnable). `expmap₀ / logmap₀` move between Euclidean tangent space and the ball.

**Boxes (modules):**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| H1 | Content encoders | shared `ENC_*` (§0.6) | → `X ∈ ℝ^{N×d}` | Euclidean |
| H2 | Channel split | reshape | `X (N×d)` → `K × (N×64)` | K=4 |
| H3 | Lift to ball | `expmap₀` | `(N×64)` per channel → `𝔻^{64}` | curvature `c` |
| H4 | Hyperbolic GCN | 2 layers/channel, channel-gated | `𝔻^{64}` → `𝔻^{64}` | Möbius agg + edge gate MLP |
| H5 | Routing net `ρ_k` | MLP + softmax over K | per pair: `K` distances → `ρ ∈ Δ^{K}` | `K→K` |
| H6 | Scorer | weighted neg-distance | `(ρ, dists)` → `s ∈ ℝ` | no params |

**Wiring:**
```
 X (N×d) ─►[H2 split K=4]─► X⁽ᵏ⁾ (N×64)  ─►[H3 expmap₀]─► h⁽ᵏ⁾ ∈ 𝔻^64     (k=1..4)
                                                  │
 fold-masked graph ─►[H4 Hyp-GCN ×2, per-channel edge gating]─► refined h_d⁽ᵏ⁾, h_s⁽ᵏ⁾ ∈ 𝔻^64
                                                  │
 pair (d,s):  dₖ = d_𝔻( h_d⁽ᵏ⁾ , h_s⁽ᵏ⁾ )  for k=1..4   (4 hyperbolic distances)
                                                  │
              [H5 routing MLP → softmax] ─► ρ₁..ρ₄     (MoA attribution, interpretable)
                                                  ▼
              [H6] score s(d,s) = Σₖ ρₖ · ( − dₖ )
 L = BPR(s) + λ_disc·Σ_{k≠k'} corr(h⁽ᵏ⁾,h⁽ᵏ'⁾) + λ_cl·Σ_k InfoNCE_k(sim-graph)
```

**Per-channel Hyp-GCN layer (draw as an inset):**
```
h⁽ᵏ⁾∈𝔻 ─►[logmap₀]─► tangent ─►[edge-gate αᵢⱼ⁽ᵏ⁾ = softmax(MLP)]─► Σⱼ αᵢⱼ·hⱼ ─►[expmap₀]─►[Möbius ⊕ bias]─► σ
```

**Concrete hyper-parameters:** `K=4`, `d_k=64`, 2 hyperbolic layers, curvature `c=1.0` (learnable), `λ_disc=1e-2`, `λ_cl=1e-4`. The MoA count `K` is the key knob — try `K∈{2,4,8}`.

### Loss
`L = BPR/BCE(s)` + `λ_disc · DisentanglementLoss` + `λ_cl · intent-contrastive (per channel)`.

### Leakage guard
Ontology + similarity are content-derived. Hyperbolic GCN runs on the **fold-masked** graph. Routing uses only train edges.

### Novelty Audit
- **vs DR: ~10%** (shares the "multi-view/semantic attention fusion" spirit of GCGB/RGLDR, but the math is entirely different — hyperbolic, disentangled, distance-based scoring vs Euclidean attention).
- **vs RecSys: ~65%** (DHCF/GDCF disentangled-hyperbolic CF, re-cast with MoA channels and ontology priors).

---

## Proposal 4 — **CausalDR**: Counterfactual Debiasing of Research-Popularity

**Targets:** W3 (popularity bias) — and crucially the **evaluation inflation** the parent HANDOFF keeps fighting.
**Transfers from RecSys:** PPAC / counterfactual inference / Inverse Propensity Weighting / MACR — *separate the popularity "direct effect" from the genuine match, and subtract it at inference.*

### The core re-framing
A known drug–disease edge exists partly because the biology fits and partly because the drug was **heavily studied** (aspirin, metformin). That is *identical* to popularity bias in RecSys, where blockbuster items get clicks regardless of fit. Existing DR ignores this and so (a) over-recommends hubs and (b) inflates AUROC. We import the RecSys causal toolkit.

### Architecture (Structural Causal Model)
```
Match path  :  M = f_match(h_d, h_s)               # the biology we WANT
Popularity  :  P_d = g(deg_d),  P_s = g(deg_s)     # research attention nuisance
Observed    :  Ŷ = σ( M  +  γ_d·P_d  +  γ_s·P_s )  # training fits the biased world
Counterfactual inference (deploy):
   TE  = effect with real popularity
   NDE = effect of popularity alone (set M to reference)
   Debiased score  =  TE − NDE   →   "what if every drug had equal research attention?"
Training reweight:  IPW with propensity ∝ node degree (down-weight hub edges)
```

### Drawable architecture

**Boxes (modules):**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| C1 | Base encoder | any (LightGCN/MPHAM) on masked graph | → `h_d, h_s ∈ ℝ^{d}` | swappable trunk |
| C2 | Match head `f_match` | 4-way concat + MLP | `[h_d‖h_s‖h_d⊙h_s‖rotate] (4d)` → `M ∈ ℝ` | `4d→128→1` |
| C3 | Drug-popularity head `g_d` | MLP on degree | `deg_d (1)` → `P_d ∈ ℝ` | `1→16→1`, log-deg input |
| C4 | Disease-popularity head `g_s` | MLP on degree | `deg_s (1)` → `P_s ∈ ℝ` | `1→16→1` |
| C5 | Fusion (train) | learnable scalars | `M, P_d, P_s` → `Ŷ` | `γ_d, γ_s` |
| C6 | Counterfactual decode (deploy) | subtraction | `M, P*` → debiased score | reference `P*` |

**Wiring:**
```
                                  ┌─────────────── TRAIN (fit the biased world) ──────────────┐
 graph(masked)─►[C1 encoder]─►h_d,h_s ─►[C2 match head 4d→1]─► M ───────────────────►(+)      │
 deg_d ─►[C3 pop head]─► P_d ──────────────────────────────────────────►(×γ_d)─────►(+)      │
 deg_s ─►[C4 pop head]─► P_s ──────────────────────────────────────────►(×γ_s)─────►(+)      │
                                                                                     ▼        │
                                          Ŷ = σ( M + γ_d·P_d + γ_s·P_s )                      │
                                          L = IPW-weighted BCE,  w = (1/deg)^η (normalised)    │
                                  └──────────────────────────────────────────────────────────┘

                                  ┌─────────────── DEPLOY (remove popularity) ────────────────┐
                                    debiased score = TE − NDE  =  M   (popularity set to ref)   │
                                    eval: overall AUROC  +  AUROC on bottom-50%-degree drugs     │
                                  └──────────────────────────────────────────────────────────┘
```

**Concrete hyper-parameters:** `d=256`; `γ_d,γ_s` init 1.0 (learnable); IPW exponent `η∈{0.5,1.0}`; reference `P*` = mean popularity logit over train. C2 reuses the RotatE 4-way decoder so this composes cleanly on top of any other proposal's encoder.

### Why this is the *honest* proposal
It does not chase a higher number — it **attacks the inflation** the project already worries about ("AUC > 0.93 honest = suspect"). A popularity-debiased AUROC on **long-tail drugs** is a more trustworthy metric than overall AUROC. Add a **stratified eval**: report AUROC on the bottom-50% degree drugs separately.

### Leakage guard
Degrees computed on **train-fold** graph only. Counterfactual subtraction is inference-time and uses no labels.

### Novelty Audit
- **vs DR: ~5%** (only the base encoder is DR-like; the causal SCM, IPW, and counterfactual decoding are absent from all DR papers).
- **vs RecSys: ~70%** (PPAC/MACR counterfactual debiasing, re-derived with degree-as-popularity for biological graphs).

---

## Proposal 5 — **MoMoE-DR**: Sparse **Mixture-of-Mechanism-Experts** + Multi-Dataset Transfer

**Targets:** W8 (gradient conflict), W4 (sparsity via cross-dataset transfer), W5 (capacity vs smoothing).
**Transfers from RecSys:** M3oE / MoME / Self-Supervised MoE for Multi-Behavior / Frequency-MoHE — *sparse expert routing where each behavior/domain activates specialized experts, sharing some and isolating others.*

### The core re-framing
GCGB's gradient-balance hack (W8) exists because one shared trunk must serve many meta-path "behaviors" with conflicting gradients. RecSys solved this with **sparse MoE**: give each behavior its own experts, let a gate route per node, and conflicts vanish because experts specialize. Two transfers:
1. **Meta-path = behavior** → each meta-path (RDR, RPR, DPD…) routes to a small expert pool; a per-node gate picks top-k. Conflicting gradients land on *different* experts (W8 solved without a custom optimizer).
2. **Dataset = domain** (M3oE multi-domain) → **shared experts across B / C / F datasets** + dataset-private experts. The dense B-dataset (11.45%) donates representation power to the starved C/F datasets (≈1%) — a transfer-learning cure for W4 that no DR method attempts.

> **Feasibility confirmed by §0.5:** disease features are **64-dim** and protein features are **320-dim in *all three* datasets**, and a SMILES encoder yields a common drug space — so shared experts need **no dimension adapters**. Use the same SMILES→encoder pipeline per dataset (mol2vec is degenerate and must not be the shared drug space). C-dataset's pre-built 10-fold splits give a clean transfer-evaluation harness.

### Architecture
```
Per node embedding h →  Gate(h) → top-k of {E₁…E_N} experts (shared) ∪ {private experts}
Meta-path m output:    y_m = Σ_{e∈topk} g_e · E_e(h ; A_m)        # routed graph experts
Fuse meta-paths:       distance-level attention (the ONE part kept from MPHAM)
Cold-expert (SSL):     an "unvisited-pair" expert trained by generative SSL for W1 cold-start
Cross-dataset:         shared experts updated on B∪C∪F; gate is dataset-conditioned
```
- Load-balancing loss (Switch-Transformer style) keeps experts utilized.
- Sparsity → only top-k experts fire → **scales better than dense GCGB** (helps W6 too).

### Drawable architecture

**Design choice:** expert pool = `8 shared` (trained on B∪C∪F) `+ 2 private` per dataset = `10` experts visible to each dataset. Each expert is one GAT layer `d→d`. Per-node gate selects `top-k=2`.

**Boxes (modules):**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| E1 | Content encoders | shared `ENC_*` (§0.6) | → `X ∈ ℝ^{N×d}` | — |
| E2 | Gating network | MLP + top-k softmax | `h (N×d)` → weights over 10 experts | `d→10`, top-2 |
| E3 | Expert pool | 8 shared + 2 private GAT experts | `(h, A_m)` → `ℝ^{N×d}` | each GAT `d→d` |
| E4 | Per-meta-path route | weighted sum of top-k experts | → `y_m ∈ ℝ^{N×d}` | 15 meta-paths |
| E5 | Distance-level attention | **(kept from MPHAM)** | `{y_m}` grouped by dist → `h_final ∈ ℝ^{N×d}` | 3 distance groups |
| E6 | Cold-start SSL expert | generative reconstruction head | masked content → content | aux task |
| E7 | RotatE 4-way decoder | concat + MLP | `[h_d‖h_s‖⊙‖rotate] (4d)` → `score` | `4d→128→1` |

**Wiring:**
```
 X (N×d)
   │
   ├──────────── for each meta-path A_m  (m = 1..15) ─────────────┐
   │   h ─►[E2 Gate → top-2 of 10]─► g_e                          │
   │           experts: [E3]  E₁..E₈ shared (B∪C∪F)  +  E₉,E₁₀ private(dataset)
   │   y_m = Σ_{e∈top2} g_e · E_e(h ; A_m)   ◄── [E4]             │
   └──────────────────────────────────────────────────────────────┘
   │  group {y_m} by distance (1/2/3)
   ▼
 [E5 distance-level attention] ─► h_final (n_R×d, n_S×d)
   │
   ▼
 [E7 RotatE 4-way decoder] ─► score
 L = BCE + α·L_loadbalance(Switch) + β·L_SSL([E6] cold-start expert)

 Dataset routing: gate is dataset-conditioned (one-hot dataset id concatenated to h before E2),
 so B/C/F share E₁..E₈ but pick different private experts E₉,E₁₀.
```

**Concrete hyper-parameters:** `d=256`; experts = 8 shared + 2 private; `top-k=2`; load-balance weight `α=1e-2`; SSL weight `β=0.1`; 15 meta-paths (same set as MPHAM). Only 2 of 10 experts fire per node → ~5× cheaper than evaluating all experts densely.

### Leakage guard
Per-fold masking unchanged; cross-dataset sharing uses *other datasets'* edges (no within-dataset test leakage). Validate that B→C transfer is tested with C's test fold fully masked.

### Novelty Audit
- **vs DR: ~12%** (keeps a single distance-level attention fuser from MPHAM; everything else — sparse routing, expert pools, multi-domain sharing, load balancing — is new to DR).
- **vs RecSys: ~60%** (M3oE/MoME routing and multi-domain experts, re-targeted to meta-paths and the B/C/F dataset family).

---

## Proposal 6 — **NoiseDR**: Ultra-Cheap Noise-Perturbation Contrastive + Long-Tail Diffusion Augmentation

**Targets:** W4 (sparsity), W3 (long-tail nodes), and the *cost* of GCGB's heavy view construction.
**Transfers from RecSys:** XSimGCL / SimGCL / Long-tail Augmented GCL / Adaptive Diffusion Augmentation — *forget expensive graph augmentation; just add uniform noise in embedding space for contrastive views, and synthesize embeddings for tail nodes.*

### The core re-framing
GCGB builds two explicit graph views (sim-view, ass-view) and contrasts them — expensive and the source of its gradient-conflict pain. RecSys discovered (SimGCL → XSimGCL) that **adding tiny uniform noise to embeddings** yields contrastive views that work *better* than structural augmentation, with one line of code and almost no hyperparameters. Plus, **long-tail GCL** specifically up-weights low-degree nodes, the exact W3/W4 victims.

### Architecture
```
Encoder: any MPHAM-style backbone → h
View 1:  h + Δ₁,   View 2: h + Δ₂      with  Δ = sign(h) ⊙ U(0,ε)     # XSimGCL noise
L_cl  :  InfoNCE(View1, View2)  with degree-aware temperature τ(deg)   # long-tail boost
Tail augmentation:  a small diffusion head synthesizes plausible embeddings for
                    drugs/diseases with < m known edges → densifies the tail
```
- Degree-aware temperature: low-degree nodes get sharper contrast → stronger gradient where data is scarce (W3/W4).
- Essentially **free** (no extra graph passes), so it composes on top of *any* other proposal (1–5) as a plug-in regularizer.

### Drawable architecture

**Boxes (modules):**

| # | Module | Type | Input → Output | Key params |
|---|---|---|---|---|
| P1 | Backbone encoder | any (MPHAM/LightGCN) | masked graph → `h ∈ ℝ^{(n_R+n_S)×d}` | swappable |
| P2 | Noise view generator | additive uniform noise | `h` → `h̃₁, h̃₂` | `Δ = sign(h)⊙U(0,ε)`, ε=0.1 |
| P3 | Projection head (opt.) | MLP | `h̃ (d)` → `z (d)` | for CL space |
| P4 | Degree-aware InfoNCE | contrastive loss | `z₁, z₂, deg` → `L_cl` | `τ(deg)` |
| P5 | Tail diffusion aug (opt.) | small cond. diffusion | content of deg<m node → synth `h⁺` | extra positive |
| P6 | Main decoder | RotatE/element-wise + MLP | `h_d, h_s` → `score` | BCE |

**Wiring:**
```
 graph(masked) ─►[P1 encoder]─► h (n_R+n_S × d)
        │
        ├─( + Δ₁ )─► h̃₁ ─►[P3 proj]─► z₁ ─┐
        ├─( + Δ₂ )─► h̃₂ ─►[P3 proj]─► z₂ ─┤─►[P4 InfoNCE, τ(deg)] ─► L_cl
        │                                  │     τ(deg)=τ₀·(1+λ/log(deg+e))  (low-deg ⇒ sharper)
        │   [P5] deg<m nodes: content ─► tiny diffusion ─► h⁺ (extra positive in P4)
        │
        └─────────────────────────────────►[P6 decoder]─► score ─► L_BCE

 L = L_BCE + λ_cl · L_cl
```

**Concrete hyper-parameters:** noise `ε=0.1`; `τ₀=0.2`, degree term `λ=0.5`; `λ_cl=1e-1` (XSimGCL uses a larger CL weight than GCGB's 1e-4 because the views are cheap/aligned); tail threshold `m=5` edges. This is the smallest proposal — `P2`+`P4` are ~10 lines and bolt onto the current MPHAM encoder.

### Leakage guard
Noise is label-free; contrastive supervision derives from embeddings of the **train-fold** graph; tail synthesis conditions on content only.

### Novelty Audit
- **vs DR: ~12%** (contrastive learning exists in GCGB, but GCGB uses structural views + custom gradient balance; the noise-perturbation recipe and degree-aware temperature are RecSys-native and unused in DR).
- **vs RecSys: ~75%** (direct XSimGCL + long-tail GCL transfer).

---

## Part II — Multi-Modal & Biological-Knowledge Proposals (the teacher's direction)

> **Why a Part II.** The 6 proposals above attack the *learning-paradigm / sparsity* axis (how we train: diffusion, generative retrieval, MoE, causal, hyperbolic, contrastive). Your teacher names a **different, orthogonal axis** — the *representation / modality* axis: drug **1D (SMILES) / 2D (molecular graph) / 3D (conformer)**, protein **1D (sequence) / 3D (AlphaFold)**, and **external biological networks (KEGG, STRING)** to fight sparsity at the *data* level. These three new proposals each realize one of the teacher's sub-points, and each is still inherited from a **current RecSys SOTA family** (multi-modal recommendation; knowledge-graph-enhanced recommendation) so the novelty rule holds.

### What we can derive from the data we already have (no new downloads of features — just standard tools/DBs)

| Modality | Source in repo | Tool / DB (keyed by an ID we have) | Output |
|---|---|---|---|
| Drug **1D** | SMILES (`DrugInformation.csv`) | ChemBERTa / MolFormer | 768-d |
| Drug **2D** | SMILES → RDKit mol graph | GIN / MPNN (atoms=nodes, bonds=edges) | `d` |
| Drug **3D** | SMILES → RDKit ETKDG conformer | EGNN / SchNet (E(3)-invariant) | `d` |
| Protein **1D** | sequence (`ProteinInformation.csv`) | ESM-2 (already have, 320-d) | 320-d |
| Protein **3D** | **UniProt ID** (`ProteinID.csv`, e.g. `P22303`) → AlphaFold DB `.pdb` | GearNet / SE(3)-GNN on Cα k-NN graph | `d` |
| Disease | MeSH (`DiseaseFeature.csv`) + name | MLP / ontology depth | 64-d |
| Protein–Protein | UniProt ID → **STRING-db** (conf > 0.7) | adds PPI edges | dense PPI graph |
| Protein–Pathway | UniProt → gene → **KEGG** | adds membership edges | bipartite |

All three proposals below are buildable **offline + free public DBs**; nothing depends on the broken mol2vec.

---

## Proposal 7 — **M³-DR**: Tri-Modal Drug + Bi-Modal Protein fusion via Modality-MoE

**Targets:** W1 (cold-start), W4 (sparsity — richer per-node features), + modality robustness.
**Transfers from RecSys:** **Multi-modal recommendation** — MAMEX (multi-modal Mixture-of-Experts for cold-start), FREEDOM (freeze the modality similarity graph), BM3 (dropout-contrastive, no negative sampling). **Bio side:** MolMix (SMILES + 2D + 3D molecular encoders).

### Core re-framing
A drug is not a 269-dim similarity row — it is a *molecule* with three views (1D/2D/3D), and a protein has two (1D/3D). Multi-modal RecSys treats each item as a bundle of modalities and learns a **gated fusion** that decides *which modality matters for which entity*. We import that wholesale: each modality gets its own encoder; a **modality-MoE gate** fuses them; the fused content seeds a light graph model. Cold-start works because everything is content-derived.

### Drawable architecture

**Boxes (modules):**

| # | Module | Type | Input → Output | Notes |
|---|---|---|---|---|
| A1 | Drug-1D encoder | ChemBERTa | SMILES → `ℝ^{n_R×768}` → MLP→`d` | frozen LM optional |
| A2 | Drug-2D encoder | GIN/MPNN | RDKit mol graph → `ℝ^{n_R×d}` | atoms/bonds |
| A3 | Drug-3D encoder | EGNN (E(3)-invariant) | ETKDG conformer → `ℝ^{n_R×d}` | rotation-invariant |
| A4 | Protein-1D encoder | ESM-2 + MLP | 320 → `ℝ^{n_P×d}` | clean signal |
| A5 | Protein-3D encoder | SE(3)-GNN/GearNet | AlphaFold Cα graph → `ℝ^{n_P×d}` | by UniProt |
| A6 | Disease encoder | MLP | MeSH 64 → `ℝ^{n_S×d}` | impute zeros |
| A7 | **Modality-MoE gate** | per-entity gate over modalities | stack of modality vecs → fused `z` | MAMEX-style top-k |
| A8 | Graph refiner | LightGCN/MPHAM on masked D–S–P graph | `z` → `h` | content-seeded |
| A9 | Decoder | RotatE 4-way | `h_d,h_s` → score | — |

**Wiring:**
```
 DRUG:    SMILES ─►[A1 1D]─┐
                  RDKit2D ─►[A2 2D]─┤
                  RDKit3D ─►[A3 3D]─┤─►[A7 Modality-MoE gate]─► z_R (n_R×d)
 PROTEIN: ESM   ─►[A4 1D]─┐         │
                 AlphaFold►[A5 3D]─┤─►[A7 gate]─► z_P (n_P×d)
 DISEASE: MeSH  ─►[A6]──────────────► z_S (n_S×d)
                                         │
            z = [z_R; z_P; z_S] ─►[A8 graph refiner on masked graph]─► h (N×d)
                                         │
                                  [A9 RotatE decoder]─► score
 SSL (BM3): two dropout views of each modality ─► intra/inter-modality alignment loss (no neg sampling)
 L = BCE + λ_align · L_BM3
```

**Concrete:** `d=256`; modality-MoE top-k=2 of {1D,2D,3D}; BM3 dropout p=0.3; freeze the drug 2D/3D similarity graph (FREEDOM) for stability. Ablation lever: turn modalities on/off to measure each one's lift.

### Leakage guard
Every modality is content/structure-derived (SMILES, RDKit, ESM, AlphaFold) — **independent of the drug–disease label**. Graph refiner runs on the fold-masked graph. No GIP.

### Novelty Audit
- **vs DR: ~12%** (shares "encode content + light GNN + RotatE decoder"; but tri-modal drug + AlphaFold protein + modality-MoE fusion is new to DR).
- **vs RecSys: ~70%** (MAMEX/FREEDOM/BM3 multi-modal recommendation, re-instantiated with molecular/structural modalities).

---

## Proposal 8 — **BioKG-DR**: Knowledge-Graph-Enhanced DR with KEGG + STRING (densify the sparsity)

**Targets:** W4 (sparsity — *the teacher's central point*), W3 (popularity), W7 (pathway-level interpretability).
**Transfers from RecSys:** **Knowledge-graph-enhanced recommendation** — KGCL (KG contrastive denoising), KGRec (KG rationalization via masked-encoder), KGAT (relation-aware attention).

### Core re-framing
The drug–disease matrix is sparse, but biology is **not**: STRING has ~hundreds of thousands of protein–protein edges, KEGG groups proteins into pathways. RecSys solved sparse user–item data the same way — by attaching a **side-information knowledge graph** (item attributes, relations) and propagating over it. We attach an **external biological KG** so a drug and a disease that share *no* direct path in the sparse matrix become connected through `drug→protein–(STRING)–protein–(KEGG pathway)–protein→disease`. KGCL denoises the (noisy) STRING edges; KGRec surfaces the *pathway rationale* explaining each prediction.

### Drawable architecture

**The augmented heterogeneous KG (draw this first):**
```
 node types:  Drug, Protein, Disease, Pathway(KEGG), [optional GO term]
 edges:
   Drug —target→ Protein        (have: DrugProteinAssociation)
   Protein —assoc→ Disease       (have: ProteinDiseaseAssociation)
   Protein —PPI→ Protein         (NEW: STRING, confidence>0.7)        ◄── densifies
   Protein —member→ Pathway      (NEW: KEGG)                           ◄── densifies
   Drug —sim→ Drug               (ECFP similarity)
   Drug —treats→ Disease         (TARGET; fold-masked at train/eval)
```

**Boxes (modules):**

| # | Module | Type | Input → Output | Notes |
|---|---|---|---|---|
| K1 | Content init | shared `ENC_*` (§0.6) | → `X` per node type | SMILES/ESM/MeSH |
| K2 | KG encoder | KGAT / R-GCN (relation-aware) | KG + `X` → `h (N'×d)` | N' includes pathways |
| K3 | **KG denoiser + contrastive** | KGCL: learn edge reliability, 2 views | `h` → `h_robust`, `L_kgcl` | suppress STRING noise |
| K4 | **KG rationalizer** | KGRec: mask triplets, reconstruct, score | → rationale weights, `L_rat` | pathway attribution |
| K5 | Decoder | RotatE 4-way on drug/disease nodes | `h_d,h_s` → score | — |

**Wiring:**
```
 STRING PPI + KEGG pathways + drug/protein/disease assoc ─► augmented KG
                                   │
 content X (SMILES/ESM/MeSH) ─►[K2 KGAT relation-aware GNN]─► h
                                   │
                             [K3 KGCL denoise + cross-view CL]─► h_robust  (+ L_kgcl)
                                   │
                             [K4 KGRec mask-reconstruct]──────► pathway rationale (+ L_rat)
                                   │
                             [K5 RotatE decoder]─► score
 L = BCE + λ1·L_kgcl + λ2·L_rat
 OUTPUT EXTRA: top rationale path, e.g. "drug→EGFR–(STRING)–MAPK1–(KEGG hsa04010)–→disease"
```

### Leakage guard
STRING/KEGG are **external biology, independent of the drug–disease labels** → not leakage (same status as content features). The `Drug—treats—Disease` edges are still strictly fold-masked from the KG during training/eval. Build the KG once; mask only the target relation per fold.

### Novelty Audit
- **vs DR: ~13%** (DR uses drug/protein/disease, but importing STRING PPI + KEGG pathways as a denoised side-info KG with KG-contrastive + rationalization is new; closest DR cousin is KGRDR, still <15%).
- **vs RecSys: ~65%** (KGCL + KGRec knowledge-graph-enhanced recommendation, re-targeted to a biological KG).

---

## Proposal 9 — **GeoBind-DR**: 3D Structure-Aware Binding Prior (drug conformer × AlphaFold pocket)

**Targets:** W1 (cold-start), W2 (a physics prior reduces reliance on label-defined negatives), + binding-pose interpretability.
**Transfers from RecSys:** the **two-tower retrieval + multimodal alignment** pattern (item-tower / user-tower, align in a shared space). **Bio side:** Generalist Equivariant Transformer / E(3)-equivariant 3D molecular interaction learning.

### Core re-framing
Two-tower RecSys learns a user-tower and item-tower and scores by alignment in a shared space. Here the two towers are **geometric**: a drug-conformer tower and a protein-pocket tower (AlphaFold). Their alignment is a learned **binding compatibility** `b(drug, protein)` — a *physically grounded* signal that exists even for a brand-new drug (cold-start) and does not depend on association-label negatives. Propagate `drug→protein(binding)→disease` to get a structure-grounded drug–disease prior, then fuse it with a recommender score.

### Drawable architecture

**Boxes (modules):**

| # | Module | Type | Input → Output | Notes |
|---|---|---|---|---|
| G1 | Drug-conformer tower | EGNN (E(3)-invariant) | RDKit 3D conformer → `ℝ^{n_R×d}` | rotation/translation-inv |
| G2 | Protein-pocket tower | SE(3)-GNN on AlphaFold pocket | residue graph → `ℝ^{n_P×d}` | by UniProt |
| G3 | **Binding-compat head** | equivariant interaction / bilinear | `(z_drug, z_prot)` → `b ∈ [0,1]` | the "alignment" |
| G4 | Structure prior propagate | `b · (protein→disease)` aggregation | → `s_struct(drug,disease)` | label-free prior |
| G5 | Recommender score | any (Prop 7/8 encoder) | → `s_rec(drug,disease)` | learned |
| G6 | Fusion | gated sum | `α·s_struct + (1-α)·s_rec` | α learnable |

**Wiring:**
```
 drug 3D conformer ─►[G1 EGNN]─► z_drug (n_R×d) ─┐
 AlphaFold pocket  ─►[G2 SE(3)]─► z_prot (n_P×d)─┤
                                                 ├─►[G3 binding-compat]─► b(drug,protein) ∈ [0,1]
                                                 │
   b ⊗ (Protein—assoc—Disease) ─►[G4 propagate]─► s_struct(drug,disease)   (physics prior, label-free)
                                                 │
   [G5 recommender (Prop 7/8)] ─► s_rec ─────────┤
                                                 ▼
                              [G6 gated fusion]─► final score = α·s_struct + (1-α)·s_rec
 (optional) pre-train G1–G3 on known drug–target binding (BindingDB) ─► transfer to cold-start drugs
```

### Leakage guard
3D structures (RDKit, AlphaFold) and drug–target binding are independent of drug–disease labels. `s_struct` uses only `drug→protein` (binding) and `protein→disease` (fold-masked for the target relation). Pre-training on BindingDB uses no B/C/F drug–disease labels.

### Novelty Audit
- **vs DR: ~8%** (DR uses proteins as nodes, but a 3D-equivariant binding tower as a label-free structural prior is essentially absent).
- **vs RecSys: ~55%** (two-tower retrieval + multimodal alignment skeleton; the geometric towers are from structural biology, the allowed "DR/bio SOTA" side).

---

## 7. Summary Matrix

| Proposal | RecSys Source | DR Weaknesses Solved | Cold-start (W1) | Honest-eval friendly | Novelty vs DR |
|----------|---------------|----------------------|:---:|:---:|:---:|
| **1. DiffuDR** | DiffRec / DiffuRec | W2, W3, W4 | partial | ✅ (calibrated dist.) | ~5% |
| **2. SemDR** | TIGER / RQ-VAE | W1, W6, W7 | ✅ native | ✅ (inductive split) | ~3% |
| **3. HypoDR** | DHCF / GDCF (hyperbolic) | W5, W7 | — | ✅ | ~10% |
| **4. CausalDR** | PPAC / IPW / MACR | W3 + inflation | — | ✅✅ (de-inflates) | ~5% |
| **5. MoMoE-DR** | M3oE / MoME | W4, W5, W8, W6 | ✅ (SSL expert) | ✅ | ~12% |
| **6. NoiseDR** | XSimGCL / LT-GCL | W3, W4 | — | ✅ | ~12% |
| **7. M³-DR** | MAMEX / FREEDOM / BM3 (multi-modal rec) | W1, W4 | ✅ native | ✅ | ~12% |
| **8. BioKG-DR** | KGCL / KGRec (KG-enhanced rec) | W4, W3, W7 | partial | ✅ | ~13% |
| **9. GeoBind-DR** | two-tower + E(3) interaction | W1, W2 | ✅ native | ✅ | ~8% |

**Two axes (this is the key takeaway for your teacher):**
- **Axis 1 — learning paradigm / sparsity (Proposals 1–6):** *how* we train on the sparse matrix (diffusion, generative retrieval, hyperbolic, causal, MoE, contrastive). ← what we had.
- **Axis 2 — representation / biological knowledge (Proposals 7–9):** *what* we feed the model (drug 1D/2D/3D, protein 1D/3D AlphaFold, KEGG/STRING networks). ← the teacher's direction.
The strongest single project combines **one method from each axis** (e.g. `BioKG-DR` data + `MoMoE-DR` training, or `M³-DR` features + `NoiseDR` contrastive).

### Recommended build order (ROI vs effort)
1. **NoiseDR** (Prop 6) — one-line plug-in, drops onto current MPHAM, immediate W4 relief. *Lowest effort.*
2. **CausalDR** (Prop 4) — re-frames evaluation honestly; small SCM head on the existing encoder.
3. **MoMoE-DR** (Prop 5) — biggest single architectural leap; unlocks B→C/F transfer.
4. **HypoDR** (Prop 3) — interpretability + ontology fit; needs hyperbolic-geometry plumbing.
5. **DiffuDR** (Prop 1) — kills negative sampling entirely; new training paradigm.
6. **SemDR** (Prop 2) — most ambitious; full generative-retrieval rebuild, best long-term cold-start story.

### Composability
Proposals are **stackable**: e.g. `MoMoE-DR encoder` + `NoiseDR contrastive` + `CausalDR decoder head` is a single coherent system hitting W3, W4, W5, W6, W8 at once while staying <15% similar to any existing DR paper.

---

## 8. Honesty Rules (inherited — apply to every proposal)
1. Strict per-fold masking of test drug–disease edges from **all** graphs/adjacencies/conditioners.
2. Model selection on a **val split**, never the test fold. Report honest (val) **and** inflated (test) with the gap.
3. Report balanced 1:1 **and** imbalanced 1:5 AUPR; for Prop 4 also report **long-tail-stratified** AUROC.
4. GIP matrices (computed on the full association matrix) remain **banned** under CV.
5. Any AUROC > 0.93 honest is treated as a suspected leakage bug until proven otherwise.
6. Cold-start claims (Prop 2/5) must be validated on an **inductive split** where evaluated drugs/diseases are absent from training.
7. **Data-quality guard (new, from §0.5):** `Drug_mol2vec.csv` is degenerate (2 unique vectors) — banned as a drug feature in every proposal. Drug content comes from **SMILES** (`DrugInformation.csv`); disease content from **MeSH** with the 29/16/8 missing rows imputed; protein content from **ESM-2** (clean). Add an assertion at data-load time: `assert n_unique(drug_features) > 0.9 * n_drugs` to fail fast if a degenerate feature ever sneaks in.

---

## Sources

**RecSys SOTA transferred**
- [DiffRec: Diffusion Recommender Model (SIGIR'23)](https://hexiangnan.github.io/papers/sigir23-DiffRec.pdf)
- [Diffusion Models in Recommendation Systems: A Survey](https://arxiv.org/pdf/2501.10548)
- [DiffGRM: Diffusion-based Generative Recommendation Model](https://arxiv.org/html/2510.21805v1)
- [TIGER: Transformer Index for Generative Recommenders](https://www.emergentmind.com/topics/transformer-index-for-generative-recommenders-tiger)
- [Generative Recommendation with Semantic IDs: A Practitioner's Handbook](https://arxiv.org/html/2507.22224v1)
- [Disentangled Representation Learning for Recommendation (IEEE TPAMI)](https://ieeexplore.ieee.org/document/9720218/)
- [Disentangled Hyperbolic Collaborative Filtering (ScienceDirect)](https://www.sciencedirect.com/science/article/abs/pii/S0950705123008857)
- [Intent-aware Recommendation via Disentangled Graph Contrastive Learning](https://arxiv.org/pdf/2403.03714)
- [Hyperbolic Diffusion Recommender Model](https://arxiv.org/pdf/2504.01541)
- [Debiasing Recommendation with Personal Popularity (PPAC)](https://arxiv.org/html/2402.07425v2)
- [Taming Recommendation Bias with Causal Intervention on Evolving Personal Popularity](https://arxiv.org/html/2505.14310v1)
- [A Survey on Causal Inference for Recommendation](https://pmc.ncbi.nlm.nih.gov/articles/PMC10901840/)
- [A Self-Supervised Mixture-of-Experts Framework for Multi-behavior Recommendation](https://arxiv.org/abs/2508.19507)
- [M3oE: Multi-Domain Multi-Task Mixture-of-Experts (SIGIR'24)](https://arxiv.org/pdf/2502.06244)
- [SimGCL / XSimGCL family — Long-tail Augmented Graph Contrastive Learning](https://arxiv.org/pdf/2309.11177)
- [Masked Graph Transformer for Large-Scale Recommendation (SIGIR'24)](https://arxiv.org/html/2405.04028v1)
- [LightGNN: Simple Graph Neural Network for Recommendation](https://arxiv.org/pdf/2501.03228)

**Multi-modal & KG-enhanced RecSys + structural-bio SOTA (Part II)**
- [FREEDOM: Freezing & Denoising Graph Structures for Multimodal Recommendation](https://arxiv.org/pdf/2412.11747)
- [BM3: Bootstrapped Multimodal self-supervised Recommendation](https://arxiv.org/pdf/2309.05273)
- [MAMEX: Multi-modal Adaptive Mixture of Experts for Cold-start Recommendation](https://arxiv.org/html/2508.08042v1)
- [Modality Alignment with Multi-scale Bilateral Attention for Multimodal Recommendation](https://arxiv.org/html/2509.09114)
- [KGCL: Knowledge Graph Contrastive Learning for Recommendation (SIGIR'22)](https://dl.acm.org/doi/abs/10.1145/3477495.3532009)
- [KGRec: Knowledge Graph Rationalization for Recommendation](https://www.nature.com/articles/s41598-024-74516-z)
- [MolMix: Multimodal Molecular Representation (SMILES + 2D + 3D)](https://arxiv.org/html/2410.07981v1)
- [Uni-Mol: A Universal 3D Molecular Representation Learning Framework](https://arxiv.org/pdf/2402.01975)
- [Generalist Equivariant Transformer Towards 3D Molecular Interaction Learning](https://arxiv.org/pdf/2306.01474)
- [AlphaFold Protein Structure Database in 2024](https://pubmed.ncbi.nlm.nih.gov/37933859/)
- [DREAM-GNN: Dual-Route Embedding-Aware GNN for Drug Repositioning (2025)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12554636/)
- [STRING database](https://string-db.org/) · [KEGG database](https://www.genome.jp/kegg/)

**DR context (the methods we must stay <15% similar to)**
- [GCGB: Heterogeneous Graph Contrastive Learning with Gradient Balance](https://academic.oup.com/bib/article/26/1/bbae650/7927589)
- [RGLDR: Regulation-aware Graph Learning for Drug Repositioning](https://www.sciencedirect.com/science/article/abs/pii/S002002552401274X)
- [Drug Repositioning with GraphSAGE and Clustering Constraints](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9127467/)
- [Hierarchical Negative Sampling Graph Contrastive Learning for DDA](https://pubmed.ncbi.nlm.nih.gov/38294927/)
