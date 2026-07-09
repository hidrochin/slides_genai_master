# PLAYBOOK THỰC CHIẾN — Kinh nghiệm làm bài toán Speech (ngoài slide)

> Phần này **không có trong PDF** nhưng hay được hỏi kiểu "trong thực tế làm A hay B?", "chọn model nào và vì sao?". Đây là các **quy tắc kinh nghiệm** (rules of thumb) khi làm ASR, MDD, SLU, Speaker, SER và xây dữ liệu. Trắc nghiệm liên quan nằm rải ở [A](../trac_nghiem/A-tong-quan.md), [E](../trac_nghiem/E-du-lieu.md), [H](../trac_nghiem/H-nhan-dang-tieng-noi.md). Ôn lý thuyết nền ở [ONE-PAGER](00-ONE-PAGER.md).

---

## 0. Nguyên tắc vàng xuyên suốt (nhớ trước tiên)

1. **Chọn model theo *bài toán + ràng buộc triển khai*, không theo "mới nhất".** Câu hỏi đầu tiên luôn là: *offline hay streaming? có bao nhiêu dữ liệu có nhãn? chạy trên server hay on-device? độ trễ tối đa?* — trả lời xong mới chọn kiến trúc.
2. **Bắt đầu từ pretrained/foundation model rồi mới fine-tune.** Rất hiếm khi train từ đầu. Whisper/wav2vec2/HuBERT là điểm xuất phát, không phải đích.
3. **Dữ liệu ăn đứt tuning model.** Thêm/ làm sạch dữ liệu đúng phân bố thường tăng chất lượng nhiều hơn đổi kiến trúc. Sửa **10 giờ dữ liệu bẩn** thắng đổi optimizer.
4. **Đo cái người dùng cảm nhận, không chỉ metric đẹp.** WER thấp mà sai toàn tên riêng/số → sản phẩm vẫn tệ. Luôn có **golden set** sát use-case + nghe thử định tính.
5. **Split theo speaker & theo điều kiện thu, không split ngẫu nhiên theo câu.** Đây là lỗi rò rỉ (leakage) phổ biến nhất khiến số đo đẹp giả. Xem [§4](#4-dữ-liệu--mlops--nguyên-tắc-xây-corpus).

---

## 1. ASR thực chiến

### 1.1 Chọn model (nguyên lý D, không phải E)
| Model | Chọn khi | Vì (nguyên lý) | Đừng chọn nếu |
|---|---|---|---|
| **Whisper** (encoder-decoder, SSL 680k giờ) | Cần **đa ngôn ngữ, robust nhiễu, offline**, ít dữ liệu fine-tune | Đã thấy dữ liệu web khổng lồ → zero/low-shot tốt, tự chuẩn hoá dấu câu | Cần **streaming** thật (Whisper là offline, cần cả đoạn) |
| **wav2vec2 / XLSR + CTC** | **Low-resource**, muốn fine-tune trên ngôn ngữ/lĩnh vực riêng, cần latency thấp | SSL pretrained → fine-tune vài chục giờ đã tốt; CTC nhẹ, nhanh | Cần ngữ cảnh dài (CTC giả định output độc lập → cần LM ngoài) |
| **Conformer/RNN-T** | **Streaming on-device** (trợ lý giọng nói) | RNN-T emit token-by-token + Predictor context-aware; Conformer bắt cả cục bộ lẫn toàn cục | Chỉ cần batch offline (AED/Whisper đơn giản hơn, chất lượng cao) |

**Quy tắc:** *streaming ⇒ RNN-T/Conformer; offline chất lượng cao ⇒ AED/Whisper; low-resource fine-tune ⇒ wav2vec2/XLSR.* (Đối chiếu [H](../trac_nghiem/H-nhan-dang-tieng-noi.md).)

### 1.2 Làm gì / không làm gì
- **Làm:** resample về **16 kHz mono** trước khi đưa vào ASR (chuẩn ngành). **Không** giữ 44.1 kHz stereo — vô ích, chỉ tốn tính (formant nằm dưới 8 kHz).
- **Làm:** chuẩn hoá text 2 chiều nhất quán khi tính WER (lowercase, bung số/viết tắt, bỏ dấu câu **theo cùng một quy ước** cho ref & hyp). **Không** so WER giữa hai pipeline chuẩn hoá khác nhau.
- **Làm:** dùng **CER/SylER cho tiếng Việt** khi ranh giới từ nhập nhằng; báo cáo kèm WER. Xem [F-Câu19](../trac_nghiem/F-danh-gia.md).
- **Làm:** với tên riêng/thuật ngữ/số hiệu → **contextual biasing / shallow fusion LM / hotword list**, hoặc hậu xử lý bằng NER. **Không** kỳ vọng model gốc tự đúng entity hiếm.
- **Không:** tin WER trung bình mà bỏ qua phân bố lỗi — luôn xem **error analysis** (lỗi ở số? tên riêng? câu dài? một accent cụ thể?).
- **Bẫy thực tế:** audio có khoảng lặng dài / nhạc nền → Whisper hay **"ảo giác" (hallucinate)** lặp câu → WER có thể **> 100%**. Giải: VAD cắt lặng, chặn lặp, giới hạn độ dài.

### 1.3 Tiếng Việt riêng
- **Thanh điệu là ngữ nghĩa**, nhưng đa số ASR học ngầm qua acoustic; lỗi hay gặp là **sai dấu** (huyền/sắc/hỏi/ngã) → cân nhắc LM mức âm tiết.
- **Đồng âm d/gi/r → /z/** (giọng Bắc): âm→chữ nhập nhằng, phải dựa **LM/ngữ cảnh** phân biệt. Xem [C-Câu17](../trac_nghiem/C-am-vi-tieng-viet.md).
- **Chuẩn hoá số/ngày/đơn vị** ("15/3", "TP.HCM", "2 triệu") là nguồn lỗi lớn ở cả front-end (TTS) lẫn scoring (ASR).

---

## 2. MDD — Mispronunciation Detection & Diagnosis (kiểu ELSA)

Bài toán: chấm **người học L2** phát âm đúng/sai ở mức **âm vị**, và **chẩn đoán** sai thế nào để phản hồi. Khác hẳn ASR (ASR muốn hiểu *nội dung*; MDD muốn biết *phát âm có khớp chuẩn không*).

### 2.1 Nguyên lý cốt lõi
- **GOP (Goodness of Pronunciation):** điểm phát âm cho từng phone = log-posterior của phone chuẩn (canonical) từ acoustic model, so với các phone cạnh tranh. **Làm:** dùng acoustic model mạnh + **forced alignment với chuỗi phone chuẩn** của từ đích. **Không** dùng WER (WER đo nội dung, không đo "đúng chuẩn phát âm").
- **Có canonical transcript** (biết người học *định* nói gì) → đây là bài toán **so khớp phone thực tế vs phone kỳ vọng**, không phải nhận dạng tự do.
- **Diagnosis > Detection:** không chỉ báo "sai", mà chỉ ra *sai kiểu gì* (thay /θ/→/t/, thiếu âm cuối, sai trọng âm) để người học sửa.

### 2.2 Dữ liệu & phone set (làm A không làm B)
- **Làm:** thu **L2 speech có annotation lỗi phát âm** của giáo viên (đắt, hiếm nhưng là vàng). **Không** chỉ train trên giọng bản ngữ rồi kỳ vọng bắt được lỗi L2 — model sẽ "khoan dung" quá mức.
- **Bù dữ liệu hiếm:** sinh **lỗi giả** (phone substitution theo L1→L2 interference), dùng bản ngữ làm **positive**, và **weak label** từ model lớn.
- **Chọn phone set theo cặp ngôn ngữ:** ưu tiên các tương phản mà L1 **không có** (VD người Việt: /θ/-/s/, âm cuối /t/-/k/, cụm phụ âm cuối, phân biệt voicing cuối). Xem tương phản voicing ở [B-Câu7](../trac_nghiem/B-ngu-am-hoc.md).
- **Accent-aware:** đừng phạt biến thể chấp nhận được (giọng vùng) như lỗi — định nghĩa rõ "chuẩn" nào đang chấm.

### 2.3 Đo lường
- Dùng **detection metrics**: precision/recall của việc phát hiện lỗi, **False Acceptance** (bỏ sót lỗi) vs **False Rejection** (báo nhầm người đúng) — giống cân bằng FAR/FRR ở verification. Ưu tiên **recall lỗi** vừa đủ để không làm nản người học bằng false alarm.

---

## 3. SLU / Speaker / SER

### 3.1 SLU — Spoken Language Understanding (intent + slot)
- **Cascade (ASR → NLU trên text):** dùng lại ASR & NLU mạnh sẵn có, **dễ debug**, nhưng **lỗi ASR trôi xuống** và **mất paralinguistic** (ngữ điệu, cảm xúc). **Làm:** train NLU **trên chính output ASR** (có lỗi) chứ không phải text sạch → NLU quen nhiễu.
- **E2E (audio → intent):** giữ được ngữ điệu, tránh error propagation, nhưng **đói dữ liệu** (cặp audio↔intent hiếm) và khó debug.
- **Quy tắc:** *ít dữ liệu, cần ra sản phẩm nhanh, cần log/debug ⇒ cascade; nhiều dữ liệu audio-nhãn & cần bắt sắc thái giọng ⇒ E2E.* Xem [A-Câu13](../trac_nghiem/A-tong-quan.md).

### 3.2 Speaker Verification / Diarization
- **Embedding là vua:** x-vector → **ECAPA-TDNN** (SOTA phổ biến) sinh **speaker embedding**; so bằng **cosine** (+ AS-norm/PLDA để chuẩn hoá điểm). **Verification 1-1 ⇒ EER**; **Identification 1-N ⇒ accuracy/top-k**. Xem [F](../trac_nghiem/F-danh-gia.md).
- **Diarization pipeline** ("ai nói khi nào"): **VAD → cắt đoạn → embedding từng đoạn → clustering (AHC/spectral)** → gán nhãn; xử lý **overlap** là phần khó nhất.
- **Enrollment quality quyết định:** vài giây sạch cho embedding tốt; **không** enroll bằng audio nhiễu/nhiều người.
- **Anti-spoofing bắt buộc** cho xác thực: chạy **countermeasure (PAD)** song song để bắt replay/deepfake (artifact vocoder). Xem [A-Câu16](../trac_nghiem/A-tong-quan.md).

### 3.3 SER — Speech Emotion Recognition
- **Bẫy dữ liệu lớn nhất:** corpus cảm xúc **diễn (acted)** như IEMOCAP không giống cảm xúc **tự nhiên** → model học "diễn" chứ không phải cảm xúc thật. **Làm:** validate trên dữ liệu tự nhiên/in-the-wild.
- **Rò rỉ theo speaker:** cùng người ở train & test → model nhớ giọng chứ không học cảm xúc. **Bắt buộc speaker-independent split.**
- **Mất cân bằng lớp** (neutral áp đảo) → dùng **macro-F1/UAR** thay vì accuracy; cân nhắc class weighting.

---

## 4. Dữ liệu & MLOps — nguyên tắc xây corpus

### 4.1 Làm A — KHÔNG làm B (bảng ghim)
| Làm (A) | Không làm (B) | Vì |
|---|---|---|
| Split **theo speaker** (và theo phiên/thiết bị) | Split ngẫu nhiên theo câu | Cùng giọng ở train+test → **leakage**, WER/accuracy đẹp giả. Xem [E-Câu16](../trac_nghiem/E-du-lieu.md) |
| Chọn augmentation **theo bất biến của bài toán** | Dùng một bộ augment cho mọi bài toán | Speed/pitch perturb phá đặc trưng của **speaker verification**; nhưng tốt cho ASR robustness. Xem [E-Câu17](../trac_nghiem/E-du-lieu.md) |
| **Giữ một golden test set cố định**, không đụng vào | Đổi test set mỗi lần đo | Test trôi → không so được tiến bộ qua thời gian |
| Kiểm định **ý nghĩa thống kê** trước khi tuyên bố cải thiện | Kết luận B tốt hơn A vì WER lệch 0.3% | Chênh nhỏ có thể do nhiễu. Xem [F-Câu21](../trac_nghiem/F-danh-gia.md) |
| Đo **IAA (Cohen/Fleiss Kappa)** cho nhãn người | Tin nhãn một annotator | Nhãn không đồng thuận → trần hiệu năng ảo |
| **VAD chunk** audio dài rồi mới ASR | Đưa file 1 giờ thẳng vào model | Bộ nhớ + hallucination ở khoảng lặng dài |
| Trộn **dữ liệu nhãn thật** khi pseudo-label | Tự train vòng lặp chỉ trên nhãn tự sinh | **Confirmation bias** khuếch đại lỗi. Xem [E-Câu20](../trac_nghiem/E-du-lieu.md) |

### 4.2 Quy trình & giám sát
- **Pipeline dữ liệu (nhắc lại):** Collection → Annotation (human/weak/pseudo) → Forced Alignment → Processing (VAD, diarization, denoise, trim, **resample 16 kHz**) → Augmentation → Benchmark. Xem [ONE-PAGER](00-ONE-PAGER.md).
- **Version cả dữ liệu lẫn model.** Biết mỗi số đo ứng với data version nào.
- **Offline ≠ online:** WER trên test tĩnh **luôn lạc quan** hơn thực tế (mic khác, nhiễu khác, domain trôi). **Giám sát drift** sau khi deploy; thu lại mẫu lỗi để cải thiện vòng sau.
- **Ưu tiên sửa lỗi hệ thống, không đuổi theo số lẻ:** phân tích lỗi theo nhóm (accent, số, tên riêng, độ dài) và sửa nhóm lỗi lớn nhất trước.

---

## 5. Bảng chọn nhanh "bài toán → hình dạng → metric"

| Bài toán | Hình dạng | Metric chính | Model tiêu biểu |
|---|---|---|---|
| **ASR** | seq2seq (audio→text) | WER/CER, RTF | Whisper, wav2vec2, Conformer-RNNT |
| **MDD** | so khớp phone (có canonical) | GOP, precision/recall lỗi | Acoustic model + forced alignment |
| **SLU** | intent (phân loại) + slot (gán nhãn chuỗi) | intent acc, slot F1 | Cascade ASR→NLU / E2E |
| **Speaker Verification** | nhị phân 1-1 | **EER**, t-DCF (kèm anti-spoof) | ECAPA-TDNN + cosine/PLDA |
| **Speaker Identification** | phân loại 1-N | accuracy, top-k | ECAPA-TDNN |
| **Diarization** | phân đoạn theo người | DER | VAD + embed + clustering |
| **SER** | phân loại nhãn cảm xúc | UAR/macro-F1 | SSL feature + classifier |
| **TTS** | text→audio | MOS/CMOS (chủ quan), MCD/RTF (khách quan) | FastSpeech2 + HiFi-GAN, VALL-E |

> **Câu thần chú thi:** *"Bài toán này hình dạng gì (seq2seq / 1-1 / 1-N / phân loại), ràng buộc gì (streaming? dữ liệu? on-device?), nên metric nào và model nào theo nguyên lý gì"* — trả lời được là làm được phần lớn câu hỏi thực tế.
