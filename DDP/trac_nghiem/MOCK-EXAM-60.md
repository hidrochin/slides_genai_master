# ĐỀ THI THỬ TỔNG HỢP — 60 câu (trộn tất cả cụm)
Huấn luyện Song song & Phân tán. Trọng số: A(7) B(11) C(6) D(5) E(13) F1(9) F2(9).
**Cách dùng:** làm hết 60 câu rồi mới tra **ĐÁP ÁN** ở cuối. Thời lượng gợi ý: ~60–75 phút.

---

**Câu 1.** Một chương trình có 20% khối lượng buộc phải chạy tuần tự. Theo Amdahl, tăng tốc **tối đa** (N→∞) là:
- A. 4× — B. 5× — C. 10× — D. Vô hạn

**Câu 2.** Thao tác MPI gửi **cùng một** dữ liệu từ root tới mọi tiến trình:
- A. `Scatter` — B. `Bcast` — C. `Gather` — D. `Reduce`

**Câu 3.** Trong Data Parallelism:
- A. Chia model, nhân bản dữ liệu — B. Nhân bản model, chia dữ liệu — C. Chia cả hai — D. Không chia gì

**Câu 4.** Huấn luyện mixed-precision FP16 + Adam tốn bao nhiêu byte **trên mỗi tham số**?
- A. 4 — B. 8 — C. 16 — D. 2

**Câu 5.** GPGPU nghĩa là:
- A. Card đồ họa chuyên game — B. General-Purpose computing on GPUs — C. Một chuẩn bộ nhớ — D. CPU tích hợp GPU

**Câu 6.** Chỉ số **TTFT** chủ yếu do pha nào quyết định?
- A. Prefill — B. Decode — C. Tokenize — D. Tải trọng số

**Câu 7.** `nn.CrossEntropyLoss` của PyTorch nên nhận đầu vào là:
- A. Xác suất sau softmax — B. Logits thô (chưa softmax) — C. Nhãn one-hot — D. Giá trị sau sigmoid

**Câu 8.** Hàm nào là **non-blocking**?
- A. `MPI_Send` — B. `MPI_Ssend` — C. `MPI_Isend` — D. `MPI_Recv`

**Câu 9.** Chi phí truyền của ring all-reduce trên p GPU (mỗi GPU) xấp xỉ:
- A. `p·N` — B. `2N`, độc lập p — C. `N/p` — D. `N·log p`

**Câu 10.** Đơn vị xếp hạng hiệu năng trong Top500:
- A. Hz — B. Watt — C. FLOPS — D. IOPS

**Câu 11.** So với ZeRO-2, **ZeRO-3** phân mảnh thêm thành phần nào?
- A. Optimizer state — B. Gradient — C. Parameter — D. Activation

**Câu 12.** Phát biểu ĐÚNG:
- A. Scatter và Gather giống nhau — B. Scatter chia dữ liệu root→các tiến trình; Gather ghép các tiến trình→root — C. Cả hai đều gộp bằng phép cộng — D. Gather là 1→all

**Câu 13.** KV cache dùng để:
- A. Nén trọng số — B. Lưu Key/Value tránh tính lại khi decode — C. Tăng độ chính xác — D. Giảm số tham số

**Câu 14.** Trong Parameter Server, worker:
- A. Pull gradient, Push tham số — B. Push gradient lên server, Pull tham số mới về — C. Chỉ gửi tham số — D. Không giao tiếp với server

**Câu 15.** Từ khóa CUDA `__global__` đánh dấu:
- A. Biến toàn cục CPU — B. Kernel gọi từ host, chạy trên device — C. Bộ nhớ chia sẻ — D. Hàm chỉ chạy CPU

**Câu 16.** `p = 0.5`, `N = 2`. Speedup theo Amdahl:
- A. 2.0 — B. 1.5 — C. 1.33 — D. 1.0

**Câu 17.** `MPI_Allreduce` khác `MPI_Reduce` ở chỗ:
- A. Chỉ dùng phép max — B. Kết quả gộp về mọi tiến trình (không chỉ root) — C. Không cần phép toán — D. Chậm hơn luôn

**Câu 18.** Quan hệ FSDP ↔ ZeRO:
- A. FSDP = ZeRO-1 — B. FSDP ≡ ZeRO-3 — C. FSDP là model-parallel — D. Không liên quan

**Câu 19.** Huấn luyện bất đồng bộ với Parameter Server dễ gặp:
- A. Gradient cũ (stale) ảnh hưởng hội tụ — B. Deadlock — C. Straggler nặng hơn đồng bộ — D. Mất mát tham số

**Câu 20.** Hàm softmax biến logits thành:
- A. Giá trị trong [−1,1] — B. Phân phối xác suất (dương, tổng = 1) — C. Nhãn cứng — D. Gradient

**Câu 21.** Cặp mô tả ĐÚNG:
- A. GPTQ = W4A16 (weight-only 4-bit); SmoothQuant = W8A8 (weight+activation) — B. GPTQ lượng tử hóa activation, SmoothQuant chỉ weight — C. Cả hai đều 4-bit weight-only — D. Cả hai không đụng weight

**Câu 22.** Với gửi đồng bộ (`Ssend`), mẫu nào **deadlock**?
- A. Hai tiến trình cùng `Ssend` cho nhau trước khi `Recv` — B. Một bên `Recv` trước — C. Dùng `Sendrecv` — D. Dùng non-blocking

**Câu 23.** Pha decode (sinh từng token) thường bị giới hạn bởi:
- A. Băng thông bộ nhớ (memory-bound) — B. FLOPS (compute-bound) — C. Đĩa — D. Số nhân CPU

**Câu 24.** GPU hợp cho DL hơn CPU chủ yếu vì:
- A. Ít nhân, xung nhịp cao — B. Rất nhiều nhân + băng thông cao → thông lượng song song lớn — C. Cache lớn hơn — D. Chạy tuần tự nhanh hơn

**Câu 25.** FSDP thuộc loại song song hóa nào?
- A. Model parallelism — B. Pipeline parallelism — C. Data parallelism có shard — D. Tensor parallelism

**Câu 26.** Kiến trúc "một lệnh, nhiều dữ liệu" (Flynn):
- A. SISD — B. SIMD — C. MISD — D. MIMD

**Câu 27.** 4 tiến trình (rank 0..3), `t = tensor([float(rank)])`, gọi `dist.all_reduce(t, SUM)`. Mỗi tiến trình in:
- A. Giá trị rank của nó — B. `tensor([6.])` ở mọi tiến trình — C. `tensor([6.])` chỉ ở rank 0 — D. `tensor([1.5])`

**Câu 28.** FlashAttention:
- A. Là attention xấp xỉ, giảm độ chính xác — B. IO-aware, tiling, không materialize N×N, kết quả chính xác — C. Chỉ chạy CPU — D. Thay thế KV cache

**Câu 29.** Thao tác mỗi tiến trình gửi **dữ liệu khác nhau** tới **từng** tiến trình khác:
- A. `Bcast` — B. `Allgather` — C. `Alltoall` — D. `Scan`

**Câu 30.** Đoạn `for i in range(B): (loss/B).backward()` rồi `optimizer.step()` là:
- A. Gradient checkpointing — B. Gradient accumulation (mô phỏng batch lớn) — C. Tensor parallel — D. LR warmup

**Câu 31.** Một **batch ảnh màu** biểu diễn bằng tensor:
- A. 2D — B. 4D (N×C×H×W) — C. 1D — D. 5D

**Câu 32.** PowerSGD giảm chi phí truyền thông bằng:
- A. Bỏ gradient nhỏ — B. Xấp xỉ hạng thấp (low-rank) + Error Feedback — C. Tăng batch — D. Lượng tử hóa weight 8-bit

**Câu 33.** Mô hình thực thi của GPU NVIDIA:
- A. SISD — B. MIMD thuần — C. SIMT — D. VLIW

**Câu 34.** Nguyên nhân chính gây sụt chất lượng khi lượng tử hóa LLM:
- A. Model nhỏ — B. Outliers trong activation — C. LR cao — D. Thiếu KV cache

**Câu 35.** One-to-all broadcast trên hypercube p nút (tối ưu) cần khoảng:
- A. p−1 bước — B. p² — C. log₂ p bước — D. √p

**Câu 36.** OpenMP phù hợp mô hình:
- A. Bộ nhớ chia sẻ, đa luồng — B. Truyền thông điệp phân tán — C. GPU — D. Lượng tử

**Câu 37.** "Straggler problem" trong DP đồng bộ:
- A. Gradient nhiễu — B. Phải chờ GPU chậm nhất mỗi bước — C. Mất mạng — D. Tràn bộ nhớ

**Câu 38.** Khác biệt GPipe vs PipeDream:
- A. GPipe có "bubble" đồng bộ; PipeDream cập nhật theo micro-batch, dùng weight stashing → gradient staleness — B. GPipe luôn nhanh hơn — C. PipeDream không dùng micro-batch — D. Giống hệt nhau

**Câu 39.** Vì sao **Reverse KL** hợp với distill LLM?
- A. Mode-covering, phủ mọi mode — B. Mode-seeking, tập trung mode chính, tránh trải xác suất lên vùng ~0 — C. Tính nhanh hơn — D. Không cần teacher

**Câu 40.** 4 tiến trình, `data=rank+1` (1,2,3,4), `total=comm.reduce(data, SUM, root=0)`; chỉ rank 0 in `total`. In ra:
- A. 10 — B. 4 — C. None — D. Lỗi

**Câu 41.** TPU là:
- A. GPU đa dụng — B. ASIC chuyên dụng (systolic array) — C. FPGA — D. CPU nhiều nhân

**Câu 42.** Decentralized/Gossip SGD đặc trưng bởi:
- A. Mỗi GPU chỉ trao đổi với vài hàng xóm (ít truyền thông, hội tụ nhiễu hơn) — B. Cần server trung tâm — C. Không trao đổi gradient — D. Luôn chính xác hơn

**Câu 43.** Gradient checkpointing đánh đổi:
- A. Thêm tính toán (tính lại activation) lấy ít bộ nhớ — B. Bộ nhớ lấy tốc độ — C. Giảm cả hai — D. Nén gradient

**Câu 44.** Hiệu quả song song (parallel efficiency) =
- A. Speedup × N — B. Speedup / N — C. N / Speedup — D. 1 − p

**Câu 45.** Về collective communication, phát biểu ĐÚNG:
- A. Chỉ một tiến trình gọi là đủ — B. Mọi tiến trình trong communicator phải cùng gọi, thiếu sẽ treo — C. Luôn non-blocking — D. Không dùng với `COMM_WORLD`

**Câu 46.** Continuous (in-flight) batching:
- A. Giảm độ chính xác — B. Thêm/bớt chuỗi vào batch động → tăng throughput — C. Ghép nhiều GPU — D. Nén KV cache

**Câu 47.** Kỹ thuật overlap computation & communication trong DDP:
- A. Tăng LR — B. All-reduce gradient tầng đã backward xong trong khi vẫn backward tầng khác — C. Dồn gradient về CPU — D. Bỏ đồng bộ

**Câu 48.** Để PyTorch tính gradient cho một tensor:
- A. `.cuda()` — B. `requires_grad=True` rồi `.backward()` — C. `torch.no_grad()` — D. `.detach()`

**Câu 49.** "Model lớn hơn GPU" — khi **một sample** cũng không vừa, giải pháp trực tiếp:
- A. Tăng batch — B. Gradient checkpointing — C. Giảm learning rate — D. Bỏ optimizer state

**Câu 50.** So sánh FPGA và ASIC:
- A. FPGA tái cấu hình/linh hoạt nhưng thường chậm hơn; ASIC nhanh/tiết kiệm điện nhất nhưng cố định — B. FPGA luôn nhanh hơn ASIC — C. ASIC lập trình lại dễ hơn — D. Giống hệt nhau

**Câu 51.** `Allreduce` thường cài đặt hiệu quả bằng:
- A. Broadcast + Scatter — B. Reduce-Scatter + All-Gather — C. Gather + Alltoall — D. Barrier + Bcast

**Câu 52.** Strong scaling là:
- A. Cố định tổng bài toán, tăng số nút để chạy nhanh hơn — B. Tăng dữ liệu tỉ lệ số nút — C. Giảm dữ liệu — D. Chỉ dùng cho CPU

**Câu 53.** Speculative decoding tăng tốc bằng:
- A. Model nháp nhỏ sinh vài token → model đích kiểm tra song song, giữ token khớp — B. Bỏ bớt tầng — C. Lượng tử hóa KV cache — D. Tăng batch

**Câu 54.** Ngoài phần tuần tự (Amdahl), yếu tố nào làm hiệu quả song song giảm khi tăng nút?
- A. Không có — B. Phụ phí truyền thông & đồng bộ — C. Dung lượng đĩa — D. Nhiệt độ phòng

**Câu 55.** Về mixed precision trong FSDP, phát biểu ĐÚNG:
- A. Chỉ hỗ trợ FP32 — B. BFloat16 được khuyến nghị và cần GPU Ampere (A100) — C. FP16 luôn nhanh hơn BF16 — D. Không hỗ trợ mixed precision

**Câu 56.** Vai trò của `DistributedSampler` trong DDP:
- A. Nén gradient — B. Bảo đảm mỗi tiến trình nhận phần dữ liệu **không trùng nhau** — C. Đồng bộ trọng số đầu — D. Tính trung bình gradient

**Câu 57.** PagedAttention (vLLM) giải quyết:
- A. Độ trễ mạng — B. Phân mảnh bộ nhớ KV cache (quản lý như bộ nhớ ảo phân trang) — C. Gradient staleness — D. Straggler

**Câu 58.** Vì sao cần MLP thay vì perceptron đơn?
- A. Perceptron chậm — B. Perceptron tuyến tính không giải được XOR; MLP + phi tuyến thì được — C. MLP không cần kích hoạt — D. Perceptron không phân loại được gì

**Câu 59.** Sau khi gọi `MPI_Isend`, để dùng lại buffer an toàn phải:
- A. Không cần làm gì — B. Gọi `MPI_Finalize` — C. Gọi `MPI_Wait`/`MPI_Test` — D. Gọi `MPI_Barrier`

**Câu 60.** Sau `all_reduce(SUM)` gradient trên N GPU, để có **gradient trung bình** cần:
- A. Nhân với N — B. Chia cho N (world_size) — C. Không làm gì — D. Lấy max

---

## ✅ ĐÁP ÁN & CỤM

| Câu | ĐA | Cụm | Câu | ĐA | Cụm | Câu | ĐA | Cụm |
|---|---|---|---|---|---|---|---|---|
| 1 | B | A | 21 | A | F2 | 41 | B | C |
| 2 | B | B | 22 | A | B | 42 | A | E |
| 3 | B | E | 23 | A | F2 | 43 | A | F1 |
| 4 | C | F1 | 24 | B | C | 44 | B | A |
| 5 | B | C | 25 | C | F1 | 45 | B | B |
| 6 | A | F2 | 26 | B | A | 46 | B | F2 |
| 7 | B | D | 27 | B | E | 47 | B | E |
| 8 | C | B | 28 | B | F2 | 48 | B | D |
| 9 | B | E | 29 | C | B | 49 | B | F1 |
| 10 | C | A | 30 | B | F1 | 50 | A | C |
| 11 | C | F1 | 31 | B | D | 51 | B | B |
| 12 | B | B | 32 | B | E | 52 | A | E |
| 13 | B | F2 | 33 | C | C | 53 | A | F2 |
| 14 | B | E | 34 | B | F2 | 54 | B | A |
| 15 | B | C | 35 | C | B | 55 | B | F1 |
| 16 | C | A | 36 | A | A | 56 | B | E |
| 17 | B | B | 37 | B | E | 57 | B | F2 |
| 18 | B | F1 | 38 | A | F1 | 58 | B | D |
| 19 | A | E | 39 | B | F2 | 59 | C | B |
| 20 | B | D | 40 | A | B | 60 | B | E |

**Thang tự chấm:** ≥54/60 (90%) vững · 45–53 (75–88%) khá, ôn lại cụm sai · <45 tập trung ôn theo cụm bị sai nhiều nhất.

### Giải thích nhanh vài câu bẫy
- **C4/C16:** 16 byte = 2(param)+2(grad)+12(Adam fp32); Amdahl `1/((1−p)+p/N)`.
- **C9/C51:** ring all-reduce ≈ 2N độc lập p; = Reduce-Scatter + All-Gather.
- **C25:** FSDP vẫn là data-parallel (shard), KHÔNG phải model-parallel.
- **C27 vs C40:** `all_reduce` → mọi tiến trình có kết quả; `reduce` → chỉ root.
- **C23/C6:** decode = memory-bound (TPS); prefill = compute-bound (TTFT).
- **C39:** Reverse KL = mode-seeking (hợp LLM).
