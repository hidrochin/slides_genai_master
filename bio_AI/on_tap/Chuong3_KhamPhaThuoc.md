# Chương 3 – Khám phá thuốc (Drug Discovery)

> Gồm 2 phần: (A) Quy trình phát triển thuốc & dược lý; (B) Biểu diễn phân tử thuốc + GNN + mô hình sinh phân tử.
>
> **🔖 Nhãn ra thi:** 🔴 CAO · 🟡 TB · ⚪ THẤP (xem [Chuong1](Chuong1_GioiThieu_GenAI_TinSinh_YHoc.md)).
> Trọng tâm đề: **PK/PD/ADME**, **các bước khám phá thuốc**, **biểu diễn phân tử (SMILES...)**, **GNN message passing**, **AE/VAE/GAN**.

---

## PHẦN A – GIỚI THIỆU QUÁ TRÌNH PHÁT TRIỂN THUỐC

### 3.1. Định nghĩa & phân loại thuốc 🟡 TB
- **Thuốc**: chất đã qua thử nghiệm & giám sát chặt để **chẩn đoán, chữa, giảm nhẹ, điều trị, phòng ngừa** bệnh.
- **Lịch sử (⚪ thấp):** trước đây chiết từ tự nhiên – **Aspirin** (vỏ cây liễu, ~3000–1500 TCN), **Artemisia** (hạ sốt, 168 TCN).
- **4 loại chính** (nhớ ví dụ để tránh gán nhầm): 🔴 CAO
  1. **Small molecule (phân tử nhỏ)**: tổng hợp hóa học, **< 900 Dalton**, dễ tổng hợp, thường **uống**, **khuếch tán qua màng**, nhắm đích đặc hiệu (enzyme, receptor). Vd: **Aspirin, Metformin, Statin**.
  2. **Biologics (sinh học)**: phân tử **lớn** từ tế bào sống (protein, kháng thể), thường **tiêm/truyền** (khả dụng đường uống kém), đặc hiệu cao. Vd: **Herceptin** (ung thư vú), **insulin**, vắc-xin.
  3. **LBA (Live Biotherapeutic Agents)**: chứa **sinh vật sống** (men vi sinh Lactobacillus, **FMT** cấy ghép hệ vi sinh cho *C. difficile*). Ưu: độc tính thấp; nhược: khó chuẩn hóa.
  4. **Cell therapies (liệu pháp tế bào)**: đưa tế bào sống vào cơ thể; tự thân/đồng loại. Vd: **CAR-T** (Kymriah, Yescarta) cho ung thư máu, tế bào gốc, ghép tủy.

> 🎯 **Bẫy:** đảo ngược *small molecule (<900 Da, uống, khuếch tán) ↔ biologics (lớn, tiêm)*; hoặc gán nhầm ví dụ (Herceptin là biologics, không phải small molecule).

### 3.2. ⭐ Dược động học & Dược lực học 🔴 CAO (gần như CHẮC ra – hay hỏi đảo ngược PK↔PD)
| | **PK – Pharmacokinetics (Dược động học)** | **PD – Pharmacodynamics (Dược lực học)** |
|---|---|---|
| Câu hỏi | **Cơ thể làm gì với thuốc** | **Thuốc làm gì với cơ thể** |
| Nội dung | **ADME** | Tương tác thuốc-receptor, liều-đáp ứng, MOA |

**ADME** (4 quá trình PK): 🔴 CAO
- **A – Absorption (Hấp thu)**: thuốc vào máu; ảnh hưởng bởi đường dùng, độ tan, pH, lưu lượng máu → **khả dụng sinh học (bioavailability)**.
- **D – Distribution (Phân bố)**: phân tán qua mô/dịch; liên kết **protein huyết tương (albumin)**; qua **hàng rào máu não**; đo bằng **thể tích phân bố Vd**.
- **M – Metabolism (Chuyển hóa)**: chủ yếu ở **gan**. **Pha I** (oxy hóa/khử/thủy phân bởi **cytochrome P450**), **Pha II** (liên hợp/glucuronidation → tan trong nước). Có thể tạo chất chuyển hóa **độc** (vd acetaminophen).
- **E – Excretion (Thải trừ)**: qua **thận (nước tiểu)**, gan (mật/phân), phổi, mồ hôi, sữa mẹ; **thời gian bán hủy (half-life)** = thời gian nồng độ giảm **50%**.

> 🎯 **Bẫy ADME:** chuyển hóa chủ yếu ở **gan** (không phải thận); thải trừ chủ yếu ở **thận**.

**PD – khái niệm cốt lõi:** 🔴 CAO
- **Receptor**: protein thuốc gắn vào (GPCR, kênh ion, enzyme, thụ thể hạt nhân).
- **Agonist** (chủ vận – kích hoạt) vs **Antagonist** (đối kháng – chặn, không có đáp ứng) vs **Partial agonist** (kích hoạt yếu hơn).
- **Affinity (ái lực)**: độ mạnh tương tác thuốc-receptor.
- **Đường cong liều-đáp ứng**: **EC50** (liều đạt 50% tác dụng tối đa – đo **hiệu lực/potency**), **Emax** (hiệu quả tối đa).
  - **Potency (hiệu lực)** = lượng thuốc cần để đạt tác dụng ≠ **Efficacy (hiệu quả)** = tác dụng tối đa đạt được.
- **MOA (Mechanism of Action)**: cơ chế phân tử (vd **beta-blocker** chặn thụ thể β-adrenergic → giảm nhịp tim).
- **Signal transduction**: thuốc tác động qua đường tín hiệu; **chất truyền tin thứ hai** (cAMP, ion Ca²⁺) khuếch đại tín hiệu.
- **Dung nạp/nhạy cảm (⚪):** Tolerance (giảm đáp ứng, cần liều cao hơn), Desensitization, Downregulation (giảm số receptor), Sensitization.
- **Therapeutic Window (cửa sổ điều trị)**: khoảng liều hiệu quả mà không độc.
- **Therapeutic Index: TI = TD50 / ED50** 🔴 (công thức hay hỏi). **TI rộng = an toàn hơn**; TI hẹp = nguy hiểm.
- Tương tác thuốc: **Synergism** (hiệp đồng > tổng, vd rượu + an thần), **Antagonism** (đối kháng, vd **Naloxone** chặn opioid), **Additive** (cộng, vd 2 thuốc hạ áp).

> 🎯 **Bẫy:** *agonist ↔ antagonist*; *potency ↔ efficacy*; công thức TI (tử số TD50, mẫu ED50).

### 3.3. Độc chất học (Toxicology) 🟡 TB
- Cấp tính, bán mãn/mãn tính, **genotoxicity** (tổn thương DNA), **carcinogenicity** (gây ung thư), độc tính sinh sản.
- Kết quả: **NOAEL** (No Observed Adverse Effect Level), **MTD** (Maximum Tolerated Dose).

### 3.4. ⭐ Các bước chính trong khám phá thuốc 🔴 CAO (hay hỏi thứ tự & phân biệt Hit/Lead)
```
Target ID → Target Validation → Hit ID → Hit-to-Lead → Lead ID → Lead Optimization → Preclinical → Clinical → FDA → Post-market
```
1. **Target Identification**: tìm đích sinh học (protein/gen) liên quan bệnh. Xét **druggability**.
2. **Target Validation**: xác nhận vai trò đích (**CRISPR, siRNA** knockdown, overexpression, mô hình động vật).
3. **Hit Identification**: sàng lọc hợp chất tương tác đích – **HTS** (high-throughput screening), **fragment-based (FBS)**, **virtual screening**, sản phẩm tự nhiên.
4. **Hit-to-Lead (H2L)**: tối ưu hit → lead; nghiên cứu **SAR**, sàng lọc **ADME** sớm. Metrics: IC50/EC50, selectivity.
5. **Lead Identification**: chọn lead có **ái lực cao**, chọn lọc, **giống thuốc (Lipinski's Rule of 5)**, ADMET chấp nhận được.
6. **Lead Optimization**: tinh chỉnh hiệu lực, chọn lọc, PK, an toàn, công thức bào chế.

> 🎯 **Bẫy Hit vs Lead:** Hit = hợp chất *mới phát hiện* có hoạt tính; Lead = hit đã tối ưu, có tính giống thuốc + ADMET chấp nhận được.

- **SAR (Structure-Activity Relationship)** 🔴: quan hệ **cấu trúc hóa học ↔ hoạt tính sinh học**. Chiến lược: sửa nhóm chức, đổi độ dài chuỗi, sửa vòng, **thay thế đẳng lập (isosteric, vd H→F)**, **QSAR**. Vd: sửa nhóm R của vòng **beta-lactam (Penicillin)** đổi phổ kháng khuẩn.
- **Druggability**: đích khó dùng thuốc (protein rối loạn nội tại, giao diện protein-protein) → dùng biologics hoặc CRISPR.

### 3.5. Lâm sàng & quản lý 🟡 TB
- **FDA** (Food and Drug Administration): đảm bảo **an toàn + hiệu quả** thuốc.
- **Companion Diagnostics** (xét nghiệm đi kèm để cá thể hóa điều trị) 🔴: **HER2 → Herceptin**; **EGFR → gefitinib**; **PD-L1 → Keytruda**.
- **Chi phí phát triển 1 thuốc**: trung vị **$985 triệu**, trung bình **$1.3 tỷ**; tỷ lệ thất bại cao (**attrition**).
- ⚪ Thuốc bệnh truyền nhiễm: kháng khuẩn 55%, kháng virus 22%, kháng nấm 12%, chống ký sinh 8%, diệt côn trùng 3%.

---

## PHẦN B – ⭐⭐ BIỂU DIỄN PHÂN TỬ, GNN & MÔ HÌNH SINH 🔴 CAO

### 3.6. Các dạng biểu diễn phân tử thuốc 🔴 CAO (hay hỏi so sánh & ưu/nhược)
| Dạng | Mô tả | Ví dụ | Ưu / Nhược |
|---|---|---|---|
| **SMILES** | Chuỗi ASCII **tuyến tính** mã hóa nguyên tử/liên kết/kết nối | Ethanol → `CCO` | Ngắn gọn, dễ đọc / khó mã hóa **lập thể, tautomer** |
| **SMARTS** | Ngôn ngữ **khớp mẫu (pattern matching)** dựa trên SMILES, tìm tiểu cấu trúc | Benzen → `c1ccccc1` | Linh hoạt tìm kiếm / phức tạp, khó đọc |
| **SELFIES** | Chuỗi **tự tham chiếu**, **LUÔN giải mã thành phân tử hợp lệ** kể cả khi bị đột biến | Benzen → `C1=CC=CC=C1` | **Robust cho ML** / khó đọc hơn SMILES |
| **InChI** | Định danh **chuẩn hóa IUPAC, DUY NHẤT** | Ethanol → `InChI=1S/C2H6O/...` | Chuẩn hóa, duy nhất / cồng kềnh, khó dùng |
| **Molecular Graph** | Đồ thị: **nguyên tử = nút, liên kết = cạnh** | Ma trận kề | Trực quan kết nối / **không nhỏ gọn** |

> 🎯 **Bẫy:** *SELFIES* = luôn hợp lệ (tốt cho ML/sinh phân tử); *InChI* = định danh duy nhất chuẩn IUPAC; *SMARTS* = tìm kiếm mẫu (không phải để sinh).

**Quy tắc SMILES (5 rules):** 🟡 TB (1) nguyên tử & liên kết (`-` đơn, `=` đôi, `#` ba, **chữ thường = thơm**, `.` không liên kết như `Na.Cl`); (2) chuỗi đơn (**H bị ẩn**); (3) nhánh trong ngoặc `()`; (4) vòng đánh **số** (mở/đóng cùng số); (5) điện tích trong `{}`.

### 3.7. Descriptor & Fingerprint 🔴 CAO
- **Morgan Fingerprints (Circular / ECFP)**: mã hóa cấu trúc con **hình tròn** quanh mỗi nguyên tử theo **bán kính (radius)** (radius 2 = 2 liên kết); băm thành **vector nhị phân độ dài cố định** (vd 1024 bit → có thể **hash collision**). Dùng cho **similarity search, QSAR, virtual screening**; hỗ trợ trong **RDKit**.
- **QSAR (Quantitative Structure–Activity Relationship)** 🔴: mô hình toán/ML liên hệ **cấu trúc hóa học ↔ hoạt tính/độc tính**.
  - Nguyên lý: *"phân tử có cấu trúc tương tự thường có hoạt tính tương tự"*.
  - Luồng: **Structure → Descriptor → Activity/Toxicity**. Lợi ích: dự đoán hoạt tính/độc tính, virtual screening, **giảm thí nghiệm wet-lab**.
  - Descriptor ví dụ: **logP** (log hệ số phân bố octanol/nước; cao → dễ qua màng, khó tan nước), **MW** (khối lượng, Da), **HBD** (số nhóm cho liên kết hidro → độ tan/thấm màng).

### 3.8. Molecular Graphs & Graph Neural Networks (GNN) 🔴 CAO
- **Đồ thị phân tử**: nút = nguyên tử (nhãn loại nguyên tử), cạnh = liên kết (đơn/đôi/ba, có thể có trọng số). Biểu diễn: **ma trận kề**, danh sách kề, hình ảnh đồ thị.
- **Loại đồ thị:** vô hướng (phổ biến cho phân tử nhỏ), có hướng (cơ chế phản ứng), có nhãn (nút+cạnh gắn nhãn), có trọng số (độ dài/cường độ liên kết).
- **Geometric Deep Learning**: mở rộng DL sang miền **phi-Euclid** (đồ thị, manifold, point cloud). DL truyền thống chỉ làm việc trên **lưới đều** (ảnh 2D, chuỗi 1D — vd CNN).
- **Invariance / Equivariance**: tính chất phân tử **bất biến** với phép quay/dịch chuyển (độ tan, ái lực, ADME). GNN cần **permutation invariant** (bất biến hoán vị nút).
- **GNN – Message Passing** 🔴: mỗi nút thu thập ("message") thông tin từ **nút lân cận** qua cạnh → cập nhật (aggregate) biểu diễn; lặp nhiều lớp → mở rộng **receptive field**.
- **3 loại đầu ra GNN** 🔴 (hay hỏi ghép ví dụ):
  - **Node classification**: phân loại **nút** (vd user spam/không spam).
  - **Link prediction**: dự đoán **cạnh** (vd **drug–target interaction**, gợi ý kết bạn) – dùng cosine similarity hoặc MLP.
  - **Graph-level**: dự đoán thuộc tính **cả phân tử** (độc tính, độ tan, ái lực) → **pooling** (sum/mean/max/attention) rồi MLP.

> 🎯 **Bẫy:** ghép sai loại output với ví dụ. Nhớ: DTI = **link prediction**; độc tính/độ tan cả phân tử = **graph-level**.

### 3.9. Mô hình sinh phân tử mới (Generating New Molecules) 🔴 CAO
- **Autoencoder (AE)**: nén (encode) → giải nén (decode); tái tạo tốt nhưng **khó sinh dữ liệu mới** *(như máy photocopy)*.
- **VAE (Variational Autoencoder)** 🔴: encoder xuất **phân phối xác suất** (mean + variance) thay vì điểm cố định → lấy mẫu latent → **sinh dữ liệu mới** *(như họa sĩ)*. Loss = **reconstruction + regularization (KL)**.
- **GAN (Generative Adversarial Network)**: **generator** vs **discriminator** đấu nhau (zero-sum) tới điểm cân bằng.
- **GAN vs VAE** 🔴 (rất hay so sánh):
  - **GAN**: khó huấn luyện, khó giữ cân bằng generator/discriminator, dễ **mode collapse** (ít đa dạng), nhưng mẫu **sắc nét (high-fidelity)**.
  - **VAE**: đa dạng hơn nhưng mẫu có thể **"mờ" (blurry)**.
- **TGVAE**: **Transformer Graph VAE** cho thiết kế phân tử sinh.

> 🎯 **Bẫy:** *AE không sinh được dữ liệu mới* (chỉ tái tạo); *GAN → sắc nét nhưng mode collapse*; *VAE → đa dạng nhưng mờ*.

---

## 3.10. 🎯 Điểm tủ Chương 3 (ưu tiên ôn)
1. 🔴 **PK vs PD** (cơ thể↔thuốc), **ADME** (4 bước, gan chuyển hóa, thận thải).
2. 🔴 **TI = TD50/ED50**, TI rộng = an toàn; agonist/antagonist; potency vs efficacy.
3. 🔴 **6 bước khám phá thuốc** + phân biệt **Hit vs Lead** + **SAR**.
4. 🔴 **5 dạng biểu diễn phân tử** – so sánh, đặc biệt **SELFIES (luôn hợp lệ)** & **InChI (duy nhất)**.
5. 🔴 **Morgan fingerprint** (hình tròn, radius, hash collision) & **QSAR** (Structure→Descriptor→Activity); logP/MW/HBD.
6. 🔴 **GNN message passing** + **3 output** (node/link/graph) + ví dụ DTI = link prediction.
7. 🔴 **AE vs VAE vs GAN** – mode collapse, blurry vs high-fidelity, ai sinh được dữ liệu mới.
8. 🟡 **4 loại thuốc** (small molecule <900Da / biologics / LBA / cell therapy) + ví dụ.
9. 🟡 **Companion diagnostics** (HER2→Herceptin, EGFR→gefitinib, PD-L1→Keytruda).

## 3.11. Câu hỏi ôn tập nhanh
1. Phân biệt **PK vs PD**. Giải thích **ADME** (cơ quan chuyển hóa/thải trừ chính?).
2. Nêu công thức **Therapeutic Index**; TI rộng/hẹp nghĩa là gì? Agonist vs antagonist?
3. Liệt kê **các bước khám phá thuốc**. Phân biệt Hit / Lead. SAR là gì?
4. So sánh **SMILES, SMARTS, SELFIES, InChI, Molecular Graph**. Vì sao SELFIES tốt cho ML?
5. **Morgan fingerprint** & **QSAR** hoạt động thế nào? logP/MW/HBD là gì?
6. Cơ chế **message passing** trong GNN? 3 loại đầu ra của GNN kèm ví dụ?
7. So sánh **AE vs VAE vs GAN**. Mode collapse là gì? Vì sao AE khó sinh dữ liệu mới?
