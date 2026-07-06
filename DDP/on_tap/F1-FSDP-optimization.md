# CHEAT-SHEET — Cụm F1: FSDP & Tối ưu mô hình lớn
Nguồn: `11-Fully Sharded Data Parallel`, `12-optimization-large-model`

---

## 1. GPU chứa những gì khi huấn luyện? (deck 11) — ⭐ NỀN TẢNG ⭐

3 thành phần (bỏ qua activation):
1. **Parameters** (tham số)
2. **Gradients**
3. **Optimizer State** (VD Adam: **momentum** m + **variance** v)

**Kế toán bộ nhớ (mixed precision FP16 + Adam), với x = số tham số:**

| Thành phần | Byte/tham số | Ghi chú |
|---|---|---|
| Parameter (fp16) | **2x** | 2 byte |
| Gradient (fp16) | **2x** | 2 byte |
| Optimizer state (fp32) | **12x** | param copy 4 + momentum 4 + variance 4 (**đều fp32**) |
| **TỔNG** | **16x** | = "2+2+12" |

→ Với model 7.5B tham số: **16 × 7.5B = 120 GB** (không vừa 1 GPU!). Đây là động lực của ZeRO/FSDP.

---

## 2. ZeRO — Bảng phân mảnh bộ nhớ ⭐⭐ (BẮT BUỘC NHỚ) ⭐⭐

K = 12 (hệ số optimizer state của Adam), Ψ = số tham số = 7.5B, N_d = 64 GPU:

| Mức | Shard cái gì | Công thức bộ nhớ/GPU | VD (Ψ=7.5B, N_d=64) |
|---|---|---|---|
| **Baseline (DDP)** | Không shard (nhân bản hết) | (2 + 2 + K)·Ψ | **120 GB** |
| **ZeRO-1 (P_os)** | Optimizer State | 2Ψ + 2Ψ + K·Ψ/N_d | **31.4 GB** |
| **ZeRO-2 (P_os+g)** | + Gradients | 2Ψ + (2+K)·Ψ/N_d | **16.6 GB** |
| **ZeRO-3 (P_os+g+p) = FSDP** | + Parameters | (2 + 2 + K)·Ψ/N_d | **1.9 GB** |

**Kết luận:** ZeRO-3/FSDP chia **toàn bộ** (param + grad + optimizer) cho N_d GPU → bộ nhớ/GPU giảm ~**N_d lần**, đổi lại **tăng chi phí truyền thông**.

---

## 3. DDP hoạt động thế nào? (nền để so với FSDP)

Mỗi GPU giữ **bản sao đầy đủ** model. Mỗi bước: Forward cục bộ → Backward cục bộ → **All-Reduce(gradient)** → Update cục bộ.
Dùng **NCCL** (NVIDIA Collective Communication Library) cho all-gather / all-reduce / reduce / reduce-scatter / broadcast / p2p, tối ưu cho **NVLink & PCIe**.

**Nhắc lại ngữ nghĩa NCCL (giống MPI):**
- **Reduce**: `out = Σ inX` tại root.
- **AllReduce**: mọi rank nhận `Σ inX`.
- **All-Gather**: `out[Y·count+i] = inY[i]` — mọi rank nhận đủ mảnh của tất cả.
- **Reduce-Scatter**: `outY = Σ_X inX[Y·count+i]` — mỗi rank nhận **1 mảnh đã reduce**.

---

## 4. FSDP là gì / KHÔNG là gì?

**FSDP ≠** Model Parallelism, Tensor Parallelism, Pipeline Parallelism.
FSDP vẫn là **Data Parallel** (mỗi GPU xử lý dữ liệu khác nhau) nhưng **shard** tham số/gradient/optimizer.

**4 thuật ngữ then chốt của FSDP:**
1. **FSDP Unit** [chia **dọc**] — đơn vị chia model: 1 layer / 1 stage / 1 nhóm `nn.Module`.
2. **Sharding** [chia **ngang**] — làm phẳng tham số của unit thành **FlatParameter** rồi cắt cho N GPU (kèm padding).
3. **All-Gather** — gom đủ tham số của unit **trước cả forward và backward**; **giải phóng mảnh của peer sau khi dùng**.
4. **Reduce-Scatter** — sau backward, gộp + chia gradient (mỗi node giữ mảnh gradient của mình).

### Luồng FSDP (1 unit):
```
[shard] → All-Gather full params → FORWARD → free peer shards
        → All-Gather full params → BACKWARD → Reduce-Scatter gradients → update local shard
```
- **Bộ nhớ FSDP** ∝ (kích thước model đã shard) + (FSDP unit lớn nhất khi materialize đầy đủ).
- **Overlap**: all-gather tham số unit kế tiếp **trong khi** đang tính unit hiện tại (giấu chi phí truyền thông).

### Dùng / không dùng FSDP
- **Nên dùng:** model tỉ tham số; chấp nhận **đánh đổi bộ nhớ lấy truyền thông**; đổi code tối thiểu (bọc `FSDP()` thay `DDP()`).
- **Không nên:** model < ~100M (dùng activation checkpointing/reversible layers); cần **BFloat16** (khuyến nghị, cần **GPU Ampere: A100/A6000**); FP16 cần `ShardedGradScaler` (chậm hơn ~4%); fine-tune một phần khó.
- **auto_wrap_policy:** `size_based` (tổng quát, kém hiệu quả) vs `transformer_auto_wrap_policy` (theo kiến trúc, hiệu quả hơn).

---

## 5. "Model lớn hơn GPU?" — thang giải pháp (deck 12) ⭐

| Mức độ | Vấn đề | Giải pháp |
|---|---|---|
| Easy | Không vừa **batch size** mong muốn | **Gradient accumulation** |
| Hard | Không vừa **1 sample** | **Gradient checkpointing** |
| Expert | Không vừa cả **tham số** | **Model/Pipeline/Tensor parallel**, **FSDP/ZeRO**, **offload**, **quantize** |

- **Gradient accumulation:** cộng dồn gradient qua B batch nhỏ rồi mới `step()` → mô phỏng batch lớn. (`(loss/B).backward()` mỗi batch, `optimizer.step()` sau vòng lặp).
- **Gradient checkpointing (rematerialization):** **không lưu** activation trung gian ở forward, **tính lại** khi backward → đổi **thêm compute** lấy **ít bộ nhớ**.

---

## 6. Model / Pipeline / Tensor Parallel (deck 12)

| Kiểu | Ý tưởng | Model size | Throughput | Ghi chú |
|---|---|---|---|---|
| **Model-parallel (naive)** | Chia layer lên các device, chạy tuần tự | O(N) | **O(1)** | Lãng phí: mỗi lúc chỉ 1 device chạy |
| **Pipeline (GPipe)** | Chia dữ liệu thành **micro-batch** tạo pipeline | O(N) | **O(n)** | Có **"bubble"** (thời gian rỗi) |
| **Pipeline (PipeDream)** | Cập nhật gradient mỗi micro-batch để tối đa throughput | O(N) | cao | **Weight stashing** để tránh **gradient staleness** |
| **Tensor-parallel** | Chia **1 phép matmul** (scatter input → partial product → **all-reduce**) | — | — | Cần **độ trễ cực thấp** (NVLink) |

**Tóm tắt model-parallel:** hợp khi model > GPU; kích thước điển hình **2–8 GPU**; phân vùng khó; **tensor parallel dễ hơn nhưng cần NVLink**; thường kết hợp gradient checkpointing.

---

## 7. Offloading & DeepSpeed/ZeRO

- **L2L (Layer-to-Layer):** để layer trên CPU, chuyển k layer sang GPU khi cần, xóa sau khi tính, **prefetch** layer kế → tiết kiệm VRAM (còn ~20–50% overhead).
- **ZeRO-Offload:** đẩy **optimizer state + gradient + cập nhật tham số** sang **CPU**; **offload song song với tính toán**; dùng gradient checkpointing + **delayed parameter update**.
- **DeepSpeed/ZeRO:** kết hợp **sharded DP + offload + chút tensor parallelism**.
  - *Multi-GPU:* pipeline model-parallel (layer lên các GPU) + sharded data-parallel (chia optimizer/tham số).
  - *Single-GPU:* model nhỏ → gradient checkpointing; model lớn → shard optimizer state (giữ tham số trên GPU).
  - **FSDP = phần lớn tính năng DeepSpeed nhưng là API native PyTorch.** Megatron-LM = triển khai theo model cụ thể.

---

## 8. Khái niệm nâng cao (deck 12)

- **Square-cube law:** `Compute = O(n_samples · n_units²)` còn `Network traffic = O(n_samples · n_units)` → **tính toán tăng nhanh hơn truyền thông** ⇒ tầng **càng lớn càng hiệu quả về truyền thông**.
- **Expert Parallelism (MoE):** **Sparsely-gated MoE** — gating network định tuyến token tới vài expert; **Switch Transformer** (experts chia trên các device, **expert capacity** = tokens/expert × **capacity factor**).
- **Automated parallelism** — cách nhìn mới:
  - **Inter-op parallelism** (≈ pipeline): **ÍT** truyền thông, **NHIỀU** thời gian rỗi.
  - **Intra-op parallelism** (≈ tensor/operator): **NHIỀU** truyền thông, **ÍT** thời gian rỗi.
  - Công cụ: **Alpa** (phân tầng: inter-op bằng Dynamic Programming + intra-op bằng ILP), RL-based / ILP-based placement.

### Sổ tay chọn chiến lược (slide cuối deck 12) — dễ ra tình huống
- Model+optimizer 16GB, activation 128GB (batch 32) → **gradient accumulation**.
- Model+optimizer 16GB, activation 16GB (batch 1) → **gradient checkpointing**.
- Model+optimizer 32GB, activation 1GB → tùy: **DDP+offload** (ít GPU, không sửa code, tiết kiệm truyền thông) / **FSDP(ZeRO)** / **Pipeline** (batch lớn, model tuần tự) / **Tensor-parallel** (cần độ trễ nhỏ nhất).
- **Mix & match:** TP trong 1 server, PP tối thiểu giữa các server, DDP giữa các nhóm.
- Không vừa nữa → **quantize** (xem cụm F2).

---

## 9. Bẫy hay gặp trong đề
1. Nhầm hệ số bộ nhớ: Adam optimizer state = **12 byte/tham số** (fp32), tổng = **16 byte/tham số**.
2. Nhầm thứ tự ZeRO: 1 = optimizer, 2 = +gradient, 3 = +parameter (**ZeRO-3 = FSDP**).
3. Cho rằng FSDP là model-parallel — **sai**, FSDP vẫn là **data-parallel có shard**.
4. FSDP forward dùng **All-Gather**, backward dùng **All-Gather + Reduce-Scatter** (không phải All-Reduce).
5. Nhầm **GPipe (có bubble)** với **PipeDream (weight stashing, gradient staleness)**.
6. Model-parallel naive có throughput **O(1)** (không phải O(n)) — pipeline mới đạt O(n).
7. Inter-op = ít comm/nhiều idle; Intra-op (tensor) = nhiều comm/ít idle — **đừng đảo ngược**.
