# TRẮC NGHIỆM — Cụm F1: FSDP & Tối ưu mô hình lớn (12 câu)
Ôn cùng [../on_tap/F1-FSDP-optimization.md](../on_tap/F1-FSDP-optimization.md).

---

**Câu 1.** Khi huấn luyện (bỏ qua activation), bộ nhớ GPU chứa **3** thành phần chính nào?
- A. Parameters, Gradients, Optimizer State
- B. Parameters, Activations, Dataset
- C. Gradients, Learning rate, Batch
- D. Weights, Biases, Loss

<details><summary>Đáp án</summary>

**A.** Parameters + Gradients + Optimizer State (VD Adam: momentum + variance). Activation thường được xét riêng.
</details>

---

**Câu 2.** Huấn luyện mixed-precision FP16 với **Adam**, tổng bộ nhớ trên **mỗi tham số** là:
- A. 4 byte
- B. 8 byte
- C. **16 byte**
- D. 2 byte

<details><summary>Đáp án</summary>

**C.** 2 (param fp16) + 2 (grad fp16) + **12** (optimizer state fp32: param copy 4 + momentum 4 + variance 4) = **16 byte/tham số**. → 7.5B tham số ≈ 120 GB.
</details>

---

**Câu 3.** Trong công thức bộ nhớ ZeRO, hệ số **K = 12** đại diện cho:
- A. Số GPU
- B. Optimizer state của Adam (fp32): bản sao tham số + momentum + variance
- C. Số tầng của model
- D. Kích thước batch

<details><summary>Đáp án</summary>

**B.** K = 12 byte/tham số cho optimizer state Adam ở fp32 (4+4+4). Baseline = (2+2+K)·Ψ.
</details>

---

**Câu 4.** Thứ tự phân mảnh của ZeRO-1, ZeRO-2, ZeRO-3 là:
- A. Parameter → Gradient → Optimizer
- B. Optimizer State → +Gradient → +Parameter
- C. Gradient → Parameter → Optimizer
- D. Cả ba đều shard giống nhau

<details><summary>Đáp án</summary>

**B.** ZeRO-1 shard **optimizer state**; ZeRO-2 thêm **gradient**; ZeRO-3 thêm **parameter**. Bộ nhớ/GPU giảm dần: 120 → 31.4 → 16.6 → 1.9 GB (Ψ=7.5B, N_d=64).
</details>

---

**Câu 5.** Phát biểu nào ĐÚNG về quan hệ FSDP và ZeRO?
- A. FSDP tương đương ZeRO-1
- B. FSDP ≡ ZeRO-3 (shard cả parameter + gradient + optimizer state)
- C. FSDP là một dạng model parallelism
- D. FSDP không liên quan tới ZeRO

<details><summary>Đáp án</summary>

**B.** **FSDP = ZeRO-3**, phần lớn tính năng của DeepSpeed nhưng là API native PyTorch.
</details>

---

**Câu 6.** FSDP thuộc loại song song hóa nào? (bẫy)
- A. Model parallelism
- B. Pipeline parallelism
- C. **Data parallelism có shard** tham số/gradient/optimizer
- D. Tensor parallelism

<details><summary>Đáp án</summary>

**C.** FSDP vẫn là **data-parallel** (mỗi GPU xử lý dữ liệu khác nhau), chỉ khác là **shard** trạng thái model thay vì nhân bản. Slide nêu rõ FSDP **KHÔNG** phải model/tensor/pipeline parallel.
</details>

---

**Câu 7.** Trong FSDP, thao tác truyền thông ở **forward** và **backward** lần lượt là:
- A. Forward: All-Reduce; Backward: Broadcast
- B. Forward: All-Gather; Backward: All-Gather + Reduce-Scatter
- C. Forward: Scatter; Backward: Gather
- D. Không cần truyền thông

<details><summary>Đáp án</summary>

**B.** Trước forward và backward đều **All-Gather** để dựng đủ tham số của unit; sau backward dùng **Reduce-Scatter** để gộp+chia gradient. (Khác DDP dùng All-Reduce.)
</details>

---

**Câu 8.** Đánh đổi cốt lõi khi chuyển từ DDP sang FSDP là:
- A. Giảm bộ nhớ/GPU nhưng **tăng chi phí truyền thông** giữa GPU
- B. Tăng bộ nhớ nhưng giảm truyền thông
- C. Không đánh đổi gì
- D. Giảm cả bộ nhớ lẫn truyền thông

<details><summary>Đáp án</summary>

**A.** "Trade memory for time": shard giúp chứa model tỉ tham số, đổi lại all-gather/reduce-scatter thêm truyền thông. Overlap comm/compute để giảm nhẹ.
</details>

---

**Câu 9.** **Model-parallel naive** (chia tầng, chạy tuần tự) có thông lượng (throughput) là:
- A. O(n) — tỉ lệ số thiết bị
- B. **O(1)** — mỗi lúc chỉ một thiết bị hoạt động
- C. O(log n)
- D. O(n²)

<details><summary>Đáp án</summary>

**B.** Naive model-parallel lãng phí: các device chờ nhau → throughput O(1). **Pipeline (GPipe)** chia micro-batch mới nâng lên **O(n)** (nhưng có "bubble").
</details>

---

**Câu 10.** Khác biệt chính giữa **GPipe** và **PipeDream**:
- A. GPipe có "bubble" (idle) do đồng bộ; PipeDream cập nhật theo micro-batch, dùng weight stashing → có **gradient staleness**
- B. GPipe nhanh hơn PipeDream trong mọi trường hợp
- C. PipeDream không dùng micro-batch
- D. Cả hai giống hệt nhau

<details><summary>Đáp án</summary>

**A.** GPipe: pipeline đồng bộ, có bong bóng rỗng. PipeDream: cập nhật liên tục để tối đa throughput, phải lưu nhiều phiên bản trọng số (**weight stashing**) → **stale gradient**.
</details>

---

**Câu 11.** Đoạn code sau minh hoạ kỹ thuật gì và tác dụng?
```python
optimizer.zero_grad()
for i in range(B):                 # B micro-batch
    loss = model(next_batch())
    (loss / B).backward()          # cộng dồn gradient
optimizer.step()
```
- A. Gradient checkpointing — tiết kiệm compute
- B. **Gradient accumulation** — mô phỏng batch lớn khi VRAM không đủ (đổi thời gian lấy bộ nhớ)
- C. Tensor parallelism
- D. Learning-rate warmup

<details><summary>Đáp án</summary>

**B.** Cộng dồn gradient qua B micro-batch rồi mới `step()` → batch hiệu dụng lớn hơn mà không tăng VRAM. Chia `loss/B` để lấy trung bình.
</details>

---

**Câu 12.** **Gradient checkpointing (rematerialization)** đánh đổi thế nào?
- A. Đổi thêm **tính toán** (tính lại activation lúc backward) lấy **ít bộ nhớ** hơn
- B. Đổi bộ nhớ lấy tốc độ
- C. Giảm cả tính toán và bộ nhớ
- D. Nén gradient để giảm truyền thông

<details><summary>Đáp án</summary>

**A.** Không lưu activation trung gian ở forward, **tính lại** khi backward → tốn thêm compute nhưng giảm mạnh bộ nhớ (dùng khi 1 sample không vừa GPU).
</details>
