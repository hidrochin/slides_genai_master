# CHEAT-SHEET — Cụm C: Fusion, Coordination & Fission (Thách thức 1 – Representation)
Nguồn: `lecture3_1-MultimodalFusion`, `lecture3_2-MultimodalCoordinationFission`. Đây là 3 sub-challenge của **Representation** — cụm nặng công thức, hay ra bài tính.

> **Bản đồ:** Fusion (`#mod > #rep`, gộp thành 1 joint rep) · Coordination (`#mod = #rep`, giữ riêng nhưng phối hợp) · Fission (`#mod < #rep`, tách thành nhiều rep phản ánh cấu trúc nội tại).

---

## 1. FUSION — mô hình hóa tương tác chéo thành 1 biểu diễn chung

### 1.1. Góc nhìn hồi quy tuyến tính (nền tảng phải hiểu) ⭐
`z = w0 + w1·x_A + w2·x_B + w3·(x_A × x_B) + ε`
- `w0` = intercept (bias) · `w1,w2` = **additive** (hiệu ứng riêng từng modality) · `w3` = **multiplicative "interaction"** (hiệu ứng phụ thuộc cả hai) · `ε` = residual.
- Ví dụ book reviews: chỉ khi thêm `w3(x_A×x_B)` và CI của `w3` **không chứa 0** thì mới kết luận có **tương tác nhân** (hiệu ứng cười phụ thuộc vào critic hay không).

### 1.2. Thang các toán tử fusion ⭐⭐
| Loại | Công thức | Ghi chú |
|---|---|---|
| **Additive** | `z = f_A(x_A) + f_B(x_B)` | = **late fusion/ensemble**; mạng 1 lớp là additive |
| **Multiplicative** | `z = w·(x_A × x_B)` | bắt tương tác bậc 2 |
| **Bilinear** | `Z = xᵀ_A W x_B` | ma trận trọng số lớn |
| **Tensor Fusion** (Zadeh 2017) | outer product của `[x;1]` các modality | bắt **đồng thời** unimodal(add) + bimodal + trimodal(mult); nhược: weight **bùng nổ theo số modality** |
| **Low-rank Fusion (LMF)** (Liu 2018) | phân rã CP weight + input | **giảm tham số** tensor fusion, tính hiệu quả |
| **High-order Polynomial** (Hou 2019) | P-order tensor product, weight bậc P+1 | low-rank tensor network |
| **Gated** (Arevalo 2017) | `z = g_A(x_A,x_B)·x_A + g_B(...)·x_B` | gate = **attention** (soft: gradient dễ; hard: cần RL) |
| **Modality-shifting** | primary modality được **dịch** bởi secondary | VD word "expectations" bị shift +/− bởi giọng/nét mặt |
| **Nonlinear** | `y = f([x_A, x_B])`, f = MLP | early fusion; nhưng liệu có học được tương tác phi tuyến? |

**Mẹo nhớ thứ tự phức tạp:** additive → multiplicative → bilinear → tensor → low-rank(tối ưu tensor) → polynomial(bậc cao) → gated/nonlinear/dynamic.

### 1.3. EMAP — Đo tương tác NON-ADDITIVE ⭐ (Hessel & Lee 2020)
- **Câu hỏi:** model của tôi có thật sự học tương tác chéo, hay chỉ additive?
- **EMAP** chiếu (project) mô hình phi tuyến về xấp xỉ additive tốt nhất: `f̂(x_A,x_B) = E_{x_B}[f] + E_{x_A}[f] + μ0`.
- **Phát hiện gây sốc:** khác biệt hiệu năng giữa nonlinear/polynomial và additive **thường rất nhỏ** → **additive luôn là baseline tốt**; nhiều model "phức tạp" không thật sự dùng tương tác chéo.

### 1.4. Fusion với modality dị thể (raw / heterogeneous)
- **Homogeneous fusion** (encoder đưa về không gian gần đồng nhất rồi gộp) vs **raw-modality fusion** (gộp trực tiếp modality thô, dị thể).
- **HMFI (3D detection, ECCV 2022):** camera (2D dày) + LiDAR (3D thưa) → **đưa về voxel 3D chung TRƯỚC khi fuse** (IVLM → QFM → VFIM). Bài học: **structure alignment trước fusion thường khó hơn chính toán tử fusion**; similarity loss làm supervision (không cần nhãn thêm).
- **FuseMix (CVPR 2024):** đóng băng encoder pretrained, chỉ train **adapter nhẹ** (~1-2M param) qua contrastive + **multimodal mixup** → 600× ít GPU-days, 80× ít data pairs, 1 GPU đủ. Bài học: tách 2 câu hỏi — (1) *có biểu diễn được tương tác chéo không* (expressiveness) vs (2) *train được dưới ràng buộc thực tế không* (data/compute efficiency).
- **Dynamic (early) fusion:** quyết định **khi nào** fuse; dùng **NAS** (DARTS, MUFASA) tìm kiến trúc fusion tự động từ các khối (concat/attention/add fuse + conv/layernorm).
- **Heterogeneity-aware (HighMMT):** ước lượng ma trận heterogeneity modality & interaction → **clustering tham số** (chia sẻ tham số giữa modality/interaction giống nhau).

### 1.5. Tại sao thêm modality không phải lúc nào cũng tốt? ⭐ (relevance heterogeneity)
- **Vấn đề:** mạng đa thể thức **dễ overfit hơn** (phức tạp hơn) và **các modality overfit/generalize với tốc độ khác nhau** → "greedy learning" (mạng chỉ dựa vào modality dễ học).
- **OGR (overfitting-to-generalization ratio):** train song song các mạng đơn thể thức để ước lượng OGR từng modality → **reweight loss đa thể thức** cân bằng generalization/overfitting.
- **Robustness:** missing modalities (suy diễn modality thiếu, translation/joint-prob model) và noise trong modality → tradeoff mạnh giữa performance và robustness.

---

## 2. COORDINATION — giữ biểu diễn riêng nhưng phối hợp

**Định nghĩa:** học biểu diễn được *ngữ cảnh hóa đa thể thức*, phối hợp qua tương tác chéo. **Strong** (kéo rất gần) vs **partial** coordination. **Cần dữ liệu ghép cặp (paired data).**

### 2.1. Hàm coordination `g(z_A, z_B)` ⭐⭐
1. **Cosine similarity:** `g = ⟨z_A,z_B⟩/(‖z_A‖‖z_B‖)` — strong coordination; với input đã centering ≈ **Pearson correlation**.
2. **Kernel similarity:** `g = k(z_A,z_B)` (linear/polynomial/exponential/**RBF**). RBF: `K(x_i,x_j)=exp(−‖x_i−x_j‖²/2σ²)`; kernel = ánh xạ `φ(x)` lên không gian cao chiều để **phân tách tuyến tính** (`K = ⟨φ(x_i),φ(x_j)⟩`).
3. **CCA (Canonical Correlation Analysis):** `argmax_{U,V,f_A,f_B} corr(z_A,z_B)` — học nhiều projection **trực giao với nhau**. Biến thể sâu: **DCCAE** (deep canonically correlated autoencoders). **Multi-view intact space**: mỗi view là biểu diễn *một phần* của một "intact" representation đầy đủ.

### 2.2. Contrastive learning ⭐⭐ (trọng tâm)
- **Ý tưởng:** kéo **positive pairs** (ghép đúng) gần, đẩy **negative pairs** xa.
- **Triplet/hinge loss:** `max(0, α + sim(z_A, z⁻_B) − sim(z_A, z⁺_B))` (α = margin). Visual-Semantic Embeddings (Kiros 2014) dùng 2 chiều loss (ảnh↔text).
- **CLIP (Radford 2021):** contrastive pretraining ảnh–text với **InfoNCE**:
  `L = −Σ_i log[ sim(z_A^i, z_B^i) / Σ_j sim(z_A^i, z_B^j) ]`.
  → `z_L` và `z_V` **được phối hợp nhưng KHÔNG đồng nhất** (2 không gian riêng, coordinated). CLIP tập trung vào **shared connections**.

### 2.3. Lý thuyết thông tin (nền để hiểu contrastive) ⭐
- **Information content:** `I(x) = log(1/p(x)) = −log p(x)` (càng ngẫu nhiên → càng nhiều thông tin).
- **Entropy:** `H(X) = E[−log p(X)] = −Σ p(x) log p(x)`.
- **Conditional entropy:** `H(Y|X)`; nếu X,Y độc lập → `H(Y|X)=H(Y)`; nếu X xác định hoàn toàn Y → `H(Y|X)=0`.
- **Mutual information:** `I(X;Y) = H(X) − H(X|Y) = D_KL(p(x,y) ‖ p(x)p(y))`.
- **InfoNCE là chặn dưới của MI ⭐:** `I(X_A;X_B) ≥ log N − L*` → contrastive learning **tối đa hóa lower bound của mutual information**; critic tối ưu `f* = p(x_A,x_B)/(p(x_A)p(x_B))`.
- **InfoMin / multi-view redundancy (Tian 2020):** hiệu năng theo MI giữa 2 view có dạng **chữ U ngược** — có "sweet spot": chia sẻ *vừa đủ* thông tin task, bỏ nuisance (`I(v1;v2)=I(x;y)`). ⚠️ **Multi-view redundancy có thể KHÔNG đúng cho bài toán đa thể thức** (modality có thông tin unique quan trọng).

---

## 3. FISSION — tách thành nhiều biểu diễn phản ánh cấu trúc nội tại

**Định nghĩa:** học *tập biểu diễn mới* phản ánh cấu trúc nội tại (factorization/clustering). **Modality-level** (tách thô: chỉ-lang / chỉ-vision / shared) vs **fine-grained** (tách mịn theo cụm/nhân tố).

### 3.1. Partial Information Decomposition (PID) ⭐⭐ (rất hay hỏi)
Phân rã thông tin task-relevant của 2 modality thành **4 thành phần**:
- **Redundancy (R):** thông tin **chung** cả hai modality đều có về task.
- **Uniqueness U1, U2:** thông tin **riêng** của mỗi modality về task.
- **Synergy (S):** thông tin **trồi lên (emergent)** chỉ có khi kết hợp cả hai — tương ứng "emergence" trong taxonomy tương tác.
- **Vì sao cần PID:** interaction information cổ điển **có thể âm** (khó diễn giải); PID cho các thành phần **không âm** (Williams & Beer 2010, Bertschinger 2014). Chỉ cần **unimodal marginals** để suy ra R/U (convex optimization, scale lên modality liên tục cao chiều qua neural nets — Liang 2023).
- **Mini-taxonomy tương tác:** Agreement+redundancy = contrastive learning; Disagreement+uniqueness = feature selection; Agreement/Disagreement + synergy = hướng mở.

### 3.2. Factorized representations (Tsai 2019 — MFM) ⭐
- Tách **shared + unique** cho mỗi modality bằng: **① maximize MI** `I(z; modality)` và **② minimize conditional entropy** `H(z | modality)`.
- **Generative-Discriminative (MFM):** `L = L1(discriminative) + L2(generative/reconstruction) + L3(no-overlap)`; prior độc lập cho `z_A, z_B, z_shared`.
- **Factorized Contrastive Learning (Liang 2023):** vượt ra ngoài multi-view redundancy — học cả **task-relevant unique information**, xấp xỉ task-relevance Y qua data augmentation.

### 3.3. Fine-grained fission — clustering
- Deep Multimodal Clustering (Hu 2019, audiovisual): unimodal encoders → **khám phá nhiều không gian chia sẻ (cluster)** → phát hiện nhiều tương ứng audio-visual (localized activations cho từng object). Trả lời: *làm sao tự động phát hiện cụm/nhân tố nội tại?*

---

## 🎯 CÂU HAY RA THI (Cụm C)
1. Trong `z = w0 + w1x_A + w2x_B + w3(x_A×x_B)`, số hạng nào là "interaction"? (w3, multiplicative).
2. Additive fusion tương đương gì? (late fusion/ensemble; mạng 1 lớp).
3. Tensor fusion bắt được gì mà additive không? Nhược điểm? (uni+bi+tri-modal; weight bùng nổ → low-rank fusion sửa).
4. EMAP đo gì và phát hiện chính là gì? (đo non-additive interaction; additive là baseline mạnh).
5. Cosine coordination = Pearson khi nào? CCA tối ưu gì?
6. CLIP dùng loss nào? `z_L`, `z_V` có đồng nhất không? (InfoNCE; coordinated nhưng KHÔNG đồng nhất).
7. InfoNCE liên hệ mutual information thế nào? (`I ≥ log N − L*`, lower bound).
8. 4 thành phần PID? Synergy tương ứng khái niệm nào? (R/U1/U2/S; synergy = emergence).
9. Vì sao thêm modality không luôn tốt? (greedy learning, OGR, overfit khác tốc độ).
