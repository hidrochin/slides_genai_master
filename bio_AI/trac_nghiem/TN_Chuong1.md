# Trắc nghiệm Chương 1 – Giới thiệu GenAI trong Tin sinh, Y học & CSSK

> ⚠️ **Nhiều đáp án đúng có thể xảy ra.** Mỗi câu có 5–7 phương án. Tự làm rồi so với **ĐÁP ÁN** ở cuối file.

---

**Câu 1.** Phát biểu nào ĐÚNG về mô hình **discriminative** và **generative**?
- A. Discriminative học ranh giới quyết định `P(Y|X)`
- B. Generative học phân phối dữ liệu `P(X)`
- C. Generative luôn là học có giám sát (supervised)
- D. Generative có thể lấy mẫu để sinh dữ liệu mới
- E. Generative có thể học có điều kiện `P(X|Y)` để sinh theo nhãn
- F. Discriminative thường dùng cho phân loại/hồi quy

**Câu 2.** Những lý do khiến **AI tạo sinh** quan trọng trong y sinh?
- A. Dữ liệu y sinh là big data, thưa nhãn (labels sparse, biased)
- B. Sinh dữ liệu nhân tạo giúp bảo vệ quyền riêng tư
- C. Data augmentation cho các quần thể thiếu dữ liệu
- D. Loại bỏ hoàn toàn nhu cầu về dữ liệu thực nghiệm
- E. Có thể suy diễn khi thiếu nhãn (vd dự đoán biến thể gây bệnh)
- F. Đảm bảo mô hình luôn có độ chính xác 100%

**Câu 3.** Về **xét nghiệm NIPT**, phát biểu nào ĐÚNG?
- A. Là xét nghiệm xâm lấn, lấy mẫu trực tiếp từ thai nhi
- B. Dựa vào DNA tự do của thai nhi (cfDNA) trong máu mẹ
- C. Phát hiện hội chứng Down (Trisomy 21)
- D. Phát hiện hội chứng Edwards (Trisomy 18) và Patau (Trisomy 13)
- E. Thực hiện bằng cách giải trình tự DNA
- F. Chỉ dùng để xác định giới tính thai nhi

**Câu 4.** Đâu là **oncogene** (gen gây ung thư)?
- A. KRAS
- B. TP53
- C. EGFR
- D. BRAF
- E. PTEN
- F. RB1

**Câu 5.** Phát biểu ĐÚNG về **gen ức chế khối u (tumor suppressor)** như TP53/p53?
- A. Bình thường làm chậm phân chia tế bào
- B. Có chức năng sửa chữa DNA lỗi
- C. Có thể khởi động apoptosis (chết theo chương trình)
- D. Khi tăng chức năng (gain-of-function) sẽ gây ung thư
- E. Khi mất chức năng → tế bào tăng sinh không kiểm soát
- F. TP53, RB1, PTEN đều là ví dụ

**Câu 6.** Về **bệnh Thalassemia**, phát biểu nào ĐÚNG?
- A. Là bệnh tan máu bẩm sinh
- B. Hemoglobin có cấu trúc bất thường → hồng cầu bị phá hủy
- C. Beta-thalassemia do không tạo đủ beta-globin
- D. Là một loại ung thư máu
- E. Có thể gây biến chứng suy tim, xơ gan, lách to
- F. Do đột biến ở gene beta-globin

**Câu 7.** Với bài toán **vi khuẩn kháng thuốc**, các mô hình ML cần giải quyết?
- A. Dự đoán kháng sinh nào còn nhạy với chủng vi khuẩn mới
- B. Đề xuất cơ chế kháng kháng sinh mới
- C. Đề xuất thuốc điều trị mới
- D. Tạo ra vi khuẩn kháng thuốc mới
- E. *Klebsiella pneumoniae* và *Acinetobacter baumannii* là ví dụ chủng đa kháng

**Câu 8.** Bài toán **Disease–Gene–Drug** bao gồm dự đoán các liên kết nào?
- A. Drug–Target Interaction (tương tác thuốc–đích)
- B. Disease–Gene Association (liên kết bệnh–gen)
- C. Drug–Disease Association (tái định vị thuốc)
- D. Gene–Gene Duplication
- E. Các cách tiếp cận: network-based, machine learning-based, data mining-based

---

## ✅ ĐÁP ÁN & GIẢI THÍCH

**1: A, B, D, E, F** — C sai: generative thường là *không giám sát*; nhưng có thể học có điều kiện.
**2: A, B, C, E** — D, F sai (không loại bỏ dữ liệu thực nghiệm, không đảm bảo 100%).
**3: B, C, D, E** — A sai (NIPT *không xâm lấn*); F sai (không chỉ để xác định giới tính).
**4: A, C, D** — TP53, PTEN, RB1 là tumor suppressor.
**5: A, B, C, E, F** — D sai: tumor suppressor gây bệnh khi *mất chức năng* (loss-of-function), không phải gain-of-function (đó là oncogene như KRAS).
**6: A, B, C, E, F** — D sai (Thalassemia là bệnh thiếu máu di truyền, không phải ung thư).
**7: A, B, C, E** — D sai (mục tiêu là *chống* vi khuẩn, không tạo ra).
**8: A, B, C, E** — D không thuộc bài toán này.
