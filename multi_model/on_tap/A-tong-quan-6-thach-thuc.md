# CHEAT-SHEET — Cụm A: Tổng quan & 6 Thách thức cốt lõi
Nguồn: `multimodal Learning` (bài nhập môn, CMU 11-777). Đây là **khung xương** của cả môn — mọi bài sau đều là đào sâu 1 trong 6 thách thức.

---

## 1. Multimodal là gì? (định nghĩa phải thuộc lòng)

- **Định nghĩa từ điển:** multimodal = có nhiều thể thức (modalities).
- **Định nghĩa nghiên cứu (PHẢI NHỚ):** *Multimodal là khoa học về dữ liệu **dị thể (heterogeneous)** và **liên kết (interconnected)**.* → 2 từ khóa `heterogeneous` + `interconnected` là chìa khóa của cả môn.
- **Modality (thể thức):** *cách thức mà một thứ được biểu đạt hoặc cảm nhận.* Trục **raw → abstract**:
  - **Raw modality** (gần sensor nhất): tín hiệu speech, ảnh pixel.
  - **Abstract modality** (xa sensor nhất): đối tượng đã phát hiện, cường độ cảm xúc, category.
  - 👉 Modality càng abstract càng **dễ đồng nhất (homogeneous)**.

- **Homogeneous vs Heterogeneous:**
  - *Homogeneous* (chất lượng tương đồng): text 2 ngôn ngữ, ảnh từ 2 camera.
  - *Heterogeneous* (chất lượng đa dạng): ngôn ngữ vs thị giác.

---

## 2. Sáu CHIỀU của tính DỊ THỂ (heterogeneity) ⭐ (rất hay ra)

Thông tin ở các modality khác nhau có chất lượng, cấu trúc, biểu diễn khác nhau theo 6 chiều:

| # | Chiều | Nội dung | Ví dụ |
|---|---|---|---|
| 1 | **Element representation** | rời rạc/liên tục, độ hạt (granularity) | pixel liên tục vs từ rời rạc |
| 2 | **Element distribution** | mật độ, tần suất | words/phút vs objects/ảnh; speech dày, text thưa |
| 3 | **Structure** | temporal, spatial, hierarchical, latent, explicit | speech=thời gian, ảnh=không gian, câu=cây cú pháp |
| 4 | **Information** | mức trừu tượng, entropy | ảnh nhiều bit hơn caption |
| 5 | **Noise** | bất định, SNR, dữ liệu thiếu | lỗi OCR/ASR, missing modality |
| 6 | **Relevance** | liên quan tác vụ, phụ thuộc ngữ cảnh | teacup ↔ "study room" |

> **Mẹo nhớ:** *R-D-S-I-N-R* → **R**epresentation, **D**istribution, **S**tructure, **I**nformation, **N**oise, **R**elevance.

---

## 3. Modality LIÊN KẾT: Connections vs Interactions ⭐⭐

Đây là phân biệt **cực kỳ hay bị lừa** trong đề thi:

- **① Modality CONNECTIONS (kết nối):** các modality **liên quan & chia sẻ điểm chung** — là thuộc tính **tĩnh của dữ liệu**, tồn tại **trước** khi suy luận.
  - **Statistical:** Association (tương quan, đồng xuất hiện) · Dependency (nhân quả, thời gian).
  - **Semantic:** Correspondence (grounding) · Relationship (chức năng, "used for").
- **② Modality INTERACTIONS (tương tác):** các phần tử modality **tương tác trong lúc SUY LUẬN (inference)** để tạo ra phản hồi (response). → Xảy ra **khi suy luận**, không phải sẵn có trong dữ liệu.

> **Bẫy kinh điển:** Connection = tính chất của **dữ liệu** (có sẵn); Interaction = xảy ra khi **inference** (mô hình xử lý). Nhớ: *"Connections share, Interactions happen during inference."*

---

## 4. Phân loại PHẢN HỒI TƯƠNG TÁC (Partan & Marler 2005) ⭐

Góc nhìn khoa học hành vi — hai tín hiệu a, b kết hợp cho ra response:

- **Redundancy (dư thừa)** — a và b cho response giống nhau:
  - **Equivalence:** a = b (cho cùng kết quả).
  - **Enhancement:** a + b → response **mạnh hơn** (được củng cố).
- **Non-redundancy (không dư thừa)** — a và b khác nhau:
  - **Independence:** a, b độc lập.
  - **Dominance:** một modality **áp đảo** (VD "study room" thắng "living room").
  - **Modulation:** a điều biến b.
  - **Emergence (trồi lên):** a + b tạo response **mới** không có ở modality đơn lẻ.

**4 chiều của tương tác (digitally-represented):**
1. **Interaction responses:** redundancy, non-redundancy, dominance, emergence…
2. **Interaction mechanics:** additive, multiplicative, nonlinear, causal, logical…
3. **Input modalities:** unimodal, bimodal, trimodal, high-modal…
4. **Context:** structure context, task relevance, context dependence…

---

## 5. SÁU THÁCH THỨC CỐT LÕI ⭐⭐⭐ (xương sống toàn môn)

| # | Thách thức | Định nghĩa ngắn | Sub-challenges |
|---|---|---|---|
| 1 | **Representation** | Học biểu diễn phản ánh **tương tác chéo modality** giữa các phần tử | **Fusion** (#mod > #rep) · **Coordination** (#mod = #rep) · **Fission** (#mod < #rep) |
| 2 | **Alignment** | Nhận diện & mô hình hóa **kết nối chéo** giữa mọi phần tử, dựa trên cấu trúc dữ liệu | Connections (grounding) · Aligned representation · Segmentation |
| 3 | **Reasoning** | Kết hợp tri thức qua **nhiều bước suy luận**, khai thác alignment + cấu trúc bài toán | Structure · Intermediate concepts · Inference paradigm · External knowledge |
| 4 | **Generation** | Học tiến trình **sinh dữ liệu mới** giữ tương tác/cấu trúc/mạch lạc chéo modality | Summarization (giảm) · Translation (giữ) · Creation (tăng) |
| 5 | **Transference** | **Chuyển tri thức** giữa modality để hỗ trợ modality yếu (nhiễu/thiếu/ít tài nguyên) | Transfer (pretrained) · Co-learning via representation · Co-learning via generation |
| 6 | **Quantification** | Nghiên cứu **thực nghiệm & lý thuyết** về heterogeneity, interactions, learning dynamics | Heterogeneity · Interactions · Learning |

### 5.1. Ba sub-challenge của Representation (đếm modality vs representation)
- **Fusion:** `#modalities > #representations` — gộp nhiều modality thành ÍT biểu diễn hơn. VD: ảnh + text → 1 vector chung. Encoder có thể **pre-trained** hoặc **học chung** với mạng fusion.
- **Coordination:** `#modalities = #representations` — giữ biểu diễn riêng nhưng **phối hợp** qua tương tác chéo (VD cosine similarity — coordination mạnh; RBF/kernel). **Cần dữ liệu ghép cặp (paired data).**
- **Fission:** `#modalities < #representations` — tạo **NHIỀU** biểu diễn hơn để phản ánh cấu trúc nội tại (factorization/clustering). VD: tách phần chỉ-ngôn-ngữ / chỉ-thị-giác / chung.

### 5.2. Early vs Late Fusion (góc nhìn lịch sử)
- **Early fusion:** **concatenate** đặc trưng thô rồi mới dự đoán (1 prediction).
- **Late fusion:** mỗi modality dự đoán riêng (`ŷ_A`, `ŷ_B`) rồi **gộp quyết định**.

### 5.3. Coordination function (công thức)
- **Cosine similarity:** `g(z_A, z_B) = ⟨z_A, z_B⟩ / (‖z_A‖·‖z_B‖)` → coordination **mạnh**; với input chuẩn hóa ≈ hệ số tương quan Pearson.
- **Kernel similarity:** `g = k(z_A, z_B)` (linear, polynomial, exponential, RBF). RBF: `K(x_i,x_j) = exp(−‖x_i−x_j‖²/2σ²)` — ánh xạ lên không gian cao chiều để phân tách tuyến tính.

---

## 6. Reasoning — điểm nhấn về COMPOSITIONALITY

- **Winoground (Thrush 2022):** CLIP/ViLT/ViLBERT đều ~**random chance** khi phải phân biệt các tổ hợp ngữ nghĩa khác nhau nhưng cùng bộ từ → mô hình yếu về **tính hợp thành (compositional generalization)**.
- **Hierarchical structure:** khai thác **cây cú pháp** ngôn ngữ (parse → object detection → coordination → composition) để grounding, VD "Skis of man in red jacket".
- **Module Networks (Andreas 2016 / Hu 2017):** học lắp ráp các module suy luận end-to-end cho VQA.
- **External knowledge (OK-VQA, Marino 2019):** VQA cần tri thức ngoài (Wikipedia, knowledge graph, COMET).
- **Interactive structure:** cấu trúc định nghĩa qua môi trường tương tác — khác temporal ở chỗ **hành động ở bước trước ảnh hưởng trạng thái tương lai** (policy `a`).

---

## 7. Generation, Transference, Quantification — ý cốt

**Generation** (theo lượng thông tin content):
- **Summarization** (`<`, reduction): giảm content, giữ phần nổi bật (VD tóm tắt video How2).
- **Translation** (`=`, maintenance): dịch modality→modality, giữ nội dung (VD DALL·E: text→image qua CLIP + diffusion).
- **Creation** (`>`, expansion): sinh **đồng thời** nhiều modality, tăng content, giữ mạch lạc (khó nhất — cần nhớ representation + alignment + reasoning).

**Transference** (modality B chỉ có **lúc train**, giúp modality A):
- **Transfer via pretrained models:** finetune/prefix-tuning từ mô hình lớn (BERT, Frozen LM). VD "This is a dax." few-shot.
- **Co-learning via representation:** phối hợp biểu diễn để zero-shot (Socher 2013: word embedding cho zero-shot image classification — **test chỉ dùng ảnh**).
- **Co-learning via generation:** dịch chéo modality trong lúc train để robust với modality thiếu/nhiễu lúc test (Pham 2019, cyclic translation).

**Quantification** (hiểu bản chất mô hình):
- **Heterogeneity:** đo modality bias, **unimodal bias & modality collapse**, cân bằng modality (VD greedy learning, VQA v2).
- **Interactions:** đánh giá phụ thuộc chéo (attention weights); **social bias bị khuếch đại** khi kết hợp modality (Women also Snowboard; biases compound).
- **Learning:** động lực học tối ưu & tổng quát hóa từng modality.

---

## 8. Bốn họ MÔ HÌNH đa thể thức & xu hướng
1. **Concatenation-based** (early fusion). 2. **Attention-based** (CLIP, ViLBERT — cross-modal transformer). 3. **Graph Neural Networks.** 4. **Contrastive learning** (căn ảnh–text).
- Xu hướng: GPT-4V, self-supervised multimodal, embodied AI; thách thức mở: explainability, fusion hiệu quả/mở rộng, few/zero-shot.

---

## 🎯 CÂU HAY RA THI (Cụm A)
1. Định nghĩa nghiên cứu của multimodal? → *khoa học về dữ liệu **heterogeneous & interconnected**.*
2. Phân biệt **Connection** vs **Interaction**? → connection = thuộc tính dữ liệu (có sẵn); interaction = xảy ra khi inference.
3. Fusion vs Coordination vs Fission phân biệt bằng gì? → so **#modalities vs #representations** (>, =, <).
4. Kể 6 thách thức cốt lõi + 6 chiều heterogeneity.
5. Phân loại phản hồi tương tác: redundancy (equivalence/enhancement) vs non-redundancy (independence/dominance/modulation/**emergence**).
