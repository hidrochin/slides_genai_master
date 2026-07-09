# A — Tổng quan Công nghệ Tiếng nói (Speech Technology)

> Nguồn: `00 - Speech Technology`, `01 - Articulatory Phonetics` (phần Introduction). Cụm nền tảng, nhiều câu hỏi khái niệm/phân loại tác vụ.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [B-ngữ-âm-học](B-ngu-am-hoc.md) · [C-tiếng-Việt](C-am-vi-tieng-viet.md) · [D-DSP](D-xu-ly-tin-hieu.md) · [E-dữ-liệu](E-du-lieu.md) · [F-đánh-giá](F-danh-gia.md) · [G-tổng-hợp](G-tong-hop-tieng-noi.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 1. Speech Technology là gì?

**Định nghĩa:** Nhận dạng (recognition), hiểu (understanding) và **sinh (generation)** tiếng nói con người. Nằm ở giao của **AI + NLP + Human-Computer Interaction (HCI)**.

**Vì sao quan trọng:**
- Hiệu quả giao tiếp người–máy (communication efficiency in HCI).
- Khả năng tiếp cận (accessibility) cho người khuyết tật (VD: screen reader cho người khiếm thị).

## 2. Các tác vụ (Tasks) của Speech Technology — DỄ BỊ HỎI PHÂN LOẠI

| Tác vụ | Viết tắt | Bản chất |
|---|---|---|
| **Automatic Speech Recognition** | ASR / STT | Tiếng nói → văn bản |
| **Text-To-Speech / Speech Synthesis** | TTS | Văn bản → tiếng nói |
| **Speaker Recognition** | — | Xác định/xác minh *ai* đang nói |
| **Speaker Diarization** | — | "Ai nói khi nào" (who spoke when) |
| **Speech Emotion Recognition** | SER | Nhận diện cảm xúc trong giọng nói |
| **Spoken Language Understanding** | SLU | Hiểu ý nghĩa/ý định lời nói |
| **Mispronunciation Detection & Diagnosis** | MD&D | Phát hiện & chẩn đoán lỗi phát âm (VD: ELSA Speak) |
| **Voice Conversion / Cloning** | — | Đổi/sao chép chất giọng |

**Phân biệt bẫy:**
- **Speaker Recognition** (ai nói) ≠ **Speech Recognition** (nói gì).
- **Speaker Verification** (xác minh 1-1: đúng người này không?) ≠ **Speaker Identification** (xác định 1-N: là ai trong tập N người?).
- **Diarization** = phân đoạn theo người nói, KHÔNG cần biết danh tính cụ thể.

## 3. Ứng dụng (Applications)

Virtual Assistant (Siri, Alexa, Google Assistant) · Speech Translation · User Authentication (voice biometrics — VD Nuance) · Automated customer service · Accessibility (screen reader, smart home điều khiển bằng giọng) · Healthcare (chẩn đoán Alzheimer qua speech patterns) · Education (công cụ học ngôn ngữ bằng TTS, ELSA) · Entertainment (audiobook giọng tổng hợp, lồng tiếng phim).

## 4. Lịch sử & bước ngoặt

- Sớm: **First automatic digit recognition** (nhận dạng chữ số đơn, 1 người nói).
- Hiện đại: **Whisper, Tacotron** — deep learning end-to-end.
- **Bước ngoặt về accuracy:** hệ sớm chỉ nhận vài chữ số/1 speaker → hệ hiện đại đạt **gần/ngang mức con người** trên hội thoại tự nhiên. VD: Google đạt **WER 5.1%** trên Switchboard, sánh với con người (~5–6%).

## 5. Xu hướng hiện tại (Current Trends)

- **Deep Learning Dominance:** ASR end-to-end vượt phương pháp truyền thống.
- **Real-Time / On-device:** xử lý ngay trên thiết bị để bảo mật (offline voice command) — VD Vbee on-device 2024, Qualcomm.
- **Multimodal:** kết hợp speech + vision (VD lip-reading).
- **Ethical AI:** giảm thiên lệch (bias), chính sách voice cloning có trách nhiệm.

## 6. Thách thức (Challenges) & Giải pháp — bảng hay ra thi

| Thách thức | Vấn đề | Giải pháp |
|---|---|---|
| **Noise & Variability** | Môi trường thực ≠ dataset kiểm soát | Data augmentation |
| **Accents & Dialects** | Giọng vùng miền bị under-represented | Thu dữ liệu đa dạng (VD Common Voice) |
| **Data Scarcity** | Ngôn ngữ ít tài nguyên (low-resource) bị bỏ quên | Transfer learning + dữ liệu tổng hợp (synthetic) |
| **Ethical Concerns** | Deepfake, xâm phạm riêng tư | Quy định + hướng dẫn đạo đức + watermarking |

## 7. Định hướng tương lai (Future Directions)

- **Universal Models:** khái quát across ngôn ngữ và domain.
- **Emotion Recognition:** tăng tương tác.
- **Low-Power Models:** mở rộng tới vùng sâu vùng xa.
- Tầm nhìn: **dân chủ hoá (democratizing)** công nghệ tiếng nói — tiếp cận được và có đạo đức cho mọi người.

## 8. Bối cảnh AI (dùng để so sánh khái niệm)

- **Rule-based AI** = luật/logic nghiệp vụ do chuyên gia định nghĩa trước. **Machine Learning** = học pattern từ dữ liệu lớn theo thời gian.
- **ML vs Deep Learning:** DL là nhánh ML dùng mạng nơ-ron nhiều tầng, tự học đặc trưng (feature) thay vì kỹ sư thiết kế tay.
- Với tiếng nói: hệ **deep learning hiện đại ít phụ thuộc mã hoá tri thức ngữ âm trực tiếp** — để mô hình tự học ánh xạ chữ↔âm từ dữ liệu thường tốt hơn việc "hand-engineer" cấu trúc ngữ âm. Nhưng hiểu ngữ âm vẫn giúp **mô tả & debug** hệ thống (xem [B-ngữ-âm-học](B-ngu-am-hoc.md)).
