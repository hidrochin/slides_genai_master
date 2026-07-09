# B — Ngữ âm học: Cấu âm & Âm học (Articulatory + Acoustic Phonetics)

> Nguồn: `01 - Articulatory Phonetics`, `02 - Linguistics and Phonetics`, `02 - Acoustic Phonetics`. Cụm rất dày khái niệm — phân loại phụ âm/nguyên âm, sóng âm, F0/formant/spectrogram.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [A-tổng-quan](A-tong-quan.md) · [C-tiếng-Việt](C-am-vi-tieng-viet.md) · [D-DSP](D-xu-ly-tin-hieu.md)

---

## 1. Phonology vs. Phonetics (Âm vị học vs. Ngữ âm học) — DỄ NHẦM

| | **Phonology (Âm vị học)** | **Phonetics (Ngữ âm học)** |
|---|---|---|
| Đối tượng | Hệ thống âm của **một ngôn ngữ**; âm *hoạt động* thế nào | Sản sinh & tri giác **vật lý** của âm |
| Bản chất | **Trừu tượng**, biểu diễn tinh thần (mental) | **Cụ thể**, thuộc tính acoustic & articulatory thực |
| Phạm vi | Quy tắc **đặc thù ngôn ngữ** (language-specific) | Thuộc tính **phổ quát (universal)** của âm, không theo luật riêng ngôn ngữ |

**Tại sao vẫn cần?** DL hiện đại ít phụ thuộc mã hoá ngữ âm tay, NHƯNG hiểu ngữ âm giúp **mô tả & debug** hệ (VD giọng/thanh điệu đổi cách phát âm ra sao). Phân loại ngữ âm **không tuỳ tiện** — nó mô hình hoá **sinh học cách con người tạo âm**.

## 2. Phonetics có 3 nhánh — HAY RA THI

- **Articulatory Phonetics** — âm được **tạo ra (produced)** thế nào.
- **Acoustic Phonetics** — thuộc tính **vật lý** của âm.
- **Auditory Phonetics** — âm được **tri giác (perceived)** bởi người nghe thế nào.

Định nghĩa Phonetics: *nghiên cứu speech sounds — production, transmission, perception*. VD kinh điển: khác biệt /b/ và /p/.

## 3. Grapheme vs. Phoneme, IPA

- **Grapheme (tự vị):** đơn vị **viết** nhỏ nhất biểu diễn một âm. VD: "d", "th", "ngh", "a", "au".
- **Phoneme (âm vị):** đơn vị **âm thanh** nhỏ nhất. VD: /d/, /θ/, /ŋ/, /a/, /ăw/.
- **IPA (International Phonetic Alphabet):** bảng ký hiệu chuẩn 1 ký hiệu ↔ 1 âm. VD: leave /liːv/, manly /ˈmænli/.
- **Letter ≠ Sound:** 1 chữ có thể nhiều âm và ngược lại → lý do cần IPA.

## 4. Cơ chế tạo tiếng nói (Speech Production)

**Luồng hơi:** thường nói khi **thở ra** → *Pulmonic egressive airstream* (luồng khí từ phổi).
1. **Hít vào & chuẩn bị khí:** phổi + cơ hoành (diaphragm) điều chỉnh luồng khí.
2. **Đẩy khí qua thanh quản:** **dây thanh (vocal folds) rung** → tạo âm thô (voicing).
3. **Resonance (cộng hưởng):** hình dạng **vocal tract** tạo **harmonics**.
4. **Articulation (cấu âm):** điều chỉnh luồng khí bằng lưỡi, môi, răng, hàm.

**Hai đường (tract):**
- **Oral tract (đường miệng):** uvula (lưỡi gà), soft palate/velum (vòm mềm), hard palate (vòm cứng), tongue, lips, teeth.
- **Nasal tract (đường mũi).**

## 5. Phân loại PHỤ ÂM (Consonants) — 3 chiều: Place, Manner, Voicing

### 5.1 Place of Articulation (Vị trí cấu âm)
Phụ âm phân loại theo **nơi luồng khí bị co thắt (constricted) nhất**:
- **Labial** — dùng môi (lips).
- **Coronal** — dùng đầu/lưỡi (tip or blade of tongue).
- **Dorsal** — dùng thân sau lưỡi (back of tongue).

### 5.2 Manner of Articulation (Phương thức cấu âm) — DỄ RA BẢNG GHÉP
| Manner | Bản chất | Ví dụ |
|---|---|---|
| **Stop / Âm tắc** | Đóng hoàn toàn articulators, không cho khí thoát qua miệng | — |
| **Oral stop / Âm tắc miệng** | Vòm nâng, khí KHÔNG qua mũi; áp suất dồn rồi **bật** khi mở | p, t, k, b, d, g |
| **Nasal stop / Âm tắc mũi** | Đóng miệng nhưng **vòm hạ**, khí thoát qua **mũi** | m, n, ng |
| **Fricative / Âm xát** | Hai articulators gần nhau → khí xoáy (turbulent), tiếng "xì" | f, v, s, z, th, dh |
| **Approximant / Âm xấp** | Gần nhưng không đủ để tạo xoáy → không turbulence | y, r |
| **Lateral approximant / Âm xấp bên** | Cản luồng ở giữa, khí thoát **hai bên lưỡi** | l |

### 5.3 Voicing (Thanh tính) — CÓ/KHÔNG rung dây thanh
- **Voiced (hữu thanh):** dây thanh **rung**. VD: /b/ (bat), /d/ (dog), /z/ (zoo), /v/ (van).
- **Unvoiced/Voiceless (vô thanh):** dây thanh **KHÔNG rung**, âm chỉ do luồng khí + tiếp xúc articulators. VD: /p/ (pen), /t/ (top), /s/ (snake), /f/ (fish).
- Nhớ cặp đối: /b/–/p/, /d/–/t/, /z/–/s/, /v/–/f/ (cùng place & manner, khác voicing).

## 6. Phân loại NGUYÊN ÂM (Vowels) — 2 chiều chính

### 6.1 Tongue Height (Độ cao lưỡi)
- **High:** lưỡi gần vòm miệng — /i/ (see), /u/ (blue).
- **Mid:** giữa — /e/ (bed), /o/ (go).
- **Low:** lưỡi hạ thấp — /æ/ (cat), /ɑ/ (father).

### 6.2 Tongue Backness (Độ trước/sau lưỡi)
- **Front:** /i/ (see), /e/ (bed).
- **Central:** /ə/ (about), /ʌ/ (cup).
- **Back:** /u/ (blue), /o/ (go).

(Thêm chiều **lip rounding** — tròn môi; dùng vowel grid/quadrilateral để định vị.)

## 7. ÂM HỌC (Acoustic Phonetics)

### 7.1 Sóng âm
- **Sóng âm là sóng dọc (longitudinal wave):** hạt môi trường dao động **song song** hướng lan truyền (giống P-wave, pressure wave).
- Mô tả bằng: **wavelength (bước sóng), frequency (tần số), amplitude (biên độ), speed**.

### 7.2 Fundamental Frequency (F0) & Harmonics — QUAN TRỌNG
- **F0 (tần số cơ bản):** tần số **thấp nhất** của sóng phức — chính là **tốc độ dao động của dây thanh** → quyết định **voicing/cao độ**. Mỗi đỉnh sóng ↔ một lần mở dây thanh.
- **Ví dụ tính F0:** nguyên âm /iy/ có **10 chu kỳ / 0.03875 s = 258 Hz**. ⇒ Công thức: **F0 = số chu kỳ / khoảng thời gian**.
- **Harmonic (hoạ âm):** sóng có tần số là **bội số nguyên** của F0. F0 = harmonic thứ 1 = f1; f2 = harmonic thứ 2 = 2×F0; …
- **Node:** điểm biên độ **cực tiểu** trên sóng dừng. **Antinode:** điểm biên độ **cực đại**.

### 7.3 Amplitude (Biên độ)
- Độ dịch chuyển **cực đại** của hạt khỏi vị trí cân bằng → liên quan **độ to (loudness/volume)**. Biên độ lớn ⇒ âm to hơn.
- Thang mức nghe (dB HL) — mức độ suy giảm thính lực: Normal −10..15, Slight 16..25, Mild 26..40, Moderate 41..55, Mod-Severe 56..70, Severe 71..90, Profound 90+.

### 7.4 Spectrogram (Ảnh phổ) & Formant — HAY HỎI
- **Spectrogram:** đồ thị hiển thị **cường độ tín hiệu theo thời gian** cho một **dải tần** cho trước = **Spectrum + trục Thời gian**.
- **Formant:** dải tần cộng hưởng đậm; nguyên âm nhận diện chủ yếu qua **F1 và F2**.
  - **Nguyên âm:** có **formant pattern đầy đủ** (dựa F1, F2).
  - **Phụ âm:** **không có formant pattern rõ** của riêng nó, mà **ảnh hưởng tới pattern của nguyên âm xung quanh**.

### 7.5 Công cụ phân tích tín hiệu
**Praat** (Boersma & Weenink, Amsterdam) · **Wavesurfer** (KTH Stockholm) · **Goldwave** (thương mại, bản dùng thử miễn phí). Thao tác điển hình: ghi âm trong Praat, tạo **TextGrid** với 2 tier để chú thích mức **word (grapheme)** và **phoneme (IPA)**.

## 8. Allophone (Tha âm) — [ ]

- **Allophone = biến thể của một phoneme.** Tập allophone của một phoneme là các âm mà:
  - **Không** làm đổi nghĩa từ.
  - Rất **giống nhau**.
  - Xuất hiện ở **ngữ cảnh ngữ âm khác nhau** (VD đầu âm tiết vs. cuối âm tiết).
- Khác biệt giữa allophone diễn đạt bằng **luật âm vị học (phonological rules)**.
- Ký hiệu: phoneme dùng `/ /`, allophone dùng `[ ]`. (Ứng dụng tiếng Việt → xem [C-tiếng-Việt](C-am-vi-tieng-viet.md).)

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. Lý thuyết Nguồn–Lọc (Source–Filter Theory, Fant 1960) — nền tảng của mọi thứ
Tiếng nói = **nguồn** (glottal source) ⊛ **lọc** (vocal tract) ⊛ **bức xạ môi** (lip radiation). Trong miền phổ (nhân thành cộng log):
```
log|Speech(f)| = log|Source(f)| + log|Filter(f)| + log|Radiation(f)|
```
- **Nguồn (thanh môn):** chuỗi xung tuần hoàn → phổ vạch tại **bội số F0** (fine structure), dốc **≈ −12 dB/octave**.
- **Lọc (vocal tract):** cộng hưởng → **formant** (spectral envelope), độc lập tương đối với F0.
- **Hệ quả then chốt:** **F0 (nguồn) và formant (lọc) TÁCH RỜI** → cùng một nguyên âm có thể nói ở nhiều cao độ (đổi F0) mà formant giữ nguyên. Đây là lý do nam/nữ/trẻ em nói "cùng nguyên âm" nghe khác pitch nhưng nhận diện được.

### N2. Vocal tract như ống cộng hưởng — tính formant
- Xấp xỉ vocal tract (dài `L ≈ 17.5 cm` ở nam) là **ống đều đóng một đầu** (thanh môn) hở một đầu (môi): cộng hưởng ở
```
Fₙ = (2n − 1)·c / (4L),  c ≈ 340 m/s
```
→ F1 ≈ 340/(4×0.175) ≈ **500 Hz**, F2 ≈ 1500 Hz, F3 ≈ 2500 Hz (nguyên âm trung tính schwa). Nữ/trẻ em L ngắn hơn → formant **cao hơn** (đây là lý do phải normalize formant theo speaker).
- **Perturbation theory:** thu hẹp ống ở điểm áp suất cao → hạ formant; ở điểm vận tốc cao → nâng formant. Giải thích **F1↔height, F2↔backness** (đã nêu ở [B-Câu18](../trac_nghiem/B-ngu-am-hoc.md)).

### N3. Đo lường thực tế (cách Praat làm)
- **F0:** **autocorrelation** hoặc **cepstrum** — cepstrum = `IDFT(log|DFT(x)|)`; đỉnh ở **quefrency = 1/F0** tách nguồn (tuần hoàn) khỏi lọc (envelope trơn ở quefrency thấp). Đây là gốc chung với **cepstrum của MFCC** ([D §N5](D-xu-ly-tin-hieu.md)).
- **Formant:** **LPC (Linear Predictive Coding)** — mô hình all-pole `H(z)=1/A(z)`; nghiệm của `A(z)` cho tần số & bandwidth formant. LPC chính là hiện thân số của source-filter (all-pole ≈ ống cộng hưởng không mất mát).

### N4. Tri giác & tương phản (Auditory Phonetics định lượng)
- **Categorical perception:** dọc continuum VOT (VD /ba/–/pa/), người nghe **phân loại rời rạc** quanh ranh giới ~25–30 ms, không nghe được biến thiên bên trong một loại.
- **VOT** (Voice Onset Time): thời gian nhả–voicing; tiếng Anh /p,t,k/ có VOT dài (aspirated), /b,d,g/ ngắn/âm. Là **cue acoustic chính** cho tương phản voicing ở âm tắc.
- **Critical bands / ERB:** tai phân giải tần theo băng tới hạn (cơ sở sinh học của **thang Mel/Bark**).

### N5. Coarticulation & bất biến — vì sao ASR khó
- **Coarticulation:** âm bị "nhoè" bởi âm lân cận (VD /d/ trong "dee" vs "doo" có burst khác nhau) → **không có bất biến acoustic 1-1 cho phoneme** (lack of invariance problem).
- **Locus theory:** transition của F2 hướng về một "locus" đặc trưng cho place of articulation → dùng để đọc phụ âm trên spectrogram (phụ âm không có formant riêng, chỉ để lại **transition** trên nguyên âm lân cận — nối [§7.4]).
- Hệ quả kỹ thuật: đây chính là lý do ASR cần **mô hình phụ thuộc ngữ cảnh** (triphone ở HMM, receptive field rộng ở Transformer) thay vì phân loại từng frame độc lập.
