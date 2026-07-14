# CHEAT-SHEET — Cụm G: Sinh Đa thể thức (Thách thức 4 – Generation)
Nguồn: `Lecture9.1-Generation-Part1`, `Lecture9.2-Generation-Part2`. Gồm 3 sub-challenge + các họ mô hình sinh (autoregressive, VAE, diffusion).

> **Định nghĩa Generation:** *Học tiến trình sinh để tạo **raw modalities** phản ánh tương tác chéo, cấu trúc & mạch lạc.*

---

## 1. HAI CHIỀU CỦA GENERATION ⭐

**Chiều 1 — Information content (so lượng content input↔output):**
| Sub-challenge | Content | Nghĩa |
|---|---|---|
| **4a Summarization** | **Reduction** (`>`) | giảm content, giữ phần nổi bật |
| **4b Translation** | **Maintenance** (`=`) | đổi modality, giữ nội dung |
| **4c Creation** | **Expansion** (`<`) | sinh thêm content mới |

**Chiều 2 — Generative process:**
- **Exemplar** (chọn/truy xuất mẫu có sẵn) ≈ **extractive**.
- **Generative** (sinh mới hoàn toàn) ≈ **abstractive**.

### 1.1. 4a Summarization
- **How2 video (Palaskar 2019):** tóm tắt đa thể thức — video có **tương tác chéo bổ sung** không có trong text. Fusion (joint representation) bắt tương tác bổ sung → generative ≈ abstractive, exemplar ≈ extractive.

### 1.2. 4b Translation ⭐
- **DALL-E (Ramesh 2021):** ① **Discrete VAE / VQ-VAE** tạo **visual token rời rạc** (grid 32×32, codebook [0..8191]) → ② **Autoregressive Transformer** sinh token → ③ image decoder. Content = coordination qua supervised translation; generation = exemplar (codebook) + generative.
- **DALL-E 2 (Ramesh 2022):** **CLIP embedding + diffusion** — content = coordination qua **CLIP similarity**; generation = **fully generative (diffusion)**.
- Khác: Language→Pose, virtual humans (speech→gesture).

### 1.3. 4c Creation (khó nhất)
- Sinh **đồng thời nhiều modality**, tăng content, giữ **mạch lạc trong & giữa modality** ("Big dog on the beach" + 'woof'/'crash' + video, cần temporal+causal+logical). Nhắc lại representation & alignment & reasoning. Bước đầu: **factorized generation** (Tsai 2019).

### 1.4. Captioning — 3 góc nhìn
- **As summarization:** trích `<object, action, scene>` triplet rồi truy xuất câu (Farhadi 2010).
- **As translation:** câu template mô tả object/attribute/relation (Baby Talk).
- **As generation:** visual storytelling (Huang 2016). → **Generation phụ thuộc dữ liệu** (mục tiêu người viết caption khác nhau).

---

## 2. MÔ HÌNH SINH — nền tảng

**Mục tiêu:** học `p(x)` (x = text/image/video/multimodal): đánh giá độ thực (p cao = thực), lấy mẫu x mới, học biểu diễn unsupervised. **Conditional `p(x|c)`** (c = category/image), **style transfer `p(x2|x1,c)`**.

### 2.1. Autoregressive models ⭐
- Chain rule: `p(x) = Π p(x_i | x_{<i})` — **exact likelihood**. VD: **PixelRNN** (ảnh), **WaveNet** (audio), **GPT** (text).
- **Đặc điểm:** dễ train, **exact inference**; **chậm khi sample** (tuần tự); **khó condition**.
- **Conditioning `p(x|c)`:** prefix tuning (Frozen, **Flamingo** 80B + cross-attention, LiMBeR, MiniGPT-4, LLaMA-Adapter+**ImageBind**, FROMAGe); representation tuning (MAG); pseudo-attention; **Bayes rule** (FUDGE — future discriminators); **gradient tuning** (PPLM — plug-and-play).

### 2.2. Latent Variable Models → VAE ⭐⭐
- **Ý tưởng:** mô hình hóa yếu tố biến thiên ẩn `z` (hair color, pose...) bằng **latent variable** + prior; features qua `p(z|x)`, sinh x mới từ z ngẫu nhiên. Dù `p(x|z)` đơn giản, **marginal `p(x)` rất phong phú**.
- **GMM** (tiền thân): sample component z → sample từ Gaussian; giải bằng **EM**.
- **Vấn đề:** MLE với `p(x) = ∫ p(x,z)dz` **intractable** (z 30-bit → tổng 2³⁰; z liên tục → tích phân bất khả).
- **Variational inference:** xấp xỉ posterior bằng `q` đơn giản, gần `p` nhất → tối ưu **ELBO (Evidence Lower Bound)**:
  `log p(x) ≥ E_q[log p(x|z)] − KL(q(z|x) ‖ p(z))` = **reconstruction − prior regularization**.
  - `q(z|x)` = **encoder** (data→latent); `p(x|z)` = **decoder**. Posterior gap = phần bỏ qua (nhỏ nếu q tốt).
- **Reparameterization trick ⭐⭐:** để gradient qua kỳ vọng phụ thuộc tham số, viết `z = μ + σ ⊙ ε`, `ε ~ N(0,I)` → tách randomness khỏi tham số. **Yêu cầu:** z **liên tục**, q **reparameterizable**, f **khả vi**. (Khi z rời rạc/f hộp đen → dùng **REINFORCE**.)
- **β-VAE:** β=1 → VAE thường; β>1 → ràng buộc mạnh hơn cho **disentanglement** (chiều latent độc lập — hữu ích cho style transfer style↔content; nhưng khó, kết quả trái chiều).
- **Đặc điểm:** dễ train, **có encoder tường minh `q(z|x)`**; ảnh **mờ hơn** (do reconstruction).

### 2.3. Diffusion Models ⭐⭐
- **Ý tưởng:** sinh bằng **khử nhiễu (denoising)**. Forward = **thêm nhiễu** dần; reverse = **khử nhiễu** dần.
- **Giống VAE nhưng:** ① latent dim = **data dim**; ② encoder q **KHÔNG học** — cố định là Gaussian quanh output bước trước; ③ tham số Gaussian **biến thiên theo thời gian** sao cho latent cuối = standard Gaussian. → **"multi-level VAE"** (nhiều tầng), học qua **ELBO**.
- **Reverse:** dùng Bayes để đảo, xấp xỉ Gaussian, reparameterization; mạng dự đoán ảnh sạch `x_{t−1}` từ `x_t`. Lịch nhiễu: **nhỏ ở đầu, tăng dần**.
- **Continuous (SDE):** diffusion liên tục = **"mô hình vô hạn tầng"** → mẫu chất lượng cao, exact log-likelihood, controllable.
- **Conditioning:** ① **train trực tiếp có điều kiện** (DALL-E 2 = diffusion trên CLIP embedding; **Imagen** = trên T5; **Latent Diffusion / Stable Diffusion** = diffusion trong **không gian latent** thay pixel → nhanh hơn: autoencoder nén tri giác, diffusion nén ngữ nghĩa). ② **Classifier guidance** (dùng gradient classifier). ③ **Classifier-free guidance** (1 model, train uncond = set y=const; **được ưa dùng hơn**, GLIDE).

### 2.4. So sánh 3 họ mô hình sinh ⭐⭐ (bảng vàng)
| Họ | Inference | Ưu | Nhược |
|---|---|---|---|
| **Autoregressive** | exact (chain rule) | dễ train, **exact likelihood** | **chậm sample**, khó condition |
| **VAE** | approx (ELBO) | **train nhanh/dễ**, có encoder | chất lượng thấp hơn (**mờ**) |
| **Diffusion** | approx (modeling noise) | **chất lượng cao** | **chậm sample** |

---

## 3. ĐIỀU KHIỂN mô hình sinh (6 cách)
1. **Disentanglement** (β-VAE). 2. **Conditioning** (train có điều kiện). 3. **Prompt/prefix tuning** (adapter). 4. **Representation tuning** (MAG shift). 5. **Classifier gradient tuning** (PPLM/classifier guidance). 6. **Classifier-free tuning**.

## 4. THÁCH THỨC MỞ & ĐẠO ĐỨC
- Sinh đồng bộ nhiều modality; kết hợp generation với **suy luận tường minh** (compositional generation); fusion/alignment tốt hơn trong sinh; kiểm soát tinh + few-shot; **đánh giá lấy con người làm trung tâm**.
- **Đạo đức:** deepfake/upsampling sai lệch (PULSE), **trích xuất dữ liệu huấn luyện** từ LLM (Carlini 2021), **thiên lệch trong sinh** ("The woman worked as a babysitter", Sheng 2019).

---

## 🎯 CÂU HAY RA THI (Cụm G)
1. 3 sub-challenge của Generation theo lượng content (reduction/maintenance/expansion)?
2. Exemplar vs Generative process ≈ extractive vs abstractive?
3. DALL-E dùng gì (dVAE + autoregressive) vs DALL-E 2 (CLIP + diffusion)?
4. ELBO gồm 2 số hạng gì? Encoder/decoder tương ứng q/p nào?
5. Reparameterization trick: công thức + 3 điều kiện? Khi nào phải dùng REINFORCE thay thế?
6. Diffusion giống/khác VAE ở 3 điểm nào?
7. Latent Diffusion nhanh hơn nhờ đâu? Classifier-free vs classifier guidance?
8. So sánh 3 họ: autoregressive/VAE/diffusion (inference, tốc độ sample, chất lượng).
