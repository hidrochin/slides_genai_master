# TRẮC NGHIỆM — Cụm F2: Suy luận hiệu quả & Lượng tử hóa (12 câu)
Ôn cùng [../on_tap/F2-inference-quantization.md](../on_tap/F2-inference-quantization.md).

---

**Câu 1.** **TTFT** (Time To First Token) chủ yếu bị quyết định bởi pha nào?
- A. Pha **prefill** (xử lý prompt)
- B. Pha decode
- C. Tải model từ đĩa
- D. Tokenize output

<details><summary>Đáp án</summary>

**A.** TTFT ≈ thời gian prefill (xử lý toàn bộ prompt để ra token đầu). Tốc độ sinh các token sau đo bằng **TPS** (decode).
</details>

---

**Câu 2.** Cặp phân loại nào ĐÚNG cho hai pha suy luận LLM?
- A. Prefill = memory-bound; Decode = compute-bound
- B. **Prefill = compute-bound; Decode = memory-bound**
- C. Cả hai đều compute-bound
- D. Cả hai đều memory-bound

<details><summary>Đáp án</summary>

**B.** Prefill xử lý nhiều token song song → compute-bound. Decode sinh 1 token/bước, đọc lại toàn bộ trọng số → memory-bound.
</details>

---

**Câu 3.** Mục đích của **KV cache** là:
- A. Nén trọng số model
- B. Lưu Key/Value đã tính để **không phải tính lại** ở mỗi bước decode (đổi bộ nhớ lấy tốc độ)
- C. Tăng độ chính xác
- D. Giảm số tham số

<details><summary>Đáp án</summary>

**B.** KV cache tránh tính lại attention cho token cũ. Nhược điểm: tốn bộ nhớ ∝ batch × seq_len × layers → dễ nghẽn.
</details>

---

**Câu 4.** **Continuous (in-flight) batching** giúp:
- A. Giảm độ chính xác để chạy nhanh
- B. **Thêm/bớt chuỗi vào batch động** khi có chỗ trống → tăng throughput
- C. Ghép nhiều GPU thành một
- D. Nén KV cache xuống 4-bit

<details><summary>Đáp án</summary>

**B.** Không phải chờ cả batch cùng xong; chuỗi xong sớm được thay bằng chuỗi mới → tận dụng GPU tốt hơn (vLLM, TGI).
</details>

---

**Câu 5.** Phát biểu nào ĐÚNG về **FlashAttention**?
- A. Là attention **xấp xỉ**, giảm độ chính xác
- B. **IO-aware, tiling, không materialize ma trận N×N**; kết quả **chính xác**, giảm bộ nhớ O(N²)→O(N)
- C. Chỉ chạy trên CPU
- D. Thay thế KV cache

<details><summary>Đáp án</summary>

**B.** FlashAttention tính attention theo khối, fuse phép toán, tránh ghi ma trận attention khổng lồ vào HBM → nhanh & tiết kiệm bộ nhớ mà **vẫn chính xác** (exact).
</details>

---

**Câu 6.** **PagedAttention** (vLLM) giải quyết vấn đề gì của KV cache?
- A. Độ trễ mạng
- B. **Phân mảnh bộ nhớ** — quản lý KV cache như bộ nhớ ảo phân trang, cho phép chia sẻ
- C. Gradient staleness
- D. Straggler

<details><summary>Đáp án</summary>

**B.** Chia KV cache thành "trang" → giảm phân mảnh, cho phép nhiều request đồng thời và chia sẻ tiền tố.
</details>

---

**Câu 7.** Phân biệt **GPTQ** và **SmoothQuant**:
- A. GPTQ = W4A16 (chỉ lượng tử hóa **trọng số** 4-bit); SmoothQuant = W8A8 (lượng tử hóa **cả trọng số & activation** 8-bit)
- B. GPTQ lượng tử hóa activation; SmoothQuant chỉ trọng số
- C. Cả hai đều là 4-bit weight-only
- D. Cả hai đều không đụng tới trọng số

<details><summary>Đáp án</summary>

**A.** GPTQ: weight-only 4-bit (W4A16), tốt cho decode memory-bound. SmoothQuant: W8A8, tận dụng INT8 tensor core, cần xử lý outlier.
</details>

---

**Câu 8.** Nguyên nhân chính khiến lượng tử hóa LLM bị **sụt chất lượng** là:
- A. Model quá nhỏ
- B. **Outliers** (giá trị ngoại lệ lớn) trong activation
- C. Learning rate cao
- D. Thiếu KV cache

<details><summary>Đáp án</summary>

**B.** Outlier biên độ lớn trong activation làm thang lượng tử hóa bị kéo giãn → mất độ phân giải. SmoothQuant "smoothing" chuyển độ khó từ activation sang weight để khử.
</details>

---

**Câu 9.** Khác biệt giữa **hard-label** và **soft-label distillation**:
- A. Hard-label học phân phối xác suất teacher; soft-label học argmax
- B. **Hard-label học argmax của teacher; soft-label học phân phối xác suất (logits + temperature)** — nhiều thông tin hơn
- C. Không khác nhau
- D. Soft-label chỉ dùng cho ảnh

<details><summary>Đáp án</summary>

**B.** Soft-label mang "dark knowledge" (quan hệ giữa các lớp) nên student học tốt hơn so với chỉ nhãn cứng (argmax).
</details>

---

**Câu 10.** Vì sao **Reverse KL** thường được ưa dùng khi distill/huấn luyện **LLM**?
- A. Vì nó **mode-covering**, phủ mọi mode
- B. Vì nó **mode-seeking** — student tập trung vào mode chính, tránh trải xác suất lên vùng teacher gán ~0
- C. Vì tính nhanh hơn Forward KL
- D. Vì không cần teacher

<details><summary>Đáp án</summary>

**B.** Reverse KL `KL(student‖teacher)` mode-seeking → sinh văn bản sắc nét/chắc chắn hơn. Forward KL mode-covering dễ làm phân phối bị nhòe.
</details>

---

**Câu 11.** **Speculative decoding** tăng tốc bằng cách:
- A. Model nháp (draft) nhỏ sinh nhanh vài token → model đích lớn **kiểm tra song song** 1 lần, giữ token khớp
- B. Bỏ bớt tầng của model
- C. Lượng tử hóa KV cache
- D. Tăng batch size

<details><summary>Đáp án</summary>

**A.** Sinh nhiều token cho mỗi lần chạy model lớn (verify song song) → nhanh hơn mà **giữ nguyên phân phối**. Kém hiệu quả khi draft và target **lệch nhau nhiều** (tỉ lệ chấp nhận thấp).
</details>

---

**Câu 12.** Trong notebook, nạp T5-3B ở 8-bit:
```python
model_8bit = AutoModelForSeq2SeqLM.from_pretrained(
    "t5-3b-sharded", device_map="auto", load_in_8bit=True)
model_8bit.get_memory_footprint() / 1e9
```
So với bản gốc ~11 GB (FP32), footprint 8-bit vào khoảng:
- A. ~11 GB (không đổi)
- B. ~5.3 GB (giảm ~một nửa)
- C. ~0.5 GB
- D. ~22 GB (tăng gấp đôi)

<details><summary>Đáp án</summary>

**B.** INT8 giảm footprint xuống ~5.3 GB (một phần layer/outlier vẫn ở fp16). Vì decode là memory-bound nên nén cũng giúp **tăng tốc**, không chỉ tiết kiệm VRAM.
</details>
