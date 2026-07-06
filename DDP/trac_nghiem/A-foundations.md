# TRẮC NGHIỆM — Cụm A: HPC & Song song hóa (10 câu)
Nguồn: `1-introduction`, `2_hpc`, `3_parallel-distributed-programming`.

---

**Câu 1.** Công thức **Luật Amdahl** cho tăng tốc (speedup) với phần song song hóa được `p` và `N` bộ xử lý:
- A. `S = N`
- B. `S = 1 / ((1 − p) + p/N)`
- C. `S = p·N`
- D. `S = 1 / (p + (1−p)/N)`

<details><summary>Đáp án</summary>

**B.** Phần tuần tự `(1−p)` không tăng tốc, phần song song `p` chia cho N. Đây là nền của **strong scaling**.
</details>

---

**Câu 2.** Nếu 90% chương trình song song hóa được (`p = 0.9`), tăng tốc **tối đa** khi `N → ∞` là:
- A. 9×
- B. **10×**
- C. 90×
- D. Vô hạn

<details><summary>Đáp án</summary>

**B.** `S_max = 1/(1−p) = 1/0.1 = 10`. Phần tuần tự 10% chặn trần tăng tốc — thông điệp cốt lõi của Amdahl.
</details>

---

**Câu 3.** Với `p = 0.8` và `N = 4` bộ xử lý, speedup theo Amdahl là:
- A. 4.0
- B. 3.2
- C. **2.5**
- D. 1.6

<details><summary>Đáp án</summary>

**C.** `S = 1/((1−0.8) + 0.8/4) = 1/(0.2 + 0.2) = 1/0.4 = 2.5`.
</details>

---

**Câu 4.** Đơn vị thường dùng để đo hiệu năng siêu máy tính (bảng Top500) là:
- A. Hertz (Hz)
- B. **FLOPS** (phép tính dấu phẩy động/giây)
- C. IOPS
- D. Watt

<details><summary>Đáp án</summary>

**B.** FLOPS (Peta/Exa-FLOPS). Top500 xếp hạng siêu máy tính theo FLOPS (benchmark LINPACK).
</details>

---

**Câu 5.** Theo phân loại **Flynn**, kiến trúc mà **một lệnh** tác động lên **nhiều dữ liệu** cùng lúc (VD vector, Intel SSE) là:
- A. SISD
- B. **SIMD**
- C. MISD
- D. MIMD

<details><summary>Đáp án</summary>

**B.** SIMD = Single Instruction, Multiple Data (song song mức dữ liệu). MIMD = nhiều lệnh/nhiều dữ liệu (đa nhân, cụm).
</details>

---

**Câu 6.** **Instruction-Level Parallelism (ILP)** là:
- A. Chia dữ liệu cho nhiều máy
- B. Song song hóa **các lệnh** trong một luồng (pipeline, superscalar) do phần cứng/compiler khai thác
- C. Dùng nhiều GPU
- D. Truyền thông điệp giữa các tiến trình

<details><summary>Đáp án</summary>

**B.** ILP thực thi nhiều lệnh chồng lấp trong cùng một luồng (pipelining, out-of-order, superscalar).
</details>

---

**Câu 7.** **OpenMP** phù hợp với mô hình lập trình song song nào?
- A. Bộ nhớ chia sẻ (shared memory), đa luồng trên một máy
- B. Bộ nhớ phân tán, truyền thông điệp
- C. GPU/CUDA
- D. Điện toán lượng tử

<details><summary>Đáp án</summary>

**A.** OpenMP = đa luồng trên **bộ nhớ chia sẻ** (chỉ thị `#pragma omp`). Đối lập với MPI (bộ nhớ phân tán).
</details>

---

**Câu 8.** Ghép đúng công nghệ với mô hình:
- A. MPI → bộ nhớ chia sẻ; CUDA → truyền thông điệp
- B. **MPI → truyền thông điệp (phân tán); CUDA → tăng tốc trên GPU; OpenMP → bộ nhớ chia sẻ**
- C. OpenMP → GPU; CUDA → CPU đa nhân
- D. Cả ba đều là bộ nhớ chia sẻ

<details><summary>Đáp án</summary>

**B.** Ba mô hình song song điển hình: OpenMP (shared memory), MPI (distributed message-passing), CUDA (accelerated/GPU).
</details>

---

**Câu 9.** Khi tăng số bộ xử lý, yếu tố nào **giới hạn** hiệu quả song song trên thực tế?
- A. Chỉ có phần tuần tự
- B. Phần tuần tự (Amdahl) **và** phụ phí truyền thông/đồng bộ (communication overhead)
- C. Không có yếu tố nào
- D. Chỉ có dung lượng đĩa

<details><summary>Đáp án</summary>

**B.** Ngoài trần Amdahl, **phụ phí truyền thông & đồng bộ** tăng theo số nút → hiệu quả (efficiency = speedup/N) giảm dần.
</details>

---

**Câu 10.** "Hiệu quả song song" (parallel efficiency) được định nghĩa là:
- A. `Speedup × N`
- B. **`Speedup / N`** (tăng tốc thực tế so với lý tưởng)
- C. `N / Speedup`
- D. `1 − p`

<details><summary>Đáp án</summary>

**B.** Efficiency = S/N ∈ (0,1]; = 1 nghĩa là tăng tốc tuyến tính lý tưởng. Truyền thông và phần tuần tự kéo nó xuống.
</details>
