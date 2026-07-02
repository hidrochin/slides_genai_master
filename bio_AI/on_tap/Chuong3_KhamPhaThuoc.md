# Chương 3 – Khám phá thuốc (Drug Discovery)

> Gồm 2 phần: (A) Quy trình phát triển thuốc & dược lý; (B) Biểu diễn phân tử thuốc + GNN + mô hình sinh phân tử.

---

## PHẦN A – GIỚI THIỆU QUÁ TRÌNH PHÁT TRIỂN THUỐC

### 3.1. Định nghĩa & phân loại thuốc
- **Thuốc**: chất đã qua thử nghiệm & giám sát chặt để chẩn đoán, chữa, giảm nhẹ, điều trị, phòng ngừa bệnh.
- **4 loại chính**:
  1. **Thuốc phân tử nhỏ (small molecule)**: hợp chất tổng hợp hóa học, **< 900 Dalton**, dễ tổng hợp, dùng đường uống, khuếch tán qua màng, nhắm đích đặc hiệu (enzyme, receptor). Vd: Aspirin, Metformin, Statin.
  2. **Thuốc sinh học (biologics)**: phân tử lớn từ tế bào sống (protein, kháng thể), dùng đường tiêm. Vd: Herceptin (ung thư vú), insulin, vắc-xin.
  3. **Tác nhân sinh học trị liệu sống (LBA)**: chứa sinh vật sống (men vi sinh Lactobacillus, FMT cấy ghép hệ vi sinh).
  4. **Liệu pháp tế bào (cell therapies)**: đưa tế bào sống vào cơ thể. Vd: **CAR-T** (Kymriah, Yescarta), tế bào gốc.

### 3.2. Dược động học & Dược lực học ⭐
| | **PK – Dược động học (Pharmacokinetics)** | **PD – Dược lực học (Pharmacodynamics)** |
|---|---|---|
| Câu hỏi | **Cơ thể làm gì với thuốc** | **Thuốc làm gì với cơ thể** |
| Nội dung | **ADME** | Tương tác thuốc-receptor, liều-đáp ứng, MOA |

**ADME** (4 quá trình PK):
- **A – Absorption (Hấp thu)**: thuốc vào máu; ảnh hưởng bởi đường dùng, độ tan, pH → **khả dụng sinh học (bioavailability)**.
- **D – Distribution (Phân bố)**: phân tán qua mô/dịch; liên kết protein huyết tương (albumin), qua **hàng rào máu não**; **thể tích phân bố Vd**.
- **M – Metabolism (Chuyển hóa)**: chủ yếu ở **gan**. Pha I (oxy hóa/khử/thủy phân bởi **cytochrome P450**), Pha II (liên hợp làm tan trong nước). Có thể tạo chất chuyển hóa độc (vd acetaminophen).
- **E – Excretion (Thải trừ)**: qua **thận (nước tiểu)**, gan (mật/phân); **thời gian bán hủy (half-life)** = thời gian nồng độ giảm 50%.

**PD – khái niệm cốt lõi:**
- **Receptor**: protein mà thuốc gắn vào (GPCR, kênh ion, enzyme, thụ thể hạt nhân).
- **Agonist** (chủ vận, kích hoạt receptor) vs **Antagonist** (đối kháng, chặn) vs **Partial agonist**.
- **Affinity** (ái lực): độ mạnh tương tác thuốc-receptor.
- **Đường cong liều-đáp ứng**: **EC50** (liều đạt 50% tác dụng tối đa – đo hiệu lực), **Emax** (hiệu quả tối đa), **Potency (hiệu lực)** vs **Efficacy (hiệu quả)**.
- **MOA (Mechanism of Action)**: cơ chế phân tử (vd beta-blocker chặn thụ thể β-adrenergic).
- **Therapeutic Window (cửa sổ điều trị)**: khoảng liều hiệu quả mà không độc.
- **Therapeutic Index: TI = TD50 / ED50** (TD50 = liều gây độc 50%, ED50 = liều hiệu quả 50%). **TI rộng = an toàn hơn**.
- Tương tác thuốc: **Synergism** (hiệp đồng > tổng), **Antagonism** (đối kháng, vd Naloxone chặn opioid), **Additive** (cộng).

### 3.3. Độc chất học (Toxicology)
- Cấp tính, bán mãn/mãn tính, **genotoxicity** (tổn thương DNA), **carcinogenicity** (gây ung thư), độc tính sinh sản.
- Kết quả: **NOAEL** (No Observed Adverse Effect Level), **MTD** (Maximum Tolerated Dose).

### 3.4. ⭐ Các bước chính trong khám phá thuốc
```
Target ID → Target Validation → Hit ID → Hit-to-Lead → Lead ID → Lead Optimization → Preclinical → Clinical → FDA → Post-market
```
1. **Target Identification**: tìm đích sinh học (protein/gen) liên quan bệnh. Xét **druggability** (khả năng dùng thuốc).
2. **Target Validation**: xác nhận vai trò đích (CRISPR, siRNA knockdown, mô hình động vật).
3. **Hit Identification**: sàng lọc hợp chất tương tác đích – **HTS** (high-throughput screening), fragment-based, **virtual screening**, sản phẩm tự nhiên.
4. **Hit-to-Lead (H2L)**: tối ưu hit → lead; nghiên cứu **SAR**, sàng lọc ADME sớm.
5. **Lead Identification**: chọn lead có ái lực cao, chọn lọc, **giống thuốc (Lipinski's Rule of 5)**, ADMET chấp nhận được.
6. **Lead Optimization**: tinh chỉnh hiệu lực, chọn lọc, PK, an toàn.

- **SAR (Structure-Activity Relationship)**: mối quan hệ giữa cấu trúc hóa học và hoạt tính sinh học. Chiến lược: sửa nhóm chức, thay đổi độ dài chuỗi, sửa vòng, thay thế đẳng lập (isosteric), **QSAR**.
- **Druggability**: đích khó dùng thuốc (protein rối loạn nội tại, giao diện protein-protein) → dùng biologics hoặc CRISPR.

### 3.5. Lâm sàng & quản lý
- **FDA** (Food and Drug Administration): đảm bảo an toàn, hiệu quả thuốc.
- **Companion Diagnostics**: xét nghiệm đi kèm để dùng thuốc an toàn/hiệu quả (vd HER2→Herceptin, EGFR→gefitinib, PD-L1→Keytruda).
- **Chi phí phát triển 1 thuốc**: trung vị **$985 triệu**, trung bình **$1.3 tỷ**. Tỷ lệ thất bại cao (attrition).

---

## PHẦN B – BIỂU DIỄN PHÂN TỬ, GNN & MÔ HÌNH SINH ⭐⭐

### 3.6. Các dạng biểu diễn phân tử thuốc
| Dạng | Mô tả | Ví dụ (Ethanol/Benzen) | Ưu / Nhược |
|---|---|---|---|
| **SMILES** | Chuỗi ASCII tuyến tính mã hóa nguyên tử/liên kết/kết nối | Ethanol → `CCO` | Ngắn gọn, dễ đọc / khó mã hóa lập thể, tautomer |
| **SMARTS** | Ngôn ngữ **khớp mẫu** dựa trên SMILES, tìm tiểu cấu trúc | Benzen → `c1ccccc1` | Linh hoạt tìm kiếm / phức tạp |
| **SELFIES** | Chuỗi tự tham chiếu, **luôn giải mã thành phân tử hợp lệ** | Benzen → `C1=CC=CC=C1` | Robust cho ML / khó đọc |
| **InChI** | Định danh chuẩn hóa của IUPAC, **duy nhất** | Ethanol → `InChI=1S/C2H6O/...` | Chuẩn hóa / cồng kềnh |
| **Molecular Graph** | Đồ thị: **nguyên tử = nút, liên kết = cạnh** | Ma trận kề | Trực quan kết nối / không nhỏ gọn |

**Quy tắc SMILES (5 rules):** (1) nguyên tử & liên kết (`-` đơn, `=` đôi, `#` ba, chữ thường = thơm); (2) chuỗi đơn (H bị ẩn); (3) nhánh trong ngoặc `()`; (4) vòng đánh số; (5) điện tích trong `{}`.

### 3.7. Descriptor & Fingerprint
- **Morgan Fingerprints (Circular / ECFP)**: mã hóa cấu trúc con **hình tròn** quanh mỗi nguyên tử theo **bán kính (radius)**; băm thành vector nhị phân độ dài cố định (vd 1024 bit, có thể **hash collision**). Dùng cho similarity search, QSAR, virtual screening (hỗ trợ trong **RDKit**).
- **QSAR (Quantitative Structure–Activity Relationship)**: mô hình toán/ML liên hệ **cấu trúc hóa học ↔ hoạt tính/độc tính**.
  - Nguyên lý: *"phân tử có cấu trúc tương tự thường có hoạt tính tương tự"*.
  - Luồng: **Structure → Descriptor → Activity/Toxicity**.
  - Descriptor ví dụ: **logP** (hệ số phân bố dầu/nước, cao → dễ qua màng, khó tan), **MW** (khối lượng phân tử, Da), **HBD** (số nhóm cho liên kết hidro).

### 3.8. Molecular Graphs & Graph Neural Networks (GNN)
- **Đồ thị phân tử**: nút = nguyên tử (nhãn loại nguyên tử), cạnh = liên kết (đơn/đôi/ba, có thể có trọng số). Biểu diễn: **ma trận kề**, danh sách kề.
- **Geometric Deep Learning**: mở rộng DL sang miền phi-Euclid (đồ thị, manifold). DL truyền thống làm việc trên lưới đều (ảnh 2D, chuỗi 1D).
- **Invariance / Equivariance**: tính chất phân tử **bất biến** với phép quay/dịch chuyển (độ tan, ái lực, ADME). GNN cần **permutation invariant**.
- **GNN – Message Passing**: mỗi nút thu thập ("message") thông tin từ các nút lân cận qua cạnh → cập nhật biểu diễn; lặp nhiều lớp → mở rộng **receptive field**.
- **Đầu ra GNN**:
  - **Node classification**: phân loại nút (vd user spam).
  - **Link prediction**: dự đoán cạnh (vd **drug–target interaction**, gợi ý kết bạn).
  - **Graph-level**: dự đoán thuộc tính cả phân tử (độc tính, độ tan, ái lực) → **pooling** (sum/mean/max/attention) rồi MLP.

### 3.9. Mô hình sinh phân tử mới (Generating New Molecules)
- **Autoencoder (AE)**: nén (encode) → giải nén (decode); tái tạo tốt nhưng **khó sinh dữ liệu mới**. *(Ví như máy photocopy).*
- **VAE (Variational Autoencoder)**: encoder xuất **phân phối xác suất** (mean + variance) thay vì điểm cố định → lấy mẫu → sinh dữ liệu mới. *(Ví như họa sĩ – vừa sao chép vừa vẽ mới).* Loss = **reconstruction + regularization (KL)**.
- **GAN (Generative Adversarial Network)**: **generator** vs **discriminator** đấu nhau (zero-sum) tới điểm cân bằng.
- **GAN vs VAE**:
  - GAN khó huấn luyện, dễ **mode collapse** (ít đa dạng), nhưng mẫu **sắc nét (high-fidelity)**.
  - VAE đa dạng hơn nhưng mẫu có thể **"mờ" (blurry)**.
- **TGVAE**: Transformer Graph VAE cho thiết kế phân tử sinh.

---

## 3.10. Câu hỏi ôn tập nhanh
1. Phân biệt **PK vs PD**. Giải thích **ADME**.
2. Nêu công thức **Therapeutic Index**; TI rộng/hẹp nghĩa là gì?
3. Liệt kê **các bước khám phá thuốc**. Phân biệt Hit / Lead. SAR là gì?
4. So sánh **SMILES, SELFIES, InChI, Molecular Graph**. Vì sao SELFIES tốt cho ML?
5. **Morgan fingerprint** & **QSAR** hoạt động thế nào? logP/MW/HBD là gì?
6. Cơ chế **message passing** trong GNN? 3 loại đầu ra của GNN?
7. So sánh **AE vs VAE vs GAN**. Mode collapse là gì?
