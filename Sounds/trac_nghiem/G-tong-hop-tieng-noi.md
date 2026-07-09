# TRẮC NGHIỆM — Cụm G: Tổng hợp Tiếng nói / TTS (21 câu)
Nguồn: `06 - Speech Synthesis` + kiến thức mô hình TTS hiện đại. Ôn kèm [G-tổng-hợp](../on_tap/G-tong-hop-tieng-noi.md) và [playbook thực chiến](../on_tap/I-thuc-hanh-kinh-nghiem.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)/(Cực khó)** = phân biệt bẫy/suy luận sâu. Câu 17–21 nâng cao (attention failure, duration model, vocoder trade-off).

---

**Câu 1.** Quan hệ giữa Speech Synthesis và TTS là gì?
- A. TTS là một loại speech synthesis (chuyển văn bản → tiếng nói)
- B. Speech synthesis là một loại TTS
- C. Hai khái niệm hoàn toàn tách biệt, không liên quan
- D. TTS chuyển tiếng nói → văn bản, synthesis thì ngược lại

<details><summary>Đáp án</summary>

**A.** **TTS ⊂ Speech Synthesis**: synthesis là sinh tiếng nói nói chung (còn có Singing Voice Synthesis từ music score, Voice Conversion từ speech…), TTS là nhánh từ **text**. D nhầm TTS thành STT (ASR).
</details>

---

**Câu 2.** (Khó) Vì sao ánh xạ Text-to-Speech được gọi là "one-to-many"?
- A. Một câu text có thể được nói theo nhiều cách khác nhau (speaker, prosody, emotion, background)
- B. Một âm thanh chỉ ứng với đúng một câu text
- C. Vì mỗi ký tự sinh ra nhiều file audio riêng biệt
- D. Vì TTS luôn tạo nhiều bản sao giống hệt của cùng một audio

<details><summary>Đáp án</summary>

**A.** Text chỉ chứa **content** (what to say); còn **who** (speaker/timbre), **how** (prosody/emotion/style), **where** (background noise) là vô số khả năng → một text ↔ nhiều speech (multi-modal). Đây là lý do TTS khó.
</details>

---

**Câu 3.** (Nhiều đáp án) Nối kỹ thuật tổng hợp với đặc điểm ĐÚNG.
- A. Articulatory: mô phỏng bộ máy cấu âm, phức tạp, chất lượng rất thấp
- B. Concatenative: ghép âm ghi thật, intelligibility cao nhưng cần DB lớn, emotionless
- C. Statistical Parametric (HMM): nhẹ, linh hoạt, nhưng robotic
- D. Neural E2E: cải thiện chất lượng lớn, ít feature engineering tay
- E. Concatenative: nhẹ nhất và biểu cảm nhất trong bốn kỹ thuật

<details><summary>Đáp án</summary>

**A, B, C, D.** Bốn mô tả đúng theo slide. E sai: concatenative cần **DB khổng lồ** (không nhẹ) và **emotionless** (không biểu cảm). "Nhẹ & linh hoạt" là của SPS/HMM.
</details>

---

**Câu 4.** Trong source-filter model (vocoder cổ điển), nguồn kích thích (source excitation) cho âm hữu thanh và vô thanh lần lượt là gì?
- A. Pulse train (hữu thanh) và white noise (vô thanh)
- B. White noise (hữu thanh) và pulse train (vô thanh)
- C. Sine wave (hữu thanh) và square wave (vô thanh)
- D. Mel-spectrogram (hữu thanh) và MFCC (vô thanh)

<details><summary>Đáp án</summary>

**A.** Source-filter (LTI): âm **hữu thanh** dùng **pulse train** (dây thanh rung tuần hoàn), âm **vô thanh** dùng **white noise** (nhiễu). Phần lọc (vocal tract) đặc trưng bởi state-output vector của HMM (mel-cepstral/LSP).
</details>

---

**Câu 5.** Thứ tự đúng của pipeline neural TTS hiện đại (modular) là gì?
- A. Text → Text Analysis (normalization + G2P) → Acoustic Model (→ mel-spectrogram) → Vocoder (→ waveform)
- B. Text → Vocoder → Acoustic Model → Text Analysis → waveform
- C. Text → Acoustic Model → Text Analysis → Vocoder → waveform
- D. Text → G2P → Vocoder → mel-spectrogram → Acoustic Model

<details><summary>Đáp án</summary>

**A.** Frontend (text normalization + G2P) → **Acoustic Model** sinh **mel-spectrogram** → **Vocoder** sinh **waveform**. Vocoder luôn ở **cuối** (spectrogram → audio).
</details>

---

**Câu 6.** (Nhiều đáp án) Text Analysis (frontend) thực hiện những tác vụ nào?
- A. Text normalization (VD "Feb. 25th" → "February twenty fifth")
- B. Grapheme-to-Phoneme (VD "speech" → s p iy ch)
- C. POS tagging và phrase/word/syllable segmentation
- D. Chuyển mel-spectrogram thành waveform
- E. Lượng tử hoá biên độ tín hiệu audio

<details><summary>Đáp án</summary>

**A, B, C.** Frontend biến text → linguistic features: normalization, G2P, segmentation, POS tagging. D là việc của **vocoder**; E là **quantization** trong ADC (cụm DSP) — không thuộc frontend TTS.
</details>

---

**Câu 7.** Trong pipeline TTS, vocoder có vai trò gì?
- A. Chuyển acoustic features (mel-spectrogram) thành waveform miền thời gian
- B. Chuyển text thành linguistic features
- C. Chuyển linguistic features thành mel-spectrogram
- D. Phân tách từ trong câu text

<details><summary>Đáp án</summary>

**A.** Vocoder = **spectrogram → waveform**. B là frontend; C là **acoustic model**; D là segmentation. Vocoder ảnh hưởng lớn naturalness/quality/intelligibility.
</details>

---

**Câu 8.** (Khó) So sánh Griffin-Lim và HiFi-GAN, cùng xu hướng tiến hoá vocoder?
- A. Griffin-Lim cổ điển/robotic; HiFi-GAN neural chất lượng cao/real-time; tiến hoá từ AR (WaveNet) → GAN & diffusion
- B. Griffin-Lim là neural mới nhất; HiFi-GAN là cổ điển
- C. Cả hai đều là autoregressive như WaveNet
- D. HiFi-GAN chậm hơn và robotic hơn Griffin-Lim

<details><summary>Đáp án</summary>

**A.** Griffin-Lim đơn giản → **robotic**; **HiFi-GAN** neural, chất lượng cao, real-time. Vocoder tiến hoá: autoregressive (**WaveNet**) → GAN-based & diffusion-based (hiệu quả hơn). B, D đảo ngược.
</details>

---

**Câu 9.** (Nhiều đáp án) Đâu là ưu điểm của mô hình End-to-End TTS được nêu?
- A. Train bằng cặp text-speech với tối thiểu annotation tay
- B. Không cần alignment tường minh giữa text và speech
- C. Không tích luỹ lỗi / không error propagation vì là một model duy nhất
- D. Luôn nhanh hơn mọi mô hình modular khi inference
- E. Không cần dữ liệu để huấn luyện

<details><summary>Đáp án</summary>

**A, B, C.** Ba ưu điểm theo slide. D sai (tốc độ tuỳ AR/NAR, không "luôn nhanh hơn"). E sai (vẫn cần cặp text-speech để train).
</details>

---

**Câu 10.** Voice Cloning được định nghĩa là gì?
- A. Tổng hợp speech mô phỏng danh tính giọng của một speaker cụ thể, thường từ dữ liệu hạn chế, với text tuỳ ý
- B. Chuyển giọng nói thành văn bản của một người cụ thể
- C. Sao chép file audio gốc mà không thay đổi nội dung
- D. Nhận diện cảm xúc trong giọng nói người nói

<details><summary>Đáp án</summary>

**A.** Voice cloning = tái tạo **danh tính giọng** của target speaker (thường **low-resource**, vài phút), cho phép nhập **text bất kỳ**. B là ASR; D là SER.
</details>

---

**Câu 11.** (Khó) Zero-shot voice cloning khác Multi-speaker TTS + Embedding ở điểm cốt lõi nào?
- A. Zero-shot chạy với speaker chưa từng thấy, không cần fine-tune (dùng speaker encoder pretrained như GE2E)
- B. Zero-shot bắt buộc fine-tune lại toàn bộ model cho mỗi speaker mới
- C. Multi-speaker + embedding không dùng speaker embedding
- D. Zero-shot chỉ hoạt động với đúng các speaker trong tập train

<details><summary>Đáp án</summary>

**A.** **Zero-shot** dùng **speaker encoder pretrained (GE2E)** + TTS backbone chung → clone **speaker chưa từng thấy, KHÔNG fine-tune** (VD YourTTS, VALL-E, StyleTTS2). B, D mâu thuẫn định nghĩa zero-shot.
</details>

---

**Câu 12.** VALL-E (Microsoft 2023) có đặc điểm nổi bật nào?
- A. Zero-shot voice cloning với prompt ~3 giây; không sinh spectrogram mà dự đoán mã rời rạc RVQ
- B. Cần ít nhất 1 giờ audio của target speaker để clone
- C. Sinh trực tiếp mel-spectrogram bằng HMM
- D. Chỉ hoạt động cho tiếng Anh và không giữ được ngữ điệu

<details><summary>Đáp án</summary>

**A.** VALL-E: **zero-shot prompt 3 giây**, là **neural codec LM** — **không sinh spectrogram** mà dự đoán **discrete codes (RVQ)** rồi tái tạo, giữ được ngữ điệu/tốc độ/chất giọng. B (cần 1 giờ) mâu thuẫn zero-shot.
</details>

---

**Câu 13.** (Khó) RVQ (Residual Vector Quantization) cải tiến VQ-VAE bằng cách nào?
- A. Dùng nhiều tầng lượng tử kế tiếp, mỗi tầng học phần dư (residual) của tầng trước → tăng biểu diễn mà không cần codebook quá lớn
- B. Dùng một codebook duy nhất cực lớn cho toàn bộ tín hiệu
- C. Loại bỏ hoàn toàn bước lượng tử hoá
- D. Thay vector quantization bằng continuous latent như VAE thuần

<details><summary>Đáp án</summary>

**A.** RVQ = **multi-stage quantization**, mỗi tầng mã hoá **residual** còn lại của tầng trước → biểu diễn giàu thông tin **mà không cần codebook khổng lồ**. B ngược ý tưởng (RVQ tránh codebook lớn); D là VAE thuần (không rời rạc).
</details>

---

**Câu 14.** (Khó) So sánh AR và NAR Transformer trong TTS+RVQ. Phát biểu nào ĐÚNG?
- A. AR chậm nhưng chất lượng/prosody cao (offline, teacher); NAR nhanh/song song (real-time, student)
- B. AR nhanh và song song hoá cao; NAR chậm vì sinh từng token
- C. AR và NAR có tốc độ và chất lượng như nhau
- D. NAR luôn giữ intonation tốt hơn AR

<details><summary>Đáp án</summary>

**A.** **AR** sinh từng token dựa mọi token trước → **chậm nhưng prosody tốt** (offline high-quality như VALL-E, làm **teacher**). **NAR** sinh song song → **nhanh, real-time** nhưng khó giữ intonation (làm **student** trong distillation). B đảo ngược; D sai (AR giữ intonation tốt hơn).
</details>

---

**Câu 15.** Từ lớn đến nhỏ, các đơn vị âm (speech unit) được sắp xếp thế nào?
- A. Utterance → Prosodic Phrase → Word → Syllable → Phoneme
- B. Phoneme → Syllable → Word → Prosodic Phrase → Utterance
- C. Word → Phoneme → Syllable → Utterance → Phrase
- D. Syllable → Phoneme → Word → Utterance → Phrase

<details><summary>Đáp án</summary>

**A.** Lớn → nhỏ: **Utterance** (câu nói) → **Prosodic Phrase** (đoạn) → **Word** → **Syllable** (tiếng) → **Phoneme** (âm vị, segment nhỏ nhất tri giác được). B là thứ tự ngược.
</details>

---

**Câu 16.** (Nhiều đáp án) Thách thức & giải pháp cho TTS tiếng Việt được nêu gồm những cặp nào?
- A. Word Segmentation & Text Normalization → hybrid models
- B. Thiếu speech data chất lượng → semi/self-supervised learning + data augmentation
- C. Prosody Modeling → style/emotion tags, reference encoder
- D. Thanh điệu → bỏ hoàn toàn thông tin thanh khi tổng hợp
- E. Tăng sample rate lên 192 kHz để giải quyết mọi vấn đề

<details><summary>Đáp án</summary>

**A, B, C.** Ba cặp thách thức-giải pháp đúng cho tiếng Việt. D sai (thanh điệu là bắt buộc, bỏ đi sẽ sai nghĩa — xem [C](../on_tap/C-am-vi-tieng-viet.md)); E là bịa, sample rate không giải quyết segmentation/prosody.
</details>

---

**Câu 17.** (Cực khó) TTS tự hồi quy dựa attention (kiểu Tacotron) hay gặp các lỗi đặc trưng nào, và hướng khắc phục là gì?
- A. Bỏ từ / lặp từ / lẩm bẩm do attention lệch; khắc phục bằng duration predictor tường minh (FastSpeech) hoặc monotonic alignment
- B. Chỉ gặp lỗi sai thanh điệu, khắc phục bằng tăng sample rate
- C. Không bao giờ lỗi vì attention luôn học được alignment hoàn hảo
- D. Lỗi vỡ tiếng do vocoder, khắc phục bằng bỏ acoustic model

<details><summary>Đáp án</summary>

**A.** Attention mềm có thể **skip** (nhảy chữ), **repeat** (lặp), hoặc **mumble** khi alignment trôi, nhất là câu dài/ngoài phân bố. Các model **non-autoregressive** như **FastSpeech** thay attention bằng **duration predictor** (biết mỗi phoneme kéo dài bao nhiêu frame) → alignment ổn định, song song, nhanh. B, C, D sai bản chất.
</details>

---

**Câu 18.** (Khó) Khác biệt cốt lõi giữa Tacotron 2 và FastSpeech 2 về cách xác định độ dài mỗi âm là gì?
- A. Tacotron 2 dùng attention học ngầm alignment (autoregressive); FastSpeech 2 dùng duration predictor tường minh + sinh song song
- B. Cả hai đều autoregressive và dùng attention giống hệt nhau
- C. FastSpeech 2 autoregressive còn Tacotron 2 song song
- D. Cả hai đều là vocoder, không phải acoustic model

<details><summary>Đáp án</summary>

**A.** Cả hai đều là **acoustic model** (text → mel), nhưng **Tacotron 2** *autoregressive* + attention (học alignment ngầm, chậm, dễ lỗi skip/repeat), còn **FastSpeech 2** *non-autoregressive* + **duration predictor** (biết trước độ dài mỗi phoneme → sinh song song, nhanh & ổn định, thêm predictor cho pitch/energy). B, C đảo tính chất; D sai (đều không phải vocoder).
</details>

---

**Câu 19.** (Khó) Vì sao chất lượng vocoder nhiều khi quyết định độ tự nhiên nghe được nhiều hơn cả acoustic model?
- A. Mel-spectrogram là biểu diễn mất mát (thiếu pha); vocoder phải "bù" pha & chi tiết waveform — vocoder kém sẽ tạo tiếng rè/kim loại dù mel đúng
- B. Vocoder sinh cả nội dung ngôn ngữ nên sai từ là do vocoder
- C. Acoustic model không ảnh hưởng chất lượng, chỉ vocoder quan trọng
- D. Vocoder chỉ đổi định dạng file nên không ảnh hưởng âm thanh

<details><summary>Đáp án</summary>

**A.** Mel-spectrogram **bỏ thông tin pha** và nén tần số; vocoder tái tạo waveform phải khôi phục pha + chi tiết high-freq. Vocoder cổ (Griffin-Lim) → robotic/kim loại; neural (HiFi-GAN) → tự nhiên. Nên một mel "đúng" vẫn nghe tệ nếu vocoder yếu. B sai (nội dung do frontend/acoustic model), C, D cường điệu/sai.
</details>

---

**Câu 20.** (Cực khó) Vocoder/model dựa diffusion (VD WaveGrad, DiffWave) đánh đổi điều gì so với GAN-based (HiFi-GAN)?
- A. Diffusion cho chất lượng rất cao & train ổn định nhưng inference qua nhiều bước khử nhiễu → chậm hơn; GAN nhanh (1 lần forward) nhưng train dễ bất ổn
- B. Diffusion nhanh hơn GAN vì chỉ cần một bước sinh duy nhất
- C. GAN cho chất lượng thấp và luôn chậm hơn diffusion
- D. Cả hai đều autoregressive như WaveNet nên tốc độ giống nhau

<details><summary>Đáp án</summary>

**A.** **Diffusion** khử nhiễu **nhiều bước** (chất lượng cao, train ổn định, nhưng inference chậm — trừ khi distill giảm bước). **GAN** sinh **một lần forward** (nhanh, real-time) nhưng huấn luyện dễ mất ổn định (mode collapse, cần cân generator/discriminator). B đảo tốc độ; D sai (không phải AR).
</details>

---

**Câu 21.** (Khó) Khi làm TTS tiếng Việt, vì sao **không** được xử lý thanh điệu như thông tin phụ trợ có thể bỏ qua?
- A. Thanh điệu mang nghĩa từ vựng — đổi thanh là đổi từ (ma/má/mà/mã/mạ); bỏ thanh → sai nghĩa, nên phải mã hoá vào đơn vị âm (tonophone)
- B. Thanh điệu chỉ ảnh hưởng cảm xúc, bỏ đi vẫn đúng nghĩa
- C. Thanh điệu tự sinh ra đúng từ ngữ cảnh nên không cần mô hình hoá
- D. Thanh điệu chỉ là đặc trưng của chữ viết, không có trong âm thanh

<details><summary>Đáp án</summary>

**A.** Tiếng Việt là ngôn ngữ **thanh điệu**: F0 contour phân biệt **nghĩa từ vựng** (6 thanh Hà Nội). TTS phải mô hình hoá thanh (gắn vào rhyme qua **tonophone** — xem [C-Câu11](C-am-vi-tieng-viet.md)), không thể coi là phụ trợ. B, C, D đều phủ nhận vai trò ngữ nghĩa của thanh.
</details>