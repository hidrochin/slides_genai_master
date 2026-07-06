# ONE-PAGER — Ôn nước rút (liếc trước giờ thi)
Huấn luyện Song song & Phân tán. Chi tiết ở: [B-MPI](B-MPI.md) · [E-data-parallel](E-data-parallel.md) · [F1-FSDP-optimization](F1-FSDP-optimization.md) · [F2-inference-quantization](F2-inference-quantization.md)

---

## 🔢 CÔNG THỨC PHẢI NHỚ

| Chủ đề | Công thức | Ghi nhớ |
|---|---|---|
| **Amdahl (speedup)** | `S = 1 / ((1−p) + p/N)` | p = phần song song hóa được; N→∞ ⇒ `S_max = 1/(1−p)` |
| **Ring all-reduce** | `data/GPU = 2·(p−1)/p·N ≈ 2N` | **Độc lập số GPU** (bandwidth-optimal) |
| **Bộ nhớ train / tham số** | fp16: **16 byte** = 2(P)+2(G)+12(Adam) | Adam optimizer state = 12 byte (fp32) |
| **ZeRO-3/FSDP mem/GPU** | `(2+2+K)·Ψ / N_d`, K=12 | Giảm ~N_d lần so với DDP |
| **Chi phí 1 thông điệp** | `t_startup + t_word · m` | Latency + băng thông |
| **Broadcast hypercube** | `log₂ p` bước | Ring = p−1 bước |
| **Square-cube law** | Compute `O(n·u²)` vs Traffic `O(n·u)` | Tầng lớn ⇒ hiệu quả truyền thông hơn |

---

## ⚖️ SO SÁNH LÕI (dễ bị lừa)

**MPI collective:** Bcast(cùng data) ≠ Scatter(chia khác) · Gather(ghép) ≠ Reduce(gộp toán) · tiền tố **All** = kết quả về mọi rank · **AllReduce = ReduceScatter + AllGather**.

**Song song hóa — chia gì?**
- **Data Parallel** = chia DỮ LIỆU, nhân bản model.
- **Model/Tensor/Pipeline** = chia MODEL, nhân bản dữ liệu.
- **FSDP/ZeRO-3** = data-parallel **có shard** cả param+grad+optimizer (KHÔNG phải model-parallel).

**PS vs All-Reduce:** PS tập trung (server dễ nghẽn, dễ async→stale) · All-Reduce phi tập trung (ring tối ưu, thường đồng bộ, sợ straggler).

**Parallel throughput:** Model-parallel naive = **O(1)** · GPipe = **O(n) nhưng có bubble** · PipeDream = weight stashing (gradient staleness).

**Inter-op (pipeline)** = ít comm / nhiều idle · **Intra-op (tensor)** = nhiều comm / ít idle.

**Quantization:** GPTQ = **W4A16** weight-only · SmoothQuant = **W8A8** weight+activation (khử **outlier** bằng smoothing).

**Distillation LLM:** Reverse KL = mode-seeking (**hợp LLM**) · Forward KL = mode-covering.

**Inference phase:** Prefill = **compute-bound** (TTFT) · Decode = **memory-bound** (TPS).

---

## 🧠 "MODEL LỚN HƠN GPU?" → thang giải pháp
batch không vừa → **grad accumulation** · 1 sample không vừa → **grad checkpointing** · param không vừa → **model/pipeline/tensor parallel + FSDP/ZeRO + offload + quantize**.

## 🔗 ZeRO stages
ZeRO-1 = shard **optimizer** · ZeRO-2 = **+gradient** · ZeRO-3 = **+parameter** (= **FSDP**).

## 🔁 FSDP luồng 1 unit
`shard → AllGather → FORWARD → free → AllGather → BACKWARD → ReduceScatter → update local`. Overlap comm/compute. Cần **BFloat16 + GPU Ampere (A100)**.

## ⚡ Tối ưu suy luận (thứ tự)
KV cache → continuous batching → Flash/Paged Attention → quantization → speculative decoding → tensor parallel.
