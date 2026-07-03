# 📝 Bộ câu hỏi trắc nghiệm ôn tập – IT5428

> Câu hỏi **nhiều lựa chọn – nhiều đáp án đúng (multiple-select)**. Mỗi câu 5–6 phương án; số đáp án đúng thay đổi (có câu **không có** phương án đúng nào — kiểu "chọn tất cả câu SAI").
> **Độ khó: trung bình → rất khó** (theo yêu cầu ôn luyện). Giải thích **đặt ngay dưới mỗi câu** trong khối gấp `▸ Đáp án`.

## Danh sách
| Chương | File | Số câu |
|---|---|---|
| 1 – Giới thiệu GenAI | [TN_Chuong1.md](TN_Chuong1.md) | 10 |
| 2 – Sinh học phân tử | [TN_Chuong2.md](TN_Chuong2.md) | 10 |
| 3 – Khám phá thuốc | [TN_Chuong3.md](TN_Chuong3.md) | 12 |
| 4 – Phân tích hệ gen + GATK ⭐ | [TN_Chuong4.md](TN_Chuong4.md) | 18 |
| 5 – Y học cá thể hóa | [TN_Chuong5.md](TN_Chuong5.md) | 10 |
| 6 – XAI | [TN_Chuong6.md](TN_Chuong6.md) | 11 |
| 🎯 **ĐỀ TỔNG HỢP** (mix 6 chương, thi thử) | [TN_TongHop_50cau.md](TN_TongHop_50cau.md) | **50** |
| 🔥 **ĐỀ CỰC KHÓ – Chương 4 (GATK)** | [TN_Chuong4_CucKho.md](TN_Chuong4_CucKho.md) | **26** |

**Tổng: 71 câu theo chương + 50 câu đề tổng hợp + 26 câu cực khó Chương 4.** Chương 4 nhiều & khó nhất (quy trình GATK).

> 🔥 **Đề cực khó Chương 4** (26 câu) đào sâu GATK: đọc trường VCF (AC/AN/AF/DP/GT), giải mã **CIGAR**, cờ dòng lệnh (`--max-mnp-distance 0`, `-ERC GVCF`, `--f1r2-tar-gz`), kịch bản CalculateContamination/orientation bias, penalty λ, EVE/AlphaMissense. Làm sau cùng, khi đã chắc lý thuyết.

> 🎯 **Đề tổng hợp 50 câu** trộn cả 6 chương, độ khó **Khó → Rất khó → Cực khó (🔥)**, nhiều câu **liên chương** (vd KRAS: oncogene→somatic→companion Dx). Làm sau khi đã luyện xong 6 bộ theo chương. Có thang tự chấm ở cuối file.

## 🎚️ Nhãn độ khó (mỗi câu có 1 nhãn)
| Nhãn | Ý nghĩa |
|---|---|
| 🟢 **TB** | Kiểm tra kiến thức nền, ít bẫy |
| 🟠 **Khó** | Có distractor tinh vi, cần phân biệt cặp khái niệm |
| 🔴 **Rất khó** | Nhiều bẫy, số liệu chính xác, tình huống, hoặc "chọn tất cả câu SAI" |
| 🔥 **Cực khó** | (chỉ có ở đề tổng hợp) Liên chương, tính toán, bẫy kép, suy luận nhiều bước |

## Cách dùng hiệu quả
1. **Không mở `▸ Đáp án` vội.** Với mỗi câu, chọn **tất cả** phương án bạn cho là đúng — đừng dừng ở 1.
2. Xét **từng phương án như một câu Đúng/Sai độc lập** (đây là mấu chốt của multiple-select).
3. Mở khối `▸ Đáp án`: nó giải thích **vì sao đúng (✅)** và **vì sao sai (❌)** cho từng phương án, kèm tên **🎯 bẫy**.
4. Câu nào sai → đọc lại mục tương ứng trong `../on_tap/` (đã có nhãn 🔴/🟡/⚪ + mục "Điểm tủ").
5. Lượt 2: chỉ làm lại các câu 🔴 **Rất khó** để luyện phản xạ bẫy.

> 💡 Khối `▸ Đáp án` gấp lại được trong trình xem Markdown (VS Code preview, GitHub). Nếu đọc raw text, đáp án nằm ngay dưới câu — tự che bằng mắt.

## Mẹo làm bài multiple-select (đề khó)
- Cảnh giác **từ tuyệt đối**: "luôn", "chỉ", "không bao giờ", "mọi", "100%", "hoàn toàn" → thường **sai**.
- Cảnh giác **đảo ngược cặp khái niệm**: germline↔somatic, PK↔PD, agonist↔antagonist, intrinsic↔post-hoc, GAN↔WGAN, transition↔transversion, purine↔pyrimidine, potency↔efficacy, Hit↔Lead, absolute↔relative risk, FASTA↔FASTQ, nonsense↔missense.
- Cảnh giác **gán sai ví dụ**: TP53 (suppressor, không phải oncogene), Herceptin (biologics), Imatinib (đa đích), DTI (link prediction), Fidelity (đo bằng PGI).
- Cảnh giác **số liệu bẫy**: QD<2, TI=TD50/ED50, 1 start/3 stop codon, 61 tRNA, WES~1,4%, VQSR chạy riêng SNP/INDEL, HGP ~92%.
- Nhớ có câu **không có đáp án đúng** (toàn bộ đều sai) — đừng ép chọn nếu mọi phương án đều sai.
