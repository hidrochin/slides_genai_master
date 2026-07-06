# TRẮC NGHIỆM — Cụm D: PyTorch & Nền tảng Deep Learning (8 câu)
Nguồn: `9-PyTorch-basics`, `10-Training-Multilayer-Neural-Networks`.

---

**Câu 1.** Một **ảnh màu** (color image) được biểu diễn tự nhiên bằng tensor mấy chiều, và một **batch ảnh màu**?
- A. 2D và 3D
- B. **3D (H×W×C) và 4D (N×C×H×W)**
- C. 1D và 2D
- D. 4D và 5D

<details><summary>Đáp án</summary>

**B.** Scalar 0D, vector 1D, ma trận 2D, ảnh màu 3D (chồng các kênh), **batch ảnh 4D**. PyTorch quy ước `N×C×H×W`.
</details>

---

**Câu 2.** Trong PyTorch, để autograd theo dõi phép tính và tính gradient cho một tensor, ta cần:
- A. `tensor.cuda()`
- B. **`requires_grad=True`** (rồi gọi `.backward()`)
- C. `torch.no_grad()`
- D. `tensor.detach()`

<details><summary>Đáp án</summary>

**B.** `requires_grad=True` xây **computation graph**; `.backward()` lan truyền ngược. `no_grad()`/`detach()` **tắt** theo dõi (dùng khi suy luận).
</details>

---

**Câu 3.** Hàm **softmax** làm gì với vector logits đầu ra?
- A. Chuẩn hóa về giá trị trong [−1, 1]
- B. **Biến logits thành phân phối xác suất** (dương, tổng = 1)
- C. Lấy giá trị lớn nhất
- D. Tính đạo hàm

<details><summary>Đáp án</summary>

**B.** Softmax = exp/Σexp → xác suất các lớp, tổng bằng 1. Dùng cho phân loại đa lớp.
</details>

---

**Câu 4.** Trong PyTorch, `nn.CrossEntropyLoss` nhận đầu vào là gì? (bẫy hay gặp)
- A. Xác suất đã qua softmax
- B. **Logits thô** (chưa softmax) — vì CrossEntropyLoss **đã gồm** log-softmax bên trong
- C. Nhãn one-hot
- D. Giá trị đã qua sigmoid

<details><summary>Đáp án</summary>

**B.** `CrossEntropyLoss = LogSoftmax + NLLLoss`. **Không** tự softmax trước → tránh softmax hai lần gây sai/số học kém ổn định.
</details>

---

**Câu 5.** Vì sao cần **mạng nhiều tầng (MLP)** thay vì perceptron đơn?
- A. Perceptron chạy chậm hơn
- B. **Perceptron đơn (tuyến tính) không giải được bài toán phi tuyến như XOR**; MLP + hàm kích hoạt phi tuyến thì được
- C. MLP không cần hàm kích hoạt
- D. Perceptron không phân loại được

<details><summary>Đáp án</summary>

**B.** XOR không tách tuyến tính → cần tầng ẩn + phi tuyến (ReLU...). Đây là động lực kinh điển của MLP.
</details>

---

**Câu 6.** Trong `DataLoader`, tham số `num_workers > 0` có tác dụng:
- A. Tăng learning rate
- B. **Dùng nhiều tiến trình con để nạp/tiền xử lý dữ liệu song song** (giấu độ trễ I/O)
- C. Chia model lên nhiều GPU
- D. Nén dữ liệu

<details><summary>Đáp án</summary>

**B.** `num_workers` nạp batch song song bằng nhiều process → tránh nghẽn khi GPU chờ dữ liệu. (`drop_last=True` bỏ batch lẻ cuối.)
</details>

---

**Câu 7.** Vì sao dùng **nhân ma trận (matmul)** thay cho vòng lặp Python khi tính net input của một tầng?
- A. Kết quả chính xác hơn về mặt toán học
- B. **Nhanh hơn nhiều nhờ vector hóa / tận dụng BLAS & GPU** (song song)
- C. Tốn ít bộ nhớ hơn luôn
- D. Không có khác biệt

<details><summary>Đáp án</summary>

**B.** Vòng lặp Python rất chậm; matmul được vector hóa, chạy trên BLAS/GPU song song → nhanh hơn hàng chục–trăm lần (benchmark trong slide 9).
</details>

---

**Câu 8.** Với **cùng ngân sách tham số**, mạng **sâu & hẹp** so với **nông & rộng** thường:
- A. Luôn kém hơn
- B. **Học được đặc trưng phân cấp tốt hơn**, nhưng khó huấn luyện hơn (cần khởi tạo/chuẩn hóa tốt)
- C. Không khác biệt gì
- D. Không cần hàm kích hoạt

<details><summary>Đáp án</summary>

**B.** Mạng sâu biểu diễn hàm phức tạp hiệu quả hơn (phân cấp đặc trưng) nhưng dễ gặp vanishing gradient → cần **khởi tạo trọng số** & kỹ thuật huấn luyện phù hợp.
</details>
