# CHEAT-SHEET — Cụm B: MPI & Truyền thông điệp
Nguồn: `4.1-MPI`, `4.2-Point-to-point`, `4.3-Collective Communication`

---

## 1. Mô hình truyền thông điệp (Message Passing Model)

- Mỗi tiến trình có **bộ nhớ riêng** (private memory), **không chia sẻ bộ nhớ** → trao đổi dữ liệu duy nhất qua **gửi/nhận thông điệp** (send/receive).
- Đối lập với mô hình **shared memory** (OpenMP): shared memory dùng chung biến, MPI thì không.
- Định danh tiến trình bằng **rank**; nhóm tiến trình + ngữ cảnh truyền thông = **communicator**.

**Khái niệm cốt lõi (hay hỏi định nghĩa):**

| Thuật ngữ | Ý nghĩa |
|---|---|
| **Communicator** | Nhóm tiến trình có thể truyền thông với nhau. Mặc định: `MPI_COMM_WORLD` (tất cả). |
| **Rank** | Số định danh (0..p-1) của tiến trình trong 1 communicator. |
| **Size** | Tổng số tiến trình trong communicator (`MPI_Comm_size`). |
| **Tag** | Nhãn phân biệt các thông điệp giữa cùng cặp tiến trình. |
| **MPI datatype** | Kiểu dữ liệu MPI (`MPI_INT`, `MPI_FLOAT`, `MPI_DOUBLE`, `MPI_CHAR`...) — không dùng kiểu C trực tiếp. |

**6 hàm "xương sống" của mọi chương trình MPI:**
`MPI_Init` → `MPI_Comm_size` → `MPI_Comm_rank` → (Send/Recv...) → `MPI_Finalize`.
Giá trị trả về `MPI_SUCCESS` nếu thành công.

> **Khi nào dùng MPI:** bài toán lớn chạy trên cụm nhiều node (distributed memory), cần khả năng mở rộng.
> **Khi nào KHÔNG:** bài toán nhỏ, chỉ 1 máy nhiều nhân (dùng OpenMP đơn giản hơn), hoặc quá nhiều truyền thông nhỏ lẻ.

---

## 2. Truyền thông ĐIỂM–ĐIỂM (Point-to-point) — deck 4.2

Giữa **đúng 2 tiến trình**: một `Send`, một `Recv`.

### 2.1. Blocking vs Non-blocking (RẤT hay ra)

| | Blocking | Non-blocking |
|---|---|---|
| Hàm | `MPI_Send`, `MPI_Recv` | `MPI_Isend`, `MPI_Irecv` (I = Immediate) |
| Hành vi | Trả về khi **buffer an toàn để tái sử dụng** | Trả về **ngay lập tức**, chưa chắc xong |
| Đồng bộ | Cần | Phải gọi `MPI_Wait`/`MPI_Test` để hoàn tất |
| Lợi ích | Đơn giản | **Chồng lấp (overlap) tính toán & truyền thông** |

### 2.2. Bốn chế độ gửi (send modes)

| Chế độ | Hàm | Hoàn tất khi... |
|---|---|---|
| **Standard** | `MPI_Send` | MPI tự quyết định có đệm hay không |
| **Buffered** | `MPI_Bsend` | Copy vào buffer người dùng → trả về ngay |
| **Synchronous** | `MPI_Ssend` | **Chỉ xong khi bên nhận đã bắt đầu nhận** (bắt tay) |
| **Ready** | `MPI_Rsend` | Giả định bên nhận **đã post `Recv`** từ trước |

### 2.3. DEADLOCK — bẫy kinh điển

Hai tiến trình cùng `MPI_Send` cho nhau **trước khi** `MPI_Recv`, nếu send ở chế độ đồng bộ/không đủ buffer → **treo (deadlock)**.
**Cách khắc phục:** đảo thứ tự Send/Recv giữa 2 bên; dùng `MPI_Sendrecv`; dùng non-blocking (`Isend`/`Irecv`); dùng buffered send.

Tiện ích: `MPI_Sendrecv`, `MPI_Status`, wildcard `MPI_ANY_SOURCE`, `MPI_ANY_TAG`.

---

## 3. Truyền thông CỘNG TÁC (Collective) — deck 4.3

Có sự tham gia của **TẤT CẢ** tiến trình trong communicator. Mọi tiến trình phải cùng gọi.

### 3.1. Bảng ngữ nghĩa thao tác — ⭐ TRỌNG TÂM TRẮC NGHIỆM ⭐

| Thao tác | Kiểu | Mô tả (ai → ai) |
|---|---|---|
| **`MPI_Bcast`** | 1 → all | Root gửi **cùng 1 dữ liệu** cho mọi tiến trình |
| **`MPI_Scatter`** | 1 → all | Root **chia mảng** thành p phần, gửi **mỗi phần khác nhau** cho mỗi tiến trình |
| **`MPI_Gather`** | all → 1 | Mỗi tiến trình gửi phần của mình, root **ghép lại** thành mảng |
| **`MPI_Allgather`** | all → all | = Gather + Bcast: **mọi** tiến trình đều nhận mảng ghép đầy đủ |
| **`MPI_Alltoall`** | all → all | Mỗi tiến trình gửi **dữ liệu riêng** tới **từng** tiến trình khác (giống chuyển vị ma trận) |
| **`MPI_Reduce`** | all → 1 | Gộp (sum/max/min/prod...) dữ liệu về **root** |
| **`MPI_Allreduce`** | all → all | = Reduce + Bcast: **mọi** tiến trình nhận kết quả gộp |
| **`MPI_Reduce_scatter`** | all → all | Reduce rồi **chia** kết quả cho các tiến trình |
| **`MPI_Scan`** | prefix | Quét tiền tố (kết quả gộp lũy tiến theo rank) |
| **`MPI_Barrier`** | đồng bộ | Chặn cho tới khi **mọi** tiến trình cùng tới điểm này |

**Mẹo phân biệt (dễ bị lừa):**
- **Bcast vs Scatter:** Bcast = *cùng* dữ liệu; Scatter = *chia nhỏ, khác nhau*.
- **Gather vs Reduce:** Gather = *ghép nối* (giữ nguyên); Reduce = *gộp bằng phép toán* (sum/max...).
- Hễ có tiền tố **`All`** = kết quả về **tất cả** tiến trình (thêm một bước broadcast).
- **`Allreduce = Reduce-Scatter + All-Gather`** (dùng lại ý này ở FSDP/ring all-reduce).

**Phép toán reduce:** `MPI_SUM`, `MPI_PROD`, `MPI_MAX`, `MPI_MIN`, `MPI_LAND/LOR` (logic), `MPI_MAXLOC/MINLOC`.

### 3.2. Topology & chi phí truyền thông

Cùng một thao tác, chi phí phụ thuộc **topology mạng kết nối** p nút:

| Topology | Broadcast/Reduce một-nhiều | Đặc điểm |
|---|---|---|
| **Ring / mảng tuyến tính** | ~ **p − 1** bước | Đơn giản, chậm khi p lớn |
| **Mesh (lưới √p × √p)** | ~ 2·√p bước (2 pha hàng/cột) | Trung gian |
| **Hypercube (siêu lập phương)** | ~ **log₂ p** bước | **Tối ưu**, nhân đôi số nút biết mỗi bước |

Ý tưởng cốt lõi: thuật toán **recursive doubling** trên hypercube đạt `log₂ p` bước cho broadcast/all-gather/all-reduce.
Chi phí 1 thông điệp: **`t_startup + t_word · m`** (`t_s` = độ trễ khởi tạo, `t_w` = thời gian/byte, m = kích thước).

Kỹ thuật tăng tốc: **chia nhỏ & định tuyến thông điệp** (message splitting), **truyền thông đa cổng**, **phép dịch vòng** (circular shift).

---

## 4. Bẫy hay gặp trong đề
1. Nhầm **Scatter ↔ Bcast** (khác/giống dữ liệu).
2. Nhầm **Gather ↔ Reduce** (ghép nối vs phép toán gộp).
3. Quên **collective phải được gọi bởi TẤT CẢ** tiến trình → thiếu 1 tiến trình = treo.
4. **Deadlock** do Send–Send đối xứng ở chế độ đồng bộ.
5. `MPI_Ssend` mới là bắt tay đồng bộ; `MPI_Send` (standard) **không đảm bảo** đồng bộ.
6. Non-blocking `Isend/Irecv` **bắt buộc** `Wait/Test` mới an toàn dùng lại buffer.
