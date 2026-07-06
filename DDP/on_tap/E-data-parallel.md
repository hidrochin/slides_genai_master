# CHEAT-SHEET — Cụm E: Data Parallelism & Distributed ML
Nguồn: `7-data-parallel-sparkml`, `7_distributed_ml`, `8-data-parallel`

---

## 1. Nền tảng: điều gì giới hạn Deep Learning trên phần cứng? (deck 8)

- **GPU vs CPU:** GPU có **FLOPS cao** và **băng thông bộ nhớ (memory bandwidth) lớn** hơn nhiều → hợp cho phép toán song song (matmul).
- **Compute-bound vs Memory-bound** ⭐:
  - *Compute-bound*: nghẽn ở khả năng tính (FLOPS) — cường độ số học cao (matmul lớn).
  - *Memory-bound*: nghẽn ở băng thông đọc/ghi bộ nhớ — cường độ số học thấp.
  - **Arithmetic intensity** = FLOPs / số byte truy cập → quyết định thuộc loại nào (mô hình **Roofline**).
- Phần cứng thay thế GPU: **FPGA** (linh hoạt, độ trễ thấp), **ASIC/TPU** (chuyên dụng, nhanh/tiết kiệm điện nhất nhưng cứng nhắc).

---

## 2. Các CHIẾN LƯỢC song song hóa (phân biệt rõ — hay ra) ⭐

| Chiến lược | Cái gì được nhân bản / chia? | Khi nào dùng |
|---|---|---|
| **Data Parallel (DP)** | **Nhân bản toàn bộ model** trên mỗi GPU; **chia dữ liệu** theo mini-batch | Model vừa 1 GPU, muốn tăng thông lượng |
| **Model Parallel** | **Chia các tầng (layer) theo chiều dọc** lên nhiều GPU | Model không vừa 1 GPU |
| **Tensor Parallel** | **Chia 1 phép toán/ma trận theo chiều ngang** (VD chia matmul theo cột) | Tầng quá lớn; cần liên kết độ trễ cực thấp (NVLink) |
| **Pipeline Parallel** | Chia theo tầng + **chia dữ liệu thành micro-batch** tạo pipeline | Model sâu, batch lớn |
| **FSDP / ZeRO** | DP nhưng **shard cả tham số/gradient/optimizer state** | Model tỉ tham số (xem cụm F) |

Ghi nhớ: **DP = chia DỮ LIỆU (model nhân bản)**; **MP/TP = chia MODEL (dữ liệu nhân bản)**.

---

## 3. Data-Parallel Training với All-Reduce (deck 7_distributed_ml, 8)

### 3.1. Vòng lặp huấn luyện DP đồng bộ (đồng bộ SGD)
Mỗi bước, trên **mỗi** GPU:
1. Nhận 1 mini-batch **khác nhau**.
2. **Forward** cục bộ → **Backward** tính gradient cục bộ.
3. **All-Reduce(gradient)** trên tất cả GPU → mọi GPU có **gradient trung bình giống nhau**.
4. **Update** optimizer state & trọng số cục bộ.

> **Q kinh điển:** *Vì sao sau bước này trọng số các GPU vẫn bằng nhau?*
> Vì khởi tạo giống nhau + sau all-reduce mọi GPU nhận **cùng gradient** → cùng bước cập nhật → trọng số luôn đồng bộ.

### 3.2. Ưu / nhược của Distributed SGD với All-Reduce
- **Ưu:** không có nút cổ chai trung tâm; băng thông cân đối; đồng bộ (hội tụ như SGD tuần tự).
- **Nhược:** phải **chờ GPU chậm nhất** (straggler); mọi GPU phải chứa **đủ toàn bộ model**; chi phí truyền thông tăng theo kích thước model.

### 3.3. Overlap computation & communication
Bắt đầu all-reduce gradient của **tầng đã backward xong** trong khi vẫn đang backward tầng khác → giấu chi phí truyền thông (gradient bucketing).

---

## 4. RING ALL-REDUCE — ⭐ TRỌNG TÂM SỐ 1 ⭐ (deck 8)

**Vấn đề của all-reduce ngây thơ:** gom hết về 1 nút → nút đó nghẽn băng thông (∝ p).

**Ring all-reduce:** xếp p GPU thành **vòng**, mỗi GPU chỉ gửi cho **hàng xóm kề**. Gồm 2 pha:
1. **Reduce-Scatter** (p−1 bước): mỗi GPU cộng dồn để cuối cùng giữ **1 mảnh tổng hoàn chỉnh**.
2. **All-Gather** (p−1 bước): truyền các mảnh tổng vòng quanh để mọi GPU có đủ.

**Công thức chi phí (phải nhớ):**
$$\text{Data truyền / GPU} = 2\cdot\frac{p-1}{p}\cdot N \;\xrightarrow{p\text{ lớn}}\; \approx 2N$$
→ **ĐỘC LẬP với số GPU p** (bandwidth-optimal). Đây là lý do ring all-reduce được dùng phổ biến (NCCL, Horovod).

Ghi nhớ: **All-Reduce = Reduce-Scatter + All-Gather** (giống hệt cơ chế FSDP).

---

## 5. Parameter Server (PS) — mô hình tập trung (deck 7_distributed_ml)

- **Server** giữ tham số toàn cục; **worker** kéo (**Pull**) tham số → tính gradient → đẩy (**Push**) gradient lên server; server cập nhật.
- Hỗ trợ **bất đồng bộ (async)**: worker không phải chờ nhau → **không bị straggler**, nhưng gradient **cũ (stale)** → có thể hại hội tụ.
- **Nhiều parameter server** để chia tải băng thông (sharding tham số).
- Dùng cho tối ưu **siêu tham số** phân tán, hệ thống rất lớn.

| | Parameter Server | All-Reduce |
|---|---|---|
| Kiến trúc | Tập trung (server–worker) | Phi tập trung (peer-to-peer) |
| Nghẽn cổ chai | Server dễ nghẽn | Không (ring bandwidth-optimal) |
| Đồng bộ | Dễ làm **async** (stale gradient) | Thường **đồng bộ** |
| Chịu lỗi/straggler | Tốt (async) | Kém (chờ nút chậm nhất) |

---

## 6. Phi tập trung & Nén truyền thông (deck 8)

- **Gossip / Decentralized SGD:** mỗi GPU chỉ trao đổi với **vài hàng xóm** (không all-reduce toàn cục) → ít truyền thông, mở rộng tốt, nhưng hội tụ chậm hơn/nhiễu hơn.
- **Stochastic Gradient Push (SGP):** biến thể gossip có hướng, dùng khi băng thông không đối xứng.
- **Gossip + All-Reduce:** kết hợp để cân bằng chất lượng và chi phí.
- **Quantized communication:** nén gradient (VD 1-bit, top-k) trước khi gửi để giảm băng thông.
- **PowerSGD:** nén gradient bằng **xấp xỉ hạng thấp (low-rank)**; kèm **Error Feedback** (giữ lại phần lỗi nén, cộng vào bước sau) để không mất hội tụ. → giảm mạnh chi phí truyền thông.

---

## 7. Distributed ML cổ điển trên Spark/MLlib (deck 7-sparkml)

- **Spark**: engine data-flow, tính toán **in-memory**, phù hợp lặp (iterative) hơn Hadoop MapReduce.
- **MLlib**: thư viện ML phân tán trên Spark (ưu điểm: tích hợp Spark SQL/Streaming/GraphX, mở rộng cụm).
- **ALS (Alternating Least Squares)** cho collaborative filtering — chiến lược phân tán:
  - *Broadcast everything* (phát toàn bộ) → *Data parallel* → *Fully parallel* (đánh đổi bộ nhớ vs truyền thông).
- **Gradient descent / Logistic regression:** phân biệt **weak scaling** (tăng dữ liệu + tăng nút, giữ tải/nút) vs **strong scaling** (cố định dữ liệu, tăng nút).
- **K-means**, **PCA** phân tán: bước gán cụm song song theo dữ liệu, cập nhật tâm cụm bằng reduce.

---

## 8. Bẫy hay gặp trong đề
1. Nhầm **Data Parallel** (chia dữ liệu) với **Model Parallel** (chia model).
2. Quên chi phí ring all-reduce ≈ **2N, độc lập p** (không phải ∝ p).
3. Cho rằng PS luôn nhanh hơn — thực ra **server dễ nghẽn**; async đổi lấy **stale gradient**.
4. Nhầm **strong scaling ↔ weak scaling**.
5. Quên **All-Reduce = Reduce-Scatter + All-Gather**.
6. Nghĩ decentralized/gossip luôn tốt hơn — nó **ít truyền thông** nhưng **hội tụ nhiễu hơn**.
