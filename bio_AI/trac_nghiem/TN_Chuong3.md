# Trắc nghiệm Chương 3 – Khám phá thuốc (Drug Discovery)

> ⚠️ **Nhiều đáp án đúng có thể xảy ra.** Tự làm rồi so với **ĐÁP ÁN** ở cuối file.

---

**Câu 1.** Về **thuốc phân tử nhỏ (small molecule)**?
- A. Trọng lượng phân tử thường < 900 Dalton
- B. Dễ tổng hợp qua quá trình hóa học
- C. Thường dùng đường uống, khuếch tán qua màng tế bào
- D. Là phân tử lớn từ tế bào sống
- E. Aspirin, Metformin, Statin là ví dụ
- F. Luôn phải tiêm tĩnh mạch do khả dụng sinh học đường uống kém

**Câu 2.** Về **thuốc sinh học (biologics)**?
- A. Phân tử lớn, phức tạp, có nguồn gốc từ tế bào sống
- B. Thường là protein hoặc kháng thể
- C. Thường dùng đường tiêm/truyền
- D. Herceptin, insulin, vắc-xin là ví dụ
- E. Trọng lượng phân tử nhỏ, dễ khuếch tán qua màng

**Câu 3.** Ghép đúng loại thuốc với ví dụ?
- A. CAR-T (Kymriah, Yescarta) là liệu pháp tế bào
- B. Men vi sinh (Lactobacillus) là tác nhân sinh học trị liệu sống (LBA)
- C. Kháng thể đơn dòng là biologics
- D. Cấy ghép hệ vi sinh đường ruột (FMT) là small molecule
- E. Tế bào gốc là liệu pháp tế bào

**Câu 4.** Phân biệt **PK (dược động học)** và **PD (dược lực học)**?
- A. PK trả lời "cơ thể làm gì với thuốc"
- B. PD trả lời "thuốc làm gì với cơ thể"
- C. PK bao gồm ADME
- D. PD gồm tương tác thuốc-receptor, liều-đáp ứng, MOA
- E. PK trả lời "thuốc làm gì với cơ thể"
- F. ADME thuộc PD

**Câu 5.** **ADME** gồm những quá trình nào?
- A. Absorption (hấp thu)
- B. Distribution (phân bố)
- C. Metabolism (chuyển hóa)
- D. Excretion (thải trừ)
- E. Amplification (khuếch đại)
- F. Elimination reaction

**Câu 6.** Về **chuyển hóa thuốc (Metabolism)**?
- A. Chủ yếu diễn ra ở gan
- B. Pha I: oxy hóa/khử/thủy phân bởi enzyme (cytochrome P450)
- C. Pha II: liên hợp làm thuốc tan trong nước hơn
- D. Có thể tạo chất chuyển hóa độc (vd acetaminophen)
- E. Chủ yếu diễn ra ở thận

**Câu 7.** Về **Therapeutic Index (TI)** và các khái niệm PD?
- A. TI = TD50 / ED50
- B. TI rộng nghĩa là thuốc an toàn hơn
- C. EC50 là liều đạt 50% tác dụng tối đa
- D. Therapeutic window là khoảng liều hiệu quả không độc
- E. TI hẹp nghĩa là thuốc an toàn hơn
- F. Agonist chặn receptor, antagonist kích hoạt receptor

**Câu 8.** Về tương tác thuốc-receptor?
- A. Agonist kích hoạt receptor tạo phản ứng
- B. Antagonist chặn hoạt hóa receptor (vd Naloxone chặn opioid)
- C. Affinity = độ mạnh tương tác thuốc-receptor
- D. Synergism: hai thuốc tạo tác dụng kết hợp lớn hơn tổng
- E. Additive: một thuốc làm giảm tác dụng thuốc khác

**Câu 9.** Thứ tự ĐÚNG các bước khám phá thuốc?
- A. Target Identification → Target Validation
- B. Hit Identification → Hit-to-Lead → Lead Identification → Lead Optimization
- C. Lead Optimization → Target Identification
- D. Preclinical → Clinical → FDA approval
- E. FDA approval → Target Validation

**Câu 10.** Về **SAR (Structure-Activity Relationship)**?
- A. Là mối quan hệ giữa cấu trúc hóa học và hoạt tính sinh học
- B. Chiến lược gồm sửa nhóm chức, thay đổi độ dài chuỗi, sửa vòng
- C. QSAR là phiên bản định lượng bằng mô hình tính toán
- D. Chỉ áp dụng cho thuốc sinh học
- E. Giúp tối ưu hiệu lực, chọn lọc, giảm độc tính

**Câu 11.** Ghép đúng **biểu diễn phân tử** với đặc điểm?
- A. SMILES = chuỗi ASCII tuyến tính (Ethanol → CCO)
- B. SELFIES = luôn giải mã thành phân tử hợp lệ (tốt cho ML)
- C. InChI = định danh chuẩn hóa duy nhất của IUPAC
- D. SMARTS = ngôn ngữ khớp mẫu tìm tiểu cấu trúc
- E. Molecular graph = nút là liên kết, cạnh là nguyên tử
- F. SMILES: vòng thơm viết chữ thường (c1ccccc1)

**Câu 12.** Về **Morgan Fingerprint** và **QSAR**?
- A. Morgan fingerprint mã hóa cấu trúc con hình tròn quanh mỗi nguyên tử
- B. Được băm thành vector nhị phân, có thể xảy ra hash collision
- C. QSAR biến cấu trúc phân tử thành molecular descriptors
- D. logP cao → dễ qua màng tế bào, khó tan trong nước
- E. HBD là số nhóm cho liên kết hidro
- F. Morgan fingerprint chỉ dùng cho protein

**Câu 13.** Về **Molecular Graph** và **GNN**?
- A. Nút = nguyên tử, cạnh = liên kết
- B. GNN dùng cơ chế message passing
- C. GNN cần tính permutation invariant
- D. Đầu ra GNN có thể là node classification, link prediction, graph-level
- E. Link prediction có thể dự đoán drug-target interaction
- F. GNN chỉ hoạt động trên dữ liệu dạng lưới đều (ảnh)

**Câu 14.** Về **tính bất biến (invariance/equivariance)** trong mô hình phân tử?
- A. Tính chất phân tử bất biến với phép quay, dịch chuyển
- B. Độ tan, ái lực, ADME là các tính chất bất biến
- C. Geometric deep learning mở rộng DL sang miền phi-Euclid
- D. DL truyền thống làm việc trên lưới đều (ảnh 2D, chuỗi 1D)
- E. Tính chất phân tử luôn thay đổi khi quay phân tử

**Câu 15.** So sánh **AE, VAE, GAN**?
- A. AE tái tạo tốt nhưng khó sinh dữ liệu mới
- B. VAE encoder xuất phân phối xác suất (mean + variance)
- C. GAN gồm generator và discriminator đấu nhau
- D. GAN dễ bị mode collapse (ít đa dạng)
- E. VAE thường cho mẫu sắc nét hơn, GAN cho mẫu "mờ"
- F. VAE loss = reconstruction + regularization (KL)

**Câu 16.** Về **GAN vs VAE** (điểm mạnh/yếu)?
- A. GAN khó huấn luyện hơn VAE
- B. GAN cho mẫu high-fidelity (sắc nét) nhưng ít đa dạng
- C. VAE cho đa dạng hơn nhưng mẫu có thể "blurry"
- D. GAN dễ đảm bảo generator và discriminator cân bằng
- E. TGVAE = Transformer Graph VAE cho thiết kế phân tử

**Câu 17.** Về **companion diagnostics** và FDA?
- A. Companion diagnostics là xét nghiệm đi kèm để dùng thuốc an toàn/hiệu quả
- B. HER2 test cho Herceptin (ung thư vú)
- C. EGFR mutation test cho gefitinib (ung thư phổi)
- D. PD-L1 cho liệu pháp miễn dịch (Keytruda)
- E. FDA đảm bảo an toàn, hiệu quả của thuốc
- F. Companion diagnostics chỉ dùng cho thuốc sinh học

---

## ✅ ĐÁP ÁN & GIẢI THÍCH

**1: A, B, C, E** — D, F mô tả biologics.
**2: A, B, C, D** — E sai (biologics là phân tử lớn, khó khuếch tán).
**3: A, B, C, E** — D sai (FMT là LBA, không phải small molecule).
**4: A, B, C, D** — E, F sai (đảo ngược PK/PD).
**5: A, B, C, D** — E, F không thuộc ADME.
**6: A, B, C, D** — E sai (chuyển hóa chủ yếu ở *gan*; thải trừ mới ở thận).
**7: A, B, C, D** — E sai (TI hẹp = nguy hiểm hơn); F sai (đảo ngược agonist/antagonist).
**8: A, B, C, D** — E sai (mô tả antagonism, không phải additive).
**9: A, B, D** — C, E sai thứ tự.
**10: A, B, C, E** — D sai (SAR áp dụng cho thuốc phân tử nhỏ là chính).
**11: A, B, C, D, F** — E sai (nút là *nguyên tử*, cạnh là *liên kết* – ngược lại).
**12: A, B, C, D, E** — F sai (dùng cho phân tử thuốc/hợp chất nói chung).
**13: A, B, C, D, E** — F sai (GNN xử lý đồ thị phi-lưới; CNN mới cho lưới đều).
**14: A, B, C, D** — E sai (tính chất *bất biến*, không thay đổi khi quay).
**15: A, B, C, D, F** — E sai (ngược: VAE "mờ", GAN sắc nét).
**16: A, B, C, E** — D sai (GAN *khó* đảm bảo cân bằng).
**17: A, B, C, D, E** — F sai (dùng cho cả small molecule và biologics).
