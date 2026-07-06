# CHEAT-SHEET — Cụm F2: Suy luận hiệu quả & Lượng tử hóa
Nguồn: `13-efficiency.pdf` + `13-efficiency.ipynb`

---

## 1. Chỉ số đo suy luận (inference metrics) ⭐

| Chỉ số | Ý nghĩa |
|---|---|
| **TTFT** (Time To First Token) | Trễ tới token đầu tiên — quyết định bởi **prefill** |
| **TPS** (Tokens Per Second) | Tốc độ sinh token — quyết định bởi **decode** |
| **Latency** | Tổng thời gian đáp ứng | 
| **Throughput** | Tổng token/giây trên toàn hệ thống (nhiều request) |

**Hai pha suy luận LLM (RẤT hay hỏi):**
- **Prefill** (xử lý prompt): tính song song mọi token → **COMPUTE-BOUND**.
- **Decode** (sinh từng token tự hồi quy): mỗi bước 1 token, đọc lại toàn bộ trọng số → **MEMORY-BOUND**.

**MBU (Model Bandwidth Utilization)** = băng thông đạt được / băng thông đỉnh phần cứng.
- VD ước lượng: model 7B ở 16-bit ⇒ ~14 GB trọng số phải đọc **mỗi token**; TPS × 14GB = băng thông cần → so với đỉnh (A100 ~2 TB/s).
- **Compute-bound vs Memory-bound** quyết định bởi **arithmetic intensity** (FLOPs/byte) — mô hình **Roofline**. Nén model (quantize) giúp pha memory-bound nhưng **không giúp** phần compute-bound.

---

## 2. Tối ưu bộ nhớ & thông lượng khi decode

### 2.1. KV Cache ⭐
- Lưu lại **Key/Value** của các token đã sinh → **không phải tính lại** ở mỗi bước decode.
- Đổi **bộ nhớ lấy tốc độ**. Kích thước KV cache ∝ `2 · batch · seq_len · n_layers · d_model · bytes` → **nghẽn bộ nhớ** khi context/batch lớn.

### 2.2. Batching
- **Static batching**: gom request thành 1 batch cố định — request xong sớm vẫn phải chờ.
- **Continuous / in-flight batching** ⭐: **thêm/bớt** chuỗi vào batch động khi có chỗ trống → **tăng mạnh throughput** (dùng trong vLLM, TGI).

### 2.3. Flash Attention ⭐
- **IO-aware**: chia khối (tiling) + **fuse** phép attention, **không materialize** ma trận attention N×N trong HBM.
- Giảm truy cập bộ nhớ từ **O(N²) → O(N)**; tăng tốc & giảm VRAM, kết quả **chính xác** (không xấp xỉ).
- **FlashAttention-2**: song song hóa tốt hơn, ít phép non-matmul.
- **Flash-Decoding**: song song hóa theo **chiều dài chuỗi KV** → nhanh cho **context dài, batch nhỏ** (lúc decode thiếu song song).

### 2.4. Paged Attention (vLLM)
- Quản lý KV cache như **bộ nhớ ảo phân trang** (paging) → giảm **phân mảnh (fragmentation)**, cho phép **chia sẻ** KV giữa các chuỗi. Tăng số request đồng thời.

### 2.5. Tensor Parallel (inference)
- Chia trọng số 1 tầng lên nhiều GPU để phục vụ model quá lớn / giảm độ trễ.

---

## 3. Knowledge Distillation (chưng cất tri thức) ⭐

Ý tưởng: model **student** nhỏ học từ model **teacher** lớn.

| Kiểu | Student học gì |
|---|---|
| **Hard-label** | Chỉ nhãn **argmax** của teacher (như nhãn cứng) |
| **Soft-label** | **Phân phối xác suất** của teacher (logits kèm **temperature**) — nhiều thông tin hơn ("dark knowledge") |
| **KL Distillation** | Cực tiểu **KL(teacher ‖ student)** trên phân phối |

**Forward KL vs Reverse KL** (đặc thù LLM):
- **Forward KL** `KL(p_teacher ‖ q_student)`: **mode-covering** — student cố phủ mọi mode → dễ sinh output nhòe/không chắc chắn với LLM.
- **Reverse KL** `KL(q_student ‖ p_teacher)`: **mode-seeking** — student tập trung vào mode chính → **tốt hơn cho LLM** (tránh trải xác suất lên vùng teacher gán ~0).
- Ví dụ: **TinyBERT**; biến thể **SLIM**; distillation mức chuỗi (sequence-level).

---

## 4. Lượng tử hóa (Quantization) ⭐⭐

Giảm số bit biểu diễn trọng số/activation (FP16 → INT8/INT4) → **giảm bộ nhớ & tăng tốc** pha memory-bound.

**Vấn đề cốt lõi:** **Outliers** trong activation → gây **sụt chất lượng** mạnh khi lượng tử hóa thô.

| Phương pháp | Ký hiệu | Ý tưởng |
|---|---|---|
| **Data-free (bitsandbytes LLM.int8())** | W8 | Nạp 8-bit trực tiếp, tách outlier ra FP16 |
| **GPTQ** | **W4A16** | Lượng tử hóa **chỉ trọng số** xuống 4-bit, theo tầng, dùng **calibration + xấp xỉ Hessian** (OBQ) |
| **SmoothQuant** | **W8A8** | Lượng tử hóa **cả trọng số & activation** 8-bit; "**smoothing**" **di chuyển độ khó** từ activation sang weight để khử outlier |

**Phân biệt (hay ra):**
- **Weight-only (GPTQ, W4A16):** giảm bộ nhớ nhiều nhất, tốt cho **decode memory-bound**, nhưng activation vẫn FP16.
- **Weight+Activation (SmoothQuant, W8A8):** tận dụng **INT8 tensor core** → nhanh cả compute; cần xử lý outlier.
- Thực nghiệm trong notebook: **naive W8A8** làm **perplexity tăng** (tệ hơn); **SmoothQuant W8A8** kéo perplexity **về gần FP16**.

**Đối chiếu bộ nhớ (từ notebook):** T5-3B FP32 ~11GB → **INT8 ~5.3GB**; lượng tử hóa 4-bit giảm >3× footprint. **Nhưng** vì decode là **memory-bound** nên nén trọng số cũng **giúp tăng tốc**, không chỉ tiết kiệm RAM.

---

## 5. Kỹ thuật giải mã nhanh khác

- **Speculative decoding** ⭐: model **nháp (draft)** nhỏ sinh nhanh vài token → model **đích (target)** lớn **kiểm tra song song** (verify) 1 lần; token khớp thì giữ. Sinh nhiều token/1 lần chạy model lớn → nhanh hơn, **giữ nguyên phân phối**.
  - **Vanilla / inference-with-reference**: dùng văn bản tham chiếu làm bản nháp.
  - **Vì sao đôi khi tệ:** nếu draft và target **lệch nhau nhiều** → tỉ lệ chấp nhận thấp + tốn thêm bộ nhớ/độ phức tạp → không lời.
- **Encoder-decoder vs Decoder-only**: cùng số tham số, cân nhắc ai nhanh hơn (encoder xử lý song song input; decoder tự hồi quy). Mẹo cho BERT (encoder) khi suy luận.

---

## 6. Bức tranh lớn
- **Pareto: Chất lượng vs Compute** — mọi kỹ thuật là đánh đổi trên đường Pareto.
- Thứ tự ưu tiên khi tối ưu suy luận: **KV cache → continuous batching → Flash/Paged Attention → quantization → speculative decoding → (tensor parallel nếu quá lớn)**.

## 7. Bẫy hay gặp trong đề
1. Nhầm **Prefill (compute-bound)** với **Decode (memory-bound)**.
2. Nhầm **TTFT** (token đầu, prefill) với **TPS** (tốc độ sinh, decode).
3. Cho rằng nén model tăng tốc **mọi** phần — chỉ giúp phần **memory-bound**.
4. Nhầm **GPTQ (W4A16, weight-only)** với **SmoothQuant (W8A8, weight+activation)**.
5. **Reverse KL** (mode-seeking) mới hợp LLM; đừng đảo với Forward KL (mode-covering).
6. Flash Attention là **chính xác** (exact), không phải attention xấp xỉ.
7. Nguồn gây khó lượng tử hóa là **outliers trong activation**.
