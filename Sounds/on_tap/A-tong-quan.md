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

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. Ba tầng thông tin trong tín hiệu tiếng nói
Cùng một sóng âm chứa đồng thời, và mỗi tác vụ "rút" một tầng khác nhau:
- **Linguistic** (nói *gì*): từ, âm vị → **ASR, SLU**.
- **Paralinguistic** (nói *thế nào*): cảm xúc, nhấn nhá, thái độ, sức khoẻ → **SER, prosody, chẩn đoán y tế**.
- **Extralinguistic** (nói bởi *ai*, ở *đâu*): danh tính, giới, tuổi, accent, kênh/phòng → **Speaker ID/Verification, Diarization**.
- ⇒ Chọn feature/augmentation theo tầng cần: ASR muốn **bất biến speaker**; speaker verification muốn **bất biến nội dung**. Đây là lý do augmentation phải khớp bài toán ([E §N3](E-du-lieu.md)).

### N2. Khung noisy-channel hợp nhất các tác vụ
- Rất nhiều tác vụ speech là **suy diễn Bayes** trên kênh nhiễu: `Ŷ = argmax P(X|Y)P(Y)`.
  - ASR: Y = chuỗi từ ([H §3](H-nhan-dang-tieng-noi.md)); TTS: bài toán **ngược** (sinh có điều kiện, [G §N1](G-tong-hop-tieng-noi.md)).
- **Hình dạng bài toán** quyết định model & metric: **seq2seq** (ASR/TTS) · **1-1 nhị phân** (verification → EER) · **1-N phân loại** (identification/SER → accuracy) · **phân đoạn** (diarization → DER). Nắm "hình dạng" là chìa khoá trả lời câu hỏi thực chiến ([A-Câu15](../trac_nghiem/A-tong-quan.md)).

### N3. Cocktail party & tách nguồn
- Bài toán **cocktail party** (nghe một giọng giữa nhiều giọng) là lõi của **speech separation** (Conv-TasNet, SepFormer), **target speaker extraction**, và **overlap** trong diarization — phần khó nhất của xử lý hội thoại thực.

### N4. Bước ngoặt Foundation Models & SSL
- Trước 2020: pipeline modular, feature tay (MFCC), cần **nhiều nhãn**. Sau 2020: **pretrain SSL trên audio không nhãn** (wav2vec2, HuBERT, Whisper) → **một backbone** fine-tune cho nhiều tác vụ, **low-resource friendly**, multilingual/zero-shot.
- Hệ quả nghiên cứu: **benchmark saturation** (WER LibriSpeech ~2%) đẩy trọng tâm sang **robustness thực tế**, **đa ngôn ngữ/low-resource**, **on-device**, và **đạo đức** (deepfake, watermarking, consent) — đúng các "xu hướng/thách thức" ở §5–6 nhưng ở tầng nguyên nhân.

### N5. Khoảng cách benchmark ↔ thực tế
- Số đẹp trên test tĩnh **không** đảm bảo sản phẩm tốt: đổi mic/nhiễu/domain, tên riêng & số, code-switching, accent thiểu số. ⇒ tư duy **hệ thống**: đo trên **golden set sát use-case**, giám sát **drift**, và vòng lặp data-centric (thu lỗi thực → sửa dữ liệu). Xem [playbook thực chiến](I-thuc-hanh-kinh-nghiem.md).
