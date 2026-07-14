# ONE-PAGER — Ôn nước rút Multimodal ML (liếc trước giờ thi)
Học máy Đa thể thức (CMU 11-777). Chi tiết: [A-Tổng quan](A-tong-quan-6-thach-thuc.md) · [B-Biểu diễn đơn](B-bieu-dien-don-the-thuc.md) · [C-Fusion/Coord/Fission](C-fusion-coordination-fission.md) · [D-Alignment](D-alignment.md) · [E-Transformers/Reasoning](E-transformers-reasoning.md) · [F-Interaction/Inference](F-interaction-inference.md) · [G-Generation](G-generation.md) · [H-Transference](H-transference.md) · [I-Quantification](I-quantification.md)

---

## 🌐 ĐỊNH NGHĨA LÕI (phải thuộc)
**Multimodal = khoa học về dữ liệu HETEROGENEOUS + INTERCONNECTED (connected + interacting).**
- **Connection** = thuộc tính **dữ liệu** (có sẵn): Association · Dependency · Correspondence · Relationship.
- **Interaction** = xảy ra khi **INFERENCE**: Redundancy · Uniqueness · **Synergy (emergence)**.

## 🏛️ 6 THÁCH THỨC CỐT LÕI ⭐⭐⭐
| # | Thách thức | Định nghĩa 1 câu | Sub-challenges |
|---|---|---|---|
| 1 | **Representation** | biểu diễn phản ánh tương tác chéo | Fusion (`>`) · Coordination (`=`) · Fission (`<`) |
| 2 | **Alignment** | kết nối chéo giữa **mọi phần tử** | Discrete · Continuous · Contextualized |
| 3 | **Reasoning** | kết hợp tri thức qua **nhiều bước** | Structure · Concepts · Inference · Knowledge |
| 4 | **Generation** | sinh raw modality giữ mạch lạc | Summarization(`>`) · Translation(`=`) · Creation(`<`) |
| 5 | **Transference** | chuyển tri thức giúp modality yếu | Transfer · Co-learning · Model Induction |
| 6 | **Quantification** | hiểu heterogeneity/interactions/learning | Heterogeneity · Interactions · Learning |

**6 chiều heterogeneity (R-D-S-I-N-R):** Representation · Distribution · Structure · Information · Noise · Relevance.

---

## 🔢 CÔNG THỨC PHẢI NHỚ
| Chủ đề | Công thức | Ghi nhớ |
|---|---|---|
| **Conv output** | `H_out=⌊(H+2P−D(K−1)−1)/S+1⌋` | P padding, S stride, D dilation |
| **Cosine coordination** | `⟨z_A,z_B⟩/(‖z_A‖‖z_B‖)` | centering ⇒ = Pearson |
| **RBF kernel** | `exp(−‖x_i−x_j‖²/2σ²)` | ánh xạ cao chiều |
| **InfoNCE ↔ MI** | `I(X_A;X_B) ≥ log N − L*` | contrastive = lower bound MI |
| **Mutual info** | `I(X;Y)=H(X)−H(X\|Y)=KL(p(x,y)‖p(x)p(y))` | — |
| **Scaled dot attn** | `α=softmax(q·k/√d)`, `h=Σα·v` | Q·K (không phải V) |
| **Self-attention** | perm-**equivariant** → **cần position embedding** | — |
| **Perplexity** | `PPL=exp(L)`, `L=−(1/N)Σlog p` | PPL=10 ≈ chọn giữa 10 từ |
| **LSTM gradient** | `∂c_t/∂c_{t−1}=f_t` | "gradient highway", `f_t≈1` |
| **VAE ELBO** | `log p(x) ≥ E_q[log p(x\|z)] − KL(q‖p)` | reconstruction − prior |
| **Reparameterization** | `z=μ+σ⊙ε`, `ε~N(0,I)` | z liên tục, q reparam, f khả vi |
| **Interaction (thống kê)** | `f ≠ f_A(x_A)+f_B(x_B)` ⇒ có tương tác | non-additive |
| **MultiViz interaction** | `∂²f/∂x_A∂x_B > 0` | gradient bậc 2 |
| **Causal** | `p(y\|do(x)) ≠ p(y\|x)` | intervention xóa cạnh **đi vào** x |
| **Co-regularization** | `L=(f1(X1)−f2(X2))²` | ép 2 view đồng thuận |
| **DAG acyclic** | trace lũy thừa ma trận kề = 0 | NO TEARS |

---

## ⚖️ SO SÁNH LÕI (dễ bị lừa)

**Representation — đếm modality vs representation:** Fusion `#mod>#rep` (gộp) · Coordination `#mod=#rep` (giữ riêng, phối hợp, CLIP) · Fission `#mod<#rep` (tách shared/unique).

**Fusion operators (tăng dần):** additive(=late/ensemble) → multiplicative → bilinear → **tensor**(uni+bi+tri, weight bùng nổ) → **low-rank**(sửa tensor) → polynomial → gated(=attention) → nonlinear/dynamic. **EMAP:** additive là baseline mạnh bất ngờ.

**Connection ≠ Interaction:** connection = dữ liệu (có sẵn); interaction = khi inference.

**Partial Information Decomposition:** Redundancy(chung) · Uniqueness(riêng) · **Synergy(emergence, VD sarcasm)**. Interaction info cổ điển có thể **âm**; PID **không âm**.

**Alignment:** Assignment(1-1 cứng, tập bằng nhau, Hungarian/LP) vs **Optimal Transport**(mềm, many-many, **Wasserstein**). Soft attn(khả vi, mặc định) vs Hard attn(rời rạc, **RL**). DTW(1 path) vs Soft-DTW(khả vi) vs **CTW**(DTW+CCA). CTC(phoneme, supervised, blank) vs **HuBERT**(pseudo-label clustering, self-supervised).

**Transformer đa thể thức — 3 mẫu:** One-stream(concatenate — **VisualBERT/UNITER**) · Cross-modal(co-attention — **ViLBERT/LXMERT**) · Modality-shift(**MAG-BERT**). Cross-modal V→L: **Query từ modality cần cập nhật (L)**.

**CNN vs ViT:** CNN có bias **locality** (ít data thắng); ViT không → cần **pretrain lớn**, long-range trực tiếp. **MAE:** mask ~75%, decoder chỉ khi pretrain. **ViLT** ≈ ViT+BERT (bỏ detector, nhanh). **ALBEF:** align **before** fuse.

**GNN:** GCN(cùng trọng số, khác norm) vs **GAT**(attention `α_uv`). Transformer = GNN trên **đồ thị đầy đủ**.

**Reasoning structure discovery:** NMN(RNN layout, **REINFORCE**) · NAS/**DARTS**(khả vi, softmax→argmax, bi-level) · Neuro-symbolic(tách reasoning khỏi perception) · Neural State Machine(scene graph).

**RL:** Value-based(sample-efficient) vs Policy-based(**REINFORCE**, không cần transition, variance cao). **DQN diverge** (correlation + non-stationary target) → **experience replay + fixed Q-targets**. **Actor-Critic:** advantage `Q−V`.

**Inference paradigm:** Logical(VQA-LOL, **Fréchet inequalities**) · Causal(`do(x)`, Causal VQA: covariant=treatment / invariant=nuisance).

**Mô hình sinh:** Autoregressive(exact likelihood, chậm sample) · **VAE**(ELBO, train nhanh, **mờ**) · **Diffusion**(chất lượng cao, chậm sample; = multi-level VAE, latent dim=data dim, encoder cố định). **Latent Diffusion**(diffusion trong latent → nhanh). **Classifier-free guidance** > classifier guidance. **DALL-E**(dVAE+autoregressive) vs **DALL-E 2**(CLIP+diffusion).

**Reparameterization vs REINFORCE:** reparam(z liên tục, f khả vi) · **REINFORCE**(z rời rạc/f hộp đen — RL, NMN layout).

**Transference:** Transfer(pretrained θ*) · Co-learning(1 model, modality phụ **chỉ lúc train**, test 1 modality) · Model Induction(nhiều model riêng: self/co-training). **Co-training(Blum&Mitchell):** 2 view đủ+độc lập, pseudo-label chéo.

**Quantification interaction phân loại:** `I_A·I_B>0` complementary · `<0` conflict · `I_A≫I_B` **dominance** (ngôn ngữ thường áp đảo sentiment). Cross-modal interaction làm **social bias TỆ HƠN**.

---

## 🔑 CÁC CÔNG TRÌNH GẮN VỚI KHÁI NIỆM (nhận diện nhanh)
CLIP(coordination/InfoNCE) · Tensor Fusion(Zadeh) · Low-rank(Liu) · EMAP(Hessel&Lee) · CCA/DCCAE(coordination) · PID(Williams&Beer, Bertschinger, Liang) · DTW/CTW · CTC(Graves) · HuBERT · BERT(MLM+NSP) · ViT(Dosovitskiy) · MAE(He) · ViLBERT/LXMERT/VisualBERT/UNITER/ViLT/ALBEF · NMN(Andreas/Hu) · Neuro-symbolic(Yi) · NSM(Hudson) · VQA-LOL(Gokhale) · Causal VQA(Agarwal) · OK-VQA/KAT · REINFORCE/Actor-Critic · DQN(replay+fixed target) · DALL-E/DALL-E2/Imagen/Latent Diffusion · Frozen/Flamingo/MiniGPT-4/FROMAGe · Socher(zero-shot) · Pham(cyclic translation) · Vokenization · Co-training(Blum&Mitchell) · HighMMT/Gato · MultiViz/M2Lens.

---

## 🧠 MẸO PHÂN BIỆT "THÁCH THỨC NÀO?"
- Học vector chung / phối hợp / tách → **Representation**.
- Nối phần tử ↔ phần tử, warping, self-attention/BERT → **Alignment**.
- Nhiều bước, logic/nhân quả, tri thức ngoài, RL, VQA → **Reasoning**.
- Sinh ảnh/text/tóm tắt/dịch modality, VAE/diffusion → **Generation**.
- Modality phụ chỉ lúc train, zero-shot, co-training → **Transference**.
- Đo bias/synergy/robustness/OGR, giải thích model → **Quantification**.
