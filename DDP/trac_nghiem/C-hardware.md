# TRẮC NGHIỆM — Cụm C: GPU, CUDA & AI Accelerators (8 câu)
Nguồn: `5-gpgpu`, `6-ai-accelerators`, phần phần cứng của `8-data-parallel`.

---

**Câu 1.** **GPGPU** nghĩa là:
- A. GPU chỉ dùng cho đồ họa
- B. **General-Purpose computing on GPUs** — dùng GPU cho tính toán tổng quát (không chỉ đồ họa)
- C. Một loại CPU đa nhân
- D. Giao thức mạng

<details><summary>Đáp án</summary>

**B.** GPGPU = tận dụng hàng nghìn nhân GPU cho tính toán song song tổng quát (matmul, mô phỏng...), nền tảng cho CUDA.
</details>

---

**Câu 2.** Trong CUDA, từ khóa `__global__` đánh dấu:
- A. Biến toàn cục trên CPU
- B. Một **kernel** — hàm chạy trên **device (GPU)**, được gọi từ **host (CPU)**
- C. Vùng bộ nhớ chia sẻ
- D. Hàm chỉ chạy trên CPU

<details><summary>Đáp án</summary>

**B.** `__global__` = kernel gọi từ host, chạy trên device. (`__device__` = gọi & chạy trên device; `__host__` = trên CPU.)
</details>

---

**Câu 3.** Cú pháp `myKernel<<<numBlocks, threadsPerBlock>>>(...)` chỉ định:
- A. Số vòng lặp
- B. **Cấu hình lưới thực thi**: số block trong grid và số thread trong mỗi block
- C. Kích thước bộ nhớ chia sẻ bắt buộc
- D. Độ ưu tiên của kernel

<details><summary>Đáp án</summary>

**B.** GPU tổ chức thread theo **grid → block → thread**. Chỉ số toàn cục thường tính bằng `blockIdx.x * blockDim.x + threadIdx.x`.
</details>

---

**Câu 4.** Vì sao GPU phù hợp cho huấn luyện deep learning hơn CPU?
- A. GPU có ít nhân nhưng xung nhịp cao
- B. **Nhiều nhân đơn giản + băng thông bộ nhớ cao → thông lượng song song lớn** (hợp với matmul)
- C. GPU có bộ nhớ đệm lớn hơn CPU
- D. GPU chạy tuần tự nhanh hơn

<details><summary>Đáp án</summary>

**B.** CPU tối ưu độ trễ (ít nhân mạnh); GPU tối ưu **thông lượng** (rất nhiều nhân + bandwidth cao) → lý tưởng cho phép toán ma trận song song.
</details>

---

**Câu 5.** Mô hình thực thi của GPU NVIDIA thường gọi là:
- A. SISD
- B. MIMD thuần túy
- C. **SIMT** (Single Instruction, Multiple Threads) — các thread trong warp chạy cùng lệnh
- D. VLIW

<details><summary>Đáp án</summary>

**C.** SIMT: một warp (32 thread) thực thi **cùng một lệnh** trên dữ liệu khác nhau; rẽ nhánh khác nhau gây "warp divergence".
</details>

---

**Câu 6.** **TPU (Tensor Processing Unit)** thuộc loại phần cứng nào và dựa trên kiến trúc gì?
- A. GPU đa dụng
- B. **ASIC chuyên dụng cho AI**, dùng **systolic array** cho phép nhân ma trận
- C. FPGA tái cấu hình
- D. CPU nhiều nhân

<details><summary>Đáp án</summary>

**B.** TPU là ASIC (mạch chuyên dụng) của Google, dùng mảng tâm thu (systolic array) để tăng tốc matmul/convolution.
</details>

---

**Câu 7.** So sánh **FPGA** và **ASIC** làm bộ tăng tốc AI:
- A. FPGA **tái cấu hình được, linh hoạt** nhưng thường chậm/tốn điện hơn; ASIC **nhanh/tiết kiệm điện nhất** nhưng **cứng nhắc, chi phí thiết kế cao**
- B. FPGA nhanh hơn ASIC trong mọi trường hợp
- C. ASIC lập trình lại dễ hơn FPGA
- D. Hai loại giống hệt nhau

<details><summary>Đáp án</summary>

**A.** FPGA = linh hoạt (nạp lại mạch), độ trễ thấp; ASIC = hiệu năng/điện năng tốt nhất nhưng làm xong không đổi được (VD TPU).
</details>

---

**Câu 8.** Vùng bộ nhớ nào trên GPU **nhanh** và **chia sẻ giữa các thread trong cùng một block**, thường dùng để tối ưu (VD tiling)?
- A. Global memory
- B. **Shared memory**
- C. Host memory (RAM CPU)
- D. Disk

<details><summary>Đáp án</summary>

**B.** Shared memory (on-chip) nhanh hơn global memory nhiều lần, dùng chung trong block — chìa khóa tối ưu như tiling matmul, FlashAttention.
</details>
