# TRẮC NGHIỆM — Cụm B: MPI & Truyền thông điệp (15 câu)
Ôn cùng [../on_tap/B-MPI.md](../on_tap/B-MPI.md). Bấm "Đáp án" để mở.

---

**Câu 1.** Đặc điểm cốt lõi phân biệt mô hình truyền thông điệp (MPI) với mô hình bộ nhớ chia sẻ (OpenMP) là:
- A. MPI luôn nhanh hơn OpenMP
- B. Mỗi tiến trình MPI có bộ nhớ riêng, chỉ trao đổi dữ liệu qua gửi/nhận thông điệp
- C. MPI chỉ chạy trên một máy
- D. OpenMP không hỗ trợ đa luồng

<details><summary>Đáp án</summary>

**B.** MPI = bộ nhớ phân tán (private memory/process), trao đổi bằng send/recv. OpenMP = bộ nhớ chia sẻ (dùng chung biến giữa các luồng).
</details>

---

**Câu 2.** `MPI_COMM_WORLD` là gì?
- A. Số thứ tự của tiến trình gốc
- B. Một kiểu dữ liệu MPI
- C. Communicator mặc định chứa **tất cả** tiến trình khi khởi động
- D. Hàm khởi tạo môi trường MPI

<details><summary>Đáp án</summary>

**C.** Là communicator mặc định gồm toàn bộ tiến trình. `rank` được đánh trong phạm vi một communicator.
</details>

---

**Câu 3.** Đoạn `mpi4py` sau chạy với 4 tiến trình in ra gì (mỗi tiến trình một dòng)?
```python
from mpi4py import MPI
comm = MPI.COMM_WORLD
print(comm.Get_rank(), "of", comm.Get_size())
```
- A. `0 of 1` bốn lần
- B. `0 of 4`, `1 of 4`, `2 of 4`, `3 of 4` (thứ tự bất kỳ)
- C. `4 of 4` bốn lần
- D. Lỗi vì thiếu `MPI_Init`

<details><summary>Đáp án</summary>

**B.** `Get_rank()` = 0..3 (định danh riêng), `Get_size()` = 4 (tổng số tiến trình). Thứ tự in **không xác định**. (mpi4py tự gọi Init.)
</details>

---

**Câu 4.** Hàm nào là **non-blocking**?
- A. `MPI_Send` / `MPI_Recv`
- B. `MPI_Ssend`
- C. `MPI_Isend` / `MPI_Irecv`
- D. `MPI_Barrier`

<details><summary>Đáp án</summary>

**C.** Tiền tố **I** (Immediate) = non-blocking, trả về ngay, phải gọi `MPI_Wait`/`MPI_Test` để hoàn tất. Lợi ích: chồng lấp tính toán & truyền thông.
</details>

---

**Câu 5.** `MPI_Ssend` (synchronous send) chỉ hoàn tất khi:
- A. Dữ liệu đã được copy vào buffer nội bộ
- B. Bên nhận đã bắt đầu nhận (bắt tay)
- C. Ngay lập tức, không cần điều kiện
- D. Sau khi gọi `MPI_Finalize`

<details><summary>Đáp án</summary>

**B.** Synchronous = bắt tay: send xong khi recv tương ứng đã khởi động. (Buffered `Bsend` mới trả về ngay sau khi copy vào buffer.)
</details>

---

**Câu 6.** Với 2 tiến trình, giả sử dùng **gửi đồng bộ** (`Ssend`), đoạn nào có nguy cơ **deadlock**?
```
# Cách 1                     # Cách 2
if rank==0:                  if rank==0:
    Ssend(dest=1)                Ssend(dest=1); Recv(src=1)
    Recv(src=1)              else:
else:                            Recv(src=0); Ssend(dest=0)
    Ssend(dest=0)
    Recv(src=0)
```
- A. Chỉ Cách 1
- B. Chỉ Cách 2
- C. Cả hai an toàn
- D. Cả hai deadlock

<details><summary>Đáp án</summary>

**A.** Cách 1: cả hai `Ssend` trước, mỗi bên chờ bên kia `Recv` → treo. Cách 2: rank 1 `Recv` trước nên rank 0 `Ssend` thoát được → không deadlock. Sửa Cách 1 bằng `MPI_Sendrecv`, đảo thứ tự, hoặc non-blocking.
</details>

---

**Câu 7.** `MPI_Bcast` thực hiện:
- A. Chia mảng thành p phần khác nhau gửi mỗi tiến trình
- B. Root gửi **cùng một** dữ liệu tới tất cả tiến trình
- C. Gộp dữ liệu từ mọi tiến trình về root
- D. Đồng bộ tất cả tiến trình

<details><summary>Đáp án</summary>

**B.** Broadcast = 1→all, **cùng** dữ liệu. (A là `Scatter`, C là `Gather/Reduce`, D là `Barrier`.)
</details>

---

**Câu 8.** Khác nhau chính giữa `MPI_Scatter` và `MPI_Gather`:
- A. Không khác gì
- B. Scatter chia dữ liệu root → các tiến trình; Gather ghép dữ liệu các tiến trình → root
- C. Scatter đồng bộ, Gather bất đồng bộ
- D. Scatter dùng cho số nguyên, Gather cho số thực

<details><summary>Đáp án</summary>

**B.** Chúng **ngược chiều** nhau: Scatter phân tán (1→all, mỗi phần khác nhau), Gather thu thập (all→1, ghép nối).
</details>

---

**Câu 9.** Điểm khác biệt giữa `MPI_Reduce` và `MPI_Allreduce`:
- A. Allreduce chỉ dùng phép cộng
- B. Reduce đưa kết quả về **root**; Allreduce đưa kết quả gộp về **mọi** tiến trình
- C. Reduce nhanh hơn Allreduce trong mọi trường hợp
- D. Allreduce không cần chỉ định phép toán

<details><summary>Đáp án</summary>

**B.** `Allreduce = Reduce + Bcast` → mọi tiến trình có kết quả. Đây là thao tác lõi của huấn luyện data-parallel đồng bộ.
</details>

---

**Câu 10.** Thao tác nào cho phép **mỗi** tiến trình gửi **dữ liệu khác nhau** tới **từng** tiến trình còn lại (giống chuyển vị ma trận)?
- A. `MPI_Bcast`
- B. `MPI_Allgather`
- C. `MPI_Alltoall`
- D. `MPI_Scan`

<details><summary>Đáp án</summary>

**C.** `Alltoall`: tiến trình i gửi khối j riêng cho tiến trình j. (`Allgather` = mọi người nhận **cùng** mảng ghép; `Scan` = quét tiền tố.)
</details>

---

**Câu 11.** Với 4 tiến trình, `data = rank + 1` (tức 1,2,3,4). Kết quả in?
```python
total = comm.reduce(data, op=MPI.SUM, root=0)
if comm.Get_rank() == 0:
    print(total)
```
- A. In `10` ở tiến trình 0
- B. In `10` ở cả 4 tiến trình
- C. In `4`
- D. Lỗi

<details><summary>Đáp án</summary>

**A.** `Reduce(SUM)` gộp 1+2+3+4 = 10, chỉ **root (rank 0)** có kết quả (các tiến trình khác nhận `None`). Nếu muốn mọi tiến trình có 10 → dùng `allreduce`.
</details>

---

**Câu 12.** Phát biểu nào **ĐÚNG** về truyền thông cộng tác (collective)?
- A. Chỉ cần một tiến trình gọi là đủ
- B. **Tất cả** tiến trình trong communicator phải cùng gọi, nếu thiếu sẽ treo
- C. Collective luôn là non-blocking
- D. Collective không dùng được với `MPI_COMM_WORLD`

<details><summary>Đáp án</summary>

**B.** Mọi tiến trình phải tham gia; thiếu một tiến trình gọi `Bcast/Reduce/Barrier...` → deadlock.
</details>

---

**Câu 13.** Trên topology **hypercube (siêu lập phương)** p nút, one-to-all broadcast cần khoảng bao nhiêu bước (tối ưu)?
- A. p − 1
- B. p²
- C. log₂ p
- D. √p

<details><summary>Đáp án</summary>

**C.** Hypercube dùng recursive doubling → `log₂ p` bước (nhân đôi số nút "đã biết" mỗi bước). Ring cần `p − 1` bước (chậm hơn khi p lớn).
</details>

---

**Câu 14.** `MPI_Allreduce` thường được cài đặt hiệu quả bằng tổ hợp nào?
- A. Broadcast + Scatter
- B. Reduce-Scatter + All-Gather
- C. Gather + Alltoall
- D. Barrier + Bcast

<details><summary>Đáp án</summary>

**B.** `Allreduce = Reduce-Scatter + All-Gather` — đây cũng chính là cơ chế **ring all-reduce** (bandwidth-optimal) và của FSDP.
</details>

---

**Câu 15.** Chi phí truyền **một** thông điệp kích thước m trong MPI thường mô hình hóa là:
- A. `t_startup` (chỉ độ trễ, không phụ thuộc m)
- B. `t_word · m` (chỉ băng thông)
- C. `t_startup + t_word · m` (độ trễ khởi tạo + thời gian/byte × kích thước)
- D. `m / p`

<details><summary>Đáp án</summary>

**C.** Latency `t_s` cố định + phần truyền `t_w·m` theo kích thước. Vì có `t_s`, gộp nhiều thông điệp nhỏ thành một thông điệp lớn thường lợi hơn.
</details>
