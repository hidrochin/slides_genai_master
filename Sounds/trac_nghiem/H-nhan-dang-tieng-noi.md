# TRẮC NGHIỆM — Cụm H: Nhận dạng Tiếng nói / ASR (23 câu)
Nguồn: `07 - Automatic Speech Recognition` + kiến thức thực chiến. Ôn kèm [H-nhận-dạng](../on_tap/H-nhan-dang-tieng-noi.md) và [playbook thực chiến](../on_tap/I-thuc-hanh-kinh-nghiem.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)/(Cực khó)** = suy luận/tính toán/phân biệt bẫy. Câu 18–23 đi sâu hơn slide (decode, fusion, streaming).

---

**Câu 1.** (Khó) Bài toán ASR được phát biểu theo Bayes là gì?
- A. Ŵ = argmax P(X|W)·P(W), trong đó P(X|W) là Acoustic Model, P(W) là Language Model
- B. Ŵ = argmax P(W|X)·P(X), trong đó P(X) là Acoustic Model
- C. Ŵ = argmax P(X)·P(W), hai thành phần độc lập không liên quan AM/LM
- D. Ŵ = argmin P(X|W) + P(W)

<details><summary>Đáp án</summary>

**A.** `Ŵ = argmax_W P(W|X) = argmax_W P(X|W)·P(W)`, với **P(X|W) = Acoustic Model** (~phonetic modeling), **P(W) = Language Model**. X cố định. Đây là công thức nền của ASR truyền thống.
</details>

---

**Câu 2.** (Nhiều đáp án) Bốn thành phần của kiến trúc ASR truyền thống là gì?
- A. Acoustic Model
- B. Language Model
- C. Decoder
- D. Adaptation
- E. Vocoder

<details><summary>Đáp án</summary>

**A, B, C, D.** AM (tri thức acoustic/phonetic), LM (từ hợp lệ & thứ tự), Decoder (sinh chuỗi từ posterior cực đại), Adaptation (chỉnh AM/LM). **Vocoder** thuộc **TTS** (spectrogram→waveform), không phải ASR.
</details>

---

**Câu 3.** (Khó) LMSF (Language Model Scaling Factor) cần thiết vì lý do gì?
- A. Vì AM có xu hướng đánh giá thấp P(X|W) do giả định độc lập trên xác suất phone, nên cần hiệu chỉnh trade-off với LM
- B. Vì LM luôn chính xác tuyệt đối nên cần khuếch đại lên
- C. Vì decoder không thể xử lý xác suất
- D. Vì cần chuyển đổi giữa sample rate và bit depth

<details><summary>Đáp án</summary>

**A.** AM **đánh giá thấp P(X|W)** do **independence assumption** trên phone → LMSF (λ₁) tái cân bằng trade-off giữa acoustic score và chuỗi từ phổ biến (LM). Không phải vì LM hoàn hảo (B).
</details>

---

**Câu 4.** Vì sao dùng Hamming window thay vì Rectangular window khi chia frame?
- A. Hamming co giá trị tín hiệu về 0 ở biên cửa sổ, tránh gián đoạn (discontinuity) → giảm spectral leakage
- B. Hamming làm tăng kích thước frame gấp đôi
- C. Rectangular không chia được frame
- D. Hamming chuyển tín hiệu sang miền thời gian

<details><summary>Đáp án</summary>

**A.** Hamming **shrink giá trị về 0 ở biên** → tránh discontinuity so với Rectangular → **giảm spectral leakage**. VD frame 25 ms, stride 10 ms.
</details>

---

**Câu 5.** Đặc điểm của Mel filter bank là gì?
- A. Phân giải rất mịn ở tần thấp, thô ở tần cao — khớp với việc tai người kém nhạy ở tần cao
- B. Phân giải đều nhau ở mọi dải tần
- C. Phân giải mịn ở tần cao, thô ở tần thấp
- D. Chỉ thu năng lượng ở một tần số duy nhất

<details><summary>Đáp án</summary>

**A.** Mel filter bank giãn **logarit**: mịn ở **tần thấp**, thô ở **tần cao** — vì **tai người kém nhạy ở tần cao**. Sau đó lấy log. C đảo ngược.
</details>

---

**Câu 6.** (Khó) Hai vấn đề đặc thù của ASR mà kiến trúc Attention Encoder-Decoder (AED/LAS) giải quyết là gì?
- A. Length differences (chuỗi acoustic dài → chuỗi ký tự ngắn) và input-output mapping (không rõ phần nào của X map phần nào của Y)
- B. Bit depth thấp và sample rate cao
- C. Thiếu dữ liệu train và thừa tham số model
- D. Nhiễu nền và reverberation trong audio

<details><summary>Đáp án</summary>

**A.** AED giải: **length differences** (compression stage rút ngắn chuỗi acoustic dài, VD 200 frame → 5 ký tự) và **input-output mapping** (attention align input↔output không cần cấu trúc định trước).
</details>

---

**Câu 7.** (Nhiều đáp án) Đâu là các nhược điểm của mô hình Attention-based (AED) trong ASR?
- A. Attention đắt cho chuỗi dài — độ phức tạp O(mn) với m, n lớn
- B. Không chạy online/real-time vì cần toàn bộ input trước khi decode
- C. Không tận dụng tính đơn điệu (monotonic) của alignment speech
- D. Không thể học từ dữ liệu có nhãn
- E. Bắt buộc phải có forced alignment frame-level

<details><summary>Đáp án</summary>

**A, B, C.** Ba nhược điểm: O(mn) đắt, không online, thiếu monotonic inductive bias (nên khó train, phải thêm auxiliary loss). D sai (AED học được từ cặp có nhãn); E sai (attention **không cần** forced alignment).
</details>

---

**Câu 8.** Thuật toán của CTC hoạt động thế nào?
- A. Xuất 1 ký tự mỗi frame (output cùng độ dài input), rồi áp collapsing function gộp ký tự giống nhau liên tiếp
- B. Xuất một ký tự cho toàn bộ câu, không cần frame
- C. Chỉ hoạt động khi input và output có độ dài bằng nhau tuyệt đối
- D. Dùng attention để align từng ký tự với từng frame

<details><summary>Đáp án</summary>

**A.** CTC: mỗi frame → 1 ký tự (output = độ dài input) → **collapsing function** gộp ký tự lặp liên tiếp → chuỗi ngắn hơn. Dùng **blank token** để phân tách ký tự lặp thật & khoảng trống. Không dùng attention (D).
</details>

---

**Câu 9.** (Khó) Hai vấn đề (Problem 1 & 2) của CTC là gì?
- A. P1: độ dài output phải nhỏ hơn input (cản pooling nhiều); P2: giả định các output độc lập nhau → dễ ra output sai kiểu "I eight food"
- B. P1: output phải dài hơn input; P2: output phụ thuộc nhau quá mức
- C. P1: cần forced alignment frame-level; P2: không dùng được blank token
- D. P1: chỉ chạy offline; P2: attention quá đắt

<details><summary>Đáp án</summary>

**A.** **Problem 1:** output **ngắn hơn** input (cản kiến trúc pooling nhiều để tăng tốc). **Problem 2:** **giả định output độc lập** → sinh output vô lý ("I eight food" thay vì "I ate food"), cần search + LM phụ. RNN-T ra đời để giải cả hai.
</details>

---

**Câu 10.** RNN-T (Transducer) giải hai vấn đề của CTC bằng cách nào?
- A. Cho phép nhiều output cho mỗi input (giải P1) và thêm Predictor + Joiner network (giải P2)
- B. Loại bỏ encoder và chỉ dùng attention
- C. Bắt buộc output ngắn hơn input và giữ giả định độc lập
- D. Dùng HMM thay cho mạng nơ-ron

<details><summary>Đáp án</summary>

**A.** RNN-T: **nhiều output/input** (giải Problem 1) + **Predictor network** (autoregressive, như LM) & **Joiner network** (giải Problem 2 — output không còn độc lập). Đây là điểm mấu chốt so CTC.
</details>

---

**Câu 11.** (Nhiều đáp án) Vì sao RNN-T phù hợp cho streaming ASR?
- A. Xử lý audio frame-by-frame, không cần cả câu trước
- B. Incremental output — emit token khi audio đang tới
- C. Monotonic decoding khớp bản chất trái→phải của lời nói
- D. Predictor giữ output trước → context-aware
- E. Phải chờ toàn bộ utterance rồi mới collapse như CTC

<details><summary>Đáp án</summary>

**A, B, C, D.** Bốn lý do streaming-friendly. E chính là đặc điểm của **CTC** (thường chờ cả chunk rồi collapse) — ngược với RNN-T (token-by-token).
</details>

---

**Câu 12.** (Khó) So sánh CTC và RNN-T về khả năng mô hình ngữ cảnh. Phát biểu nào ĐÚNG?
- A. CTC không có decoder → output độc lập, thiếu ngữ cảnh; RNN-T có Predictor (autoregressive) → context-aware
- B. CTC có Predictor network còn RNN-T thì không
- C. Cả hai đều có internal LM mạnh như nhau
- D. RNN-T giả định output độc lập, CTC thì không

<details><summary>Đáp án</summary>

**A.** CTC **không có decoder** → output độc lập, thiếu ngữ cảnh (cần LM ngoài). RNN-T có **Predictor** đóng vai internal LM → context-aware. B, D đảo ngược.
</details>

---

**Câu 13.** SSL (Self-Supervised Learning) trong ASR hoạt động thế nào?
- A. Pre-train trên lượng lớn audio KHÔNG nhãn, học biểu diễn bằng cách dự đoán phần bị mask
- B. Chỉ train trên dữ liệu có nhãn thủ công của con người
- C. Không cần dữ liệu, sinh biểu diễn ngẫu nhiên
- D. Chuyển audio thành text bằng luật cứng

<details><summary>Đáp án</summary>

**A.** SSL pretrain trên **audio không nhãn** quy mô lớn, học biểu diễn qua **masking-based prediction** (hoặc task tự định nghĩa) → nắm thông tin acoustic/phonetic tổng quát, rồi fine-tune. B ngược (SSL tận dụng dữ liệu **chưa** nhãn).
</details>

---

**Câu 14.** (Khó) Trong bảng SSL models, model nào multilingual "out-of-the-box", train 680k giờ trên 96+ ngôn ngữ?
- A. Whisper
- B. Wav2vec 2.0
- C. HuBERT
- D. Data2vec

<details><summary>Đáp án</summary>

**A.** **Whisper** train **680k giờ, 96+ ngôn ngữ**, hỗ trợ multilingual ASR + translation ngay. Wav2vec 2.0 & HuBERT gốc **monolingual** (English, cần fine-tune). (XLSR — cross-lingual Wav2vec 2.0 — mới là 53+ ngôn ngữ.)
</details>

---

**Câu 15.** (Nhiều đáp án) Vì sao kết hợp SSL với Transformer trong ASR?
- A. Transformer dùng self-attention nắm phụ thuộc xa tốt hơn RNN
- B. Transformer cho phép xử lý song song → train nhanh hơn
- C. SSL giúp low-resource friendly (ít fine-tune vẫn tốt) và multilingual/zero-shot
- D. SSL loại bỏ hoàn toàn nhu cầu dữ liệu audio
- E. Transformer chỉ chạy được trên dữ liệu có nhãn thủ công

<details><summary>Đáp án</summary>

**A, B, C.** Transformer: self-attention (phụ thuộc xa) + song song hoá (train nhanh). SSL: low-resource friendly, multilingual/zero-shot (Whisper, HuBERT). D sai (vẫn cần audio, chỉ là không nhãn); E sai (SSL dùng audio **không** nhãn).
</details>

---

**Câu 16.** Theo dòng lịch sử ASR, thứ tự tiến hoá kỹ thuật nào ĐÚNG?
- A. Template Matching → HMM → GMM-HMM → Deep Learning (CTC, RNN-T) → SSL + Transformers
- B. Deep Learning → HMM → Template Matching → SSL
- C. SSL + Transformers → GMM-HMM → Template Matching → CTC
- D. HMM → Template Matching → SSL → GMM-HMM

<details><summary>Đáp án</summary>

**A.** 1950s Template Matching → 1980s HMM → 1990s GMM-HMM → 2010s Deep Learning (CTC, RNN-T) → 2020s SSL + Transformers (Whisper, Wav2Vec2). Các phương án khác xáo trộn mốc thời gian.
</details>

---

**Câu 17.** (Khó) ASR gặp khó với "rare words" và "proper names"; giải pháp nào được nêu?
- A. Mở rộng training data đa dạng + transfer learning + tích hợp NER (Named Entity Recognition)
- B. Giảm kích thước training data để model tập trung hơn
- C. Bỏ hoàn toàn Language Model
- D. Chỉ nhận dạng các từ phổ biến, bỏ qua tên riêng

<details><summary>Đáp án</summary>

**A.** Với rare words/proper names: **expand & diversify data**, **transfer learning**, tích hợp **NER** để nhận diện tên riêng/thuật ngữ theo ngữ cảnh, và tối ưu model/algorithm. B, C, D đều đi ngược hướng cải thiện.
</details>

---

**Câu 18.** (Cực khó) Reference có 4 từ. Hệ ASR sinh ra 9 từ, trong đó khớp đúng 4 từ reference nhưng chèn thêm 5 từ thừa (I=5, S=0, D=0). WER bằng bao nhiêu và nói lên điều gì?
- A. WER = 125% — WER có thể > 100% vì insertion không bị chặn bởi N
- B. WER = 100% — vì hệ sai toàn bộ
- C. WER = 55.6% — vì chia cho số từ ASR (9)
- D. WER = 56% — vì insertion không được tính vào lỗi

<details><summary>Đáp án</summary>

**A.** `WER = (S+D+I)/N = (0+0+5)/4 = 1.25 = 125%`. Đây là bẫy quan trọng: **WER có thể vượt 100%** khi model "ảo giác" chèn nhiều từ (hay gặp với audio nhiễu/khoảng lặng dài). C sai vì mẫu số luôn là **N reference**, không phải số từ output.
</details>

---

**Câu 19.** (Khó) Trong shallow fusion, điểm cho một giả thuyết W được tính `score = log P_AM(X|W) + λ · log P_LM(W)`. Vai trò của external LM và λ là gì?
- A. LM ngoài (train trên text lớn) kéo giả thuyết về phía chuỗi từ hợp lý; λ điều tiết mức tin LM so với acoustic
- B. LM ngoài thay thế hoàn toàn acoustic model; λ là learning rate khi train
- C. LM chỉ dùng lúc train, λ là dropout rate; khi inference bỏ cả hai
- D. LM ngoài làm chậm decode nên λ luôn đặt bằng 0 trong thực tế

<details><summary>Đáp án</summary>

**A.** Shallow fusion cộng log-prob của **external LM** (thường train trên corpus text lớn hơn nhiều transcript audio) vào điểm beam search; **λ** cân bằng acoustic ↔ ngôn ngữ (giống vai trò LMSF ở [Câu 3](#)). Hữu ích cho domain có nhiều thuật ngữ/tên riêng. B, C, D hiểu sai bản chất fusion.
</details>

---

**Câu 20.** (Khó) Vì sao greedy decoding (chọn token xác suất cao nhất mỗi bước) thường cho WER cao hơn beam search?
- A. Greedy chọn tối ưu cục bộ từng bước nên có thể bỏ lỡ chuỗi có tổng xác suất cao hơn; beam giữ nhiều giả thuyết song song
- B. Greedy chậm hơn beam nên bị cắt sớm trước khi hội tụ
- C. Greedy không dùng được acoustic model, chỉ dựa language model
- D. Beam search luôn cho kết quả tệ hơn greedy nhưng nhanh hơn

<details><summary>Đáp án</summary>

**A.** Greedy = tham lam cục bộ, dễ "kẹt" ở nhánh không tối ưu toàn cục; **beam search** giữ *k* giả thuyết tốt nhất, cho phép một lựa chọn kém ở bước sớm dẫn tới tổng điểm cao hơn về sau. Đổi lại beam **chậm hơn** (không phải nhanh hơn như D). Beam width lớn → chính xác hơn nhưng tốn tính.
</details>

---

**Câu 21.** (Cực khó) So với CTC, vì sao RNN-T tốn bộ nhớ và khó train hơn dù cùng học alignment?
- A. RNN-T tính trên lattice 2 chiều (thời gian × nhãn) với Joiner kết hợp mọi cặp encoder-predictor state → tensor lớn hơn nhiều CTC (chỉ 1 chiều thời gian)
- B. RNN-T phải có forced alignment frame-level trước khi train, CTC thì không
- C. RNN-T dùng attention O(mn) còn CTC không dùng attention
- D. RNN-T bắt buộc external LM khi train nên nặng gấp đôi

<details><summary>Đáp án</summary>

**A.** RNN-T marginalize trên **lattice T×U** (frame × token) qua Joiner network → activation/gradient tensor lớn (hay phải dùng function-merging, gradient checkpointing). CTC chỉ cần forward-backward trên **một trục thời gian**. B sai (cả hai **không** cần forced alignment); C sai (RNN-T không dùng attention); D sai (LM ngoài là tuỳ chọn).
</details>

---

**Câu 22.** (Khó) Kiến trúc Conformer cải tiến Transformer encoder cho ASR bằng cách nào?
- A. Chèn module convolution vào giữa các block self-attention để nắm cả phụ thuộc **cục bộ** (conv) lẫn **toàn cục** (attention)
- B. Loại bỏ self-attention, chỉ dùng convolution thuần cho nhẹ
- C. Thay feed-forward bằng HMM để mô hình hoá thời gian
- D. Dùng attention hai chiều nên chỉ chạy được offline, không streaming

<details><summary>Đáp án</summary>

**A.** **Conformer = Convolution + Transformer**: self-attention bắt quan hệ **xa/toàn cục**, convolution bắt pattern **cục bộ** (formant, transition) → SOTA nhiều benchmark ASR. B, C sai bản chất; D sai (có biến thể streaming với masked/limited-context attention).
</details>

---

**Câu 23.** (Cực khó) Trong streaming ASR, tăng "lookahead" (cho model nhìn thêm vài frame tương lai) tác động thế nào?
- A. Giảm WER (ngữ cảnh tương lai giúp quyết định tốt hơn) nhưng tăng latency — một trade-off phải cân theo ứng dụng
- B. Giảm cả WER lẫn latency vì model thấy nhiều thông tin hơn
- C. Tăng WER và tăng latency — không có lợi ích gì
- D. Không ảnh hưởng WER, chỉ làm model chạy nhanh hơn

<details><summary>Đáp án</summary>

**A.** Nhìn thêm frame tương lai (right context) cho quyết định token tốt hơn ⇒ **WER giảm**, nhưng phải **chờ** frame đó tới ⇒ **latency tăng**. Đây là núm chỉnh cốt lõi của streaming (VD trợ lý giọng nói cần latency thấp phải hi sinh chút WER). B là điều không thể; latency và độ chính xác luôn đánh đổi.
</details>
