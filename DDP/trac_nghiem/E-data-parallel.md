# TRẮC NGHIỆM — Cụm E: Data Parallelism & Distributed ML (15 câu)
Ôn cùng [../on_tap/E-data-parallel.md](../on_tap/E-data-parallel.md).

---

**Câu 1.** Trong **Data Parallelism**, cái gì được nhân bản và cái gì được chia?
- A. Chia model, nhân bản dữ liệu
- B. Nhân bản model (mỗi GPU 1 bản), chia dữ liệu theo mini-batch
- C. Chia cả model và dữ liệu
- D. Không chia gì cả

<details><summary>Đáp án</summary>

**B.** DP = **nhân bản model**, **chia dữ liệu**. Ngược lại, Model/Tensor Parallel = chia model, nhân bản dữ liệu.
</details>

---

**Câu 2.** Chi phí truyền dữ liệu của **ring all-reduce** trên p GPU (mỗi GPU) xấp xỉ:
- A. `p · N` (tăng tuyến tính theo số GPU)
- B. `2·(p−1)/p · N ≈ 2N`, **độc lập** số GPU
- C. `N / p`
- D. `log₂ p · N`

<details><summary>Đáp án</summary>

**B.** Ring all-reduce là **bandwidth-optimal**: dữ liệu/GPU ≈ 2N không phụ thuộc p → mở rộng tốt. Đó là lý do NCCL/Horovod dùng nó.
</details>

---

**Câu 3.** Ring all-reduce gồm hai pha nào?
- A. Broadcast + Gather
- B. Scatter + Barrier
- C. Reduce-Scatter + All-Gather
- D. Push + Pull

<details><summary>Đáp án</summary>

**C.** Pha 1 Reduce-Scatter (mỗi GPU giữ 1 mảnh tổng), pha 2 All-Gather (lan truyền mảnh tổng cho mọi GPU).
</details>

---

**Câu 4.** Trong data-parallel đồng bộ, vì sao trọng số các GPU **vẫn bằng nhau** sau mỗi bước?
- A. Vì các GPU dùng chung bộ nhớ
- B. Vì khởi tạo giống nhau + all-reduce cho **cùng gradient** → cùng bước cập nhật
- C. Vì có parameter server đồng bộ
- D. Vì mỗi GPU xử lý cùng một dữ liệu

<details><summary>Đáp án</summary>

**B.** Cùng trọng số ban đầu + cùng gradient (sau all-reduce) ⇒ cùng update ⇒ luôn đồng bộ. (Mỗi GPU xử lý dữ liệu **khác nhau**.)
</details>

---

**Câu 5.** Trong mô hình **Parameter Server**, thao tác **Push** và **Pull** của worker là:
- A. Push = kéo tham số về, Pull = đẩy gradient lên
- B. Push = đẩy gradient lên server, Pull = kéo tham số mới về
- C. Cả hai đều gửi gradient
- D. Cả hai đều gửi tham số

<details><summary>Đáp án</summary>

**B.** Worker **Pull** tham số → tính gradient → **Push** gradient lên server → server cập nhật tham số toàn cục.
</details>

---

**Câu 6.** Nhược điểm chính của Parameter Server so với ring all-reduce là:
- A. Không hỗ trợ bất đồng bộ
- B. Server dễ trở thành **nút nghẽn băng thông**
- C. Không dùng được nhiều GPU
- D. Luôn hội tụ chậm hơn

<details><summary>Đáp án</summary>

**B.** Băng thông dồn về server → nghẽn (giảm bằng nhiều PS). Ring all-reduce phi tập trung nên tránh được.
</details>

---

**Câu 7.** Huấn luyện **bất đồng bộ (async)** với Parameter Server có đặc điểm:
- A. Không có straggler nhưng gradient có thể **cũ (stale)**, ảnh hưởng hội tụ
- B. Luôn hội tụ nhanh và ổn định hơn đồng bộ
- C. Bắt buộc mọi worker chờ nhau
- D. Không cần server

<details><summary>Đáp án</summary>

**A.** Async: worker không chờ nhau (chịu lỗi/straggler tốt) nhưng dùng **stale gradient** → có thể hại chất lượng/hội tụ.
</details>

---

**Câu 8.** Trong data-parallel **đồng bộ**, "straggler problem" nghĩa là:
- A. Gradient bị nhiễu
- B. Toàn hệ thống phải **chờ GPU chậm nhất** ở mỗi bước all-reduce
- C. Mất kết nối mạng
- D. Bộ nhớ GPU bị tràn

<details><summary>Đáp án</summary>

**B.** Rào đồng bộ khiến tốc độ bị giới hạn bởi nút chậm nhất. Async/decentralized giảm nhẹ vấn đề này.
</details>

---

**Câu 9.** Pha **decode** (sinh từng token) của suy luận, và nhìn rộng hơn nhiều thao tác batch nhỏ, thường bị giới hạn bởi:
- A. Băng thông bộ nhớ (memory-bound)
- B. Khả năng tính toán FLOPS (compute-bound)
- C. Dung lượng đĩa
- D. Số nhân CPU

<details><summary>Đáp án</summary>

**A.** Cường độ số học thấp → **memory-bound**. Matmul lớn / prefill / training mới là **compute-bound**. (Xem Roofline.)
</details>

---

**Câu 10.** **Decentralized SGD / Gossip** khác all-reduce toàn cục ở chỗ:
- A. Mỗi GPU chỉ trao đổi với **vài hàng xóm** → ít truyền thông, nhưng hội tụ nhiễu hơn
- B. Cần một server trung tâm
- C. Không trao đổi gradient
- D. Luôn cho độ chính xác cao hơn

<details><summary>Đáp án</summary>

**A.** Gossip = trao đổi cục bộ với lân cận → giảm chi phí truyền thông, mở rộng tốt, nhưng đồng bộ yếu hơn nên hội tụ nhiễu/chậm hơn.
</details>

---

**Câu 11.** **PowerSGD** giảm chi phí truyền thông bằng cách:
- A. Bỏ qua gradient nhỏ
- B. Nén gradient bằng **xấp xỉ hạng thấp (low-rank)**, kèm **Error Feedback**
- C. Tăng kích thước batch
- D. Dùng số nguyên 8-bit cho trọng số

<details><summary>Đáp án</summary>

**B.** PowerSGD nén gradient thành ma trận hạng thấp; **Error Feedback** giữ lại phần lỗi nén cộng vào bước sau để không mất hội tụ.
</details>

---

**Câu 12.** Kỹ thuật **overlap computation & communication** trong DP đồng bộ là:
- A. Tăng learning rate
- B. Bắt đầu all-reduce gradient của tầng **đã backward xong** trong khi vẫn đang backward tầng khác
- C. Dồn toàn bộ gradient về CPU
- D. Bỏ đồng bộ giữa các GPU

<details><summary>Đáp án</summary>

**B.** Gradient bucketing: giấu chi phí truyền thông sau tính toán → giảm thời gian mỗi bước. (Cơ chế của `DistributedDataParallel`.)
</details>

---

**Câu 13.** Chạy với 4 tiến trình, backend `gloo`. Mỗi tiến trình in gì?
```python
import torch, torch.distributed as dist
# ... đã init_process_group ...
t = torch.tensor([float(dist.get_rank())])   # [0], [1], [2], [3]
dist.all_reduce(t, op=dist.ReduceOp.SUM)
print(t)
```
- A. Mỗi tiến trình in giá trị rank của nó
- B. Mọi tiến trình đều in `tensor([6.])`
- C. Chỉ rank 0 in `tensor([6.])`
- D. In `tensor([1.5])` (trung bình)

<details><summary>Đáp án</summary>

**B.** `all_reduce(SUM)` = 0+1+2+3 = 6, và **mọi** tiến trình nhận kết quả → tất cả in `tensor([6.])`. (Muốn trung bình thì chia cho world_size.)
</details>

---

**Câu 14.** Phân biệt **strong scaling** và **weak scaling**:
- A. Strong: cố định tổng dữ liệu, tăng số nút; Weak: tăng dữ liệu tỉ lệ với số nút (giữ tải/nút)
- B. Strong: tăng dữ liệu; Weak: giảm dữ liệu
- C. Không khác nhau
- D. Strong dùng cho CPU, Weak cho GPU

<details><summary>Đáp án</summary>

**A.** Strong scaling = bài toán cố định, thêm nút để chạy nhanh hơn (bị Amdahl chặn). Weak scaling = tăng quy mô bài toán cùng số nút.
</details>

---

**Câu 15.** Trong PyTorch DDP, vai trò của `DistributedSampler` là:
- A. Nén gradient trước khi gửi
- B. Bảo đảm mỗi tiến trình nhận **phần dữ liệu không trùng nhau** của dataset
- C. Đồng bộ trọng số ban đầu
- D. Tính trung bình gradient

<details><summary>Đáp án</summary>

**B.** `DistributedSampler` chia dataset để mỗi GPU thấy một tập con khác nhau (đúng tinh thần data-parallel). Việc trung bình gradient do `all_reduce` trong DDP lo.
</details>
