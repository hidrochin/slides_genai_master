# TRẮC NGHIỆM — Cụm B: Biểu diễn Đơn thể thức (18 câu)
Nguồn: `lecture2.1-UnimodalRepresentations-Part1`, `Lecture2_2_unimodal_path2`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — mọi lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem phần **mổ xẻ từng phương án**. Câu **(Khó)** cần tính toán/phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Cùng con mèo dưới ánh sáng/góc khác nhau cho vector pixel rất xa nhau; hai vật khác loài cùng tư thế lại cho vector gần nhau. Hệ quả cho học biểu diễn:
- A. Cần tăng độ phân giải ảnh để hai vector của cùng vật gần lại với nhau
- B. Khoảng cách pixel không phản ánh ngữ nghĩa, nên cần học bất biến
- C. Chỉ cần chuẩn hóa pixel về [0,1] là khoảng cách trở nên có nghĩa
- D. Nên chuyển ảnh sang ảnh xám để giảm số chiều trước khi đem so sánh

<details><summary>Đáp án</summary>

**Đúng: B.** Đây là **pixel distance ≠ semantic similarity** → cần bất biến (augmentation, conv+pooling, attention).
- **A sai:** tăng độ phân giải không làm cùng vật dưới ánh sáng khác gần lại về pixel.
- **C sai:** chuẩn hóa biên độ không xử lý biến thiên góc/nền/ánh sáng.
- **D sai:** bỏ màu mất thông tin, không giải quyết lệch ngữ nghĩa.
</details>

---

**Câu 2.** Dịch ảnh sang phải: feature map của convolution dịch theo, nhưng sau max-pooling điểm số lớp gần như không đổi. Cặp tính chất là:
- A. Invariance ở convolution và equivariance ở tầng pooling phía sau
- B. Equivariance ở convolution và invariance ở tầng pooling phía sau
- C. Cả hai đều là equivariance, chỉ khác nhau về mức độ mạnh yếu
- D. Cả hai đều là invariance, đều nhờ cơ chế chia sẻ trọng số kernel

<details><summary>Đáp án</summary>

**Đúng: B.** Convolution **equivariant** (dịch input → dịch feature map); pooling tạo **invariance** (điểm số ít đổi khi dịch nhỏ).
- **A sai:** đảo ngược hai tính chất.
- **C sai:** pooling *không* equivariant — nó cố ý xóa vị trí.
- **D sai:** weight sharing tạo *equivariance*; invariance đến từ pooling.
</details>

---

**Câu 3. (Khó)** Ảnh cao H=32, kernel K=5, padding P=2, stride S=2, dilation D=1. Chiều cao đầu ra là:
- A. 14
- B. 15
- C. 16
- D. 32

<details><summary>Đáp án</summary>

**Đúng: C = 16.** `⌊(32 + 4 − 4 − 1)/2 + 1⌋ = ⌊15.5 + 1⌋ = 16`.
- **A sai:** quên số hạng "+1" cuối.
- **B sai:** làm tròn nhầm.
- **D sai:** 32 chỉ khi stride=1; ở đây stride=2 nên giảm đôi.
</details>

---

**Câu 4. (Khó) 🔗** FC học riêng trọng số cho từng vị trí pixel, còn convolution dùng chung kernel trượt. Ngoài ít tham số hơn, tính chất bản chất mà FC đánh mất còn conv giữ được là:
- A. Khả năng biểu diễn quan hệ phi tuyến giữa các pixel trong ảnh
- B. Tính bất biến tịnh tiến (cùng đặc trưng nhận ra ở mọi vị trí)
- C. Khả năng xử lý ảnh có nhiều kênh màu RGB cùng một lúc
- D. Khả năng tăng độ sâu mạng mà không gặp vanishing gradient

<details><summary>Đáp án</summary>

**Đúng: B.** FC học *khác nhau cho từng vị trí* nên không translation-invariant; conv chia sẻ kernel → nhận cùng đặc trưng mọi vị trí (liên hệ chiều "structure" ở [cụm A](A-tong-quan-6-thach-thuc.md)).
- **A sai:** phi tuyến đến từ hàm kích hoạt, cả hai đều có.
- **C sai:** FC cũng xử lý được nhiều kênh.
- **D sai:** chống vanishing là nhờ residual/ResNet.
</details>

---

**Câu 5.** Grad-CAM được ưa dùng hơn CAM trong nhiều tình huống. Lý do cốt lõi:
- A. Grad-CAM chỉ cần một phép nhân ma trận nên chạy nhanh hơn CAM
- B. CAM cho bản đồ mượt hơn còn Grad-CAM cho bản đồ sắc nét hơn
- C. Grad-CAM dùng gradient nên chạy được với kiến trúc bất kỳ
- D. CAM hoạt động với ViT còn Grad-CAM chỉ hoạt động với CNN

<details><summary>Đáp án</summary>

**Đúng: C.** CAM *đòi* GAP + linear; Grad-CAM lấy trọng số kênh từ gradient nên **kiến trúc-bất khả tri** (ResNet, VGG, ViT).
- **A sai:** tốc độ không phải lý do chính.
- **B sai:** độ mượt/sắc không phải điểm phân biệt bản chất.
- **D sai:** ngược — CAM mới bị giới hạn kiến trúc.
</details>

---

**Câu 6.** Sau khi randomize trọng số mô hình, bản đồ saliency của một phương pháp *đáng tin* (sanity check, Adebayo 2018) sẽ:
- A. Gần như không đổi, vì giải thích tốt phải ổn định trước nhiễu tham số mô hình
- B. Thay đổi mạnh, vì giải thích trung thực phải bám theo mô hình chứ không theo ảnh
- C. Luôn tập trung vào các cạnh và vùng có tương phản cao trong bức ảnh
- D. Trở nên trơn và đẹp hơn, phản ánh rõ cấu trúc nổi bật của bức ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** Mô hình "rác" thì giải thích *bám mô hình* phải đổi mạnh. Nếu không đổi → nó phản ánh **ảnh**, không phải mô hình ("pretty ≠ faithful").
- **A sai:** "ổn định trước nhiễu tham số" chính là dấu hiệu *không* faithful.
- **C, D sai:** bám cạnh/độ tương phản của ảnh là biểu hiện *không* faithful.
</details>

---

**Câu 7.** DeepSets mã hóa tập bằng `ρ(Σᵢ φ(xᵢ))`. Yếu tố *thực sự* tạo bất biến hoán vị là:
- A. Phép gộp giao hoán (sum/mean) trên các phần tử
- B. Bộ mã hóa phần tử φ được chia sẻ giữa mọi phần tử trong tập
- C. Bộ dự đoán ρ đặc thù cho tác vụ đặt ở cuối pipeline
- D. Việc sắp xếp phần tử theo một thứ tự chuẩn trước khi mã hóa

<details><summary>Đáp án</summary>

**Đúng: A.** Tính bất biến đến từ **phép gộp giao hoán** (sum/mean cho cùng kết quả với mọi thứ tự).
- **B sai:** φ chia sẻ là *cần* nhưng chưa *đủ*.
- **C sai:** ρ xử lý *sau* khi gộp.
- **D sai:** trái tinh thần "tập không thứ tự".
</details>

---

**Câu 8.** "walkability" chưa từng thấy lúc train nhưng fastText vẫn dựng được vector hợp lý, Word2Vec/GloVe thì không. Khác biệt là:
- A. fastText tạo vector khác nhau cho mỗi lần từ xuất hiện trong ngữ cảnh
- B. fastText biểu diễn từ như tổng các n-gram ký tự, chia sẻ với từ đã biết
- C. fastText dùng ma trận đồng xuất hiện toàn cục thay cho cửa sổ cục bộ
- D. fastText bỏ qua bước tokenization nên hoàn toàn không gặp vấn đề OOV

<details><summary>Đáp án</summary>

**Đúng: B.** `v_word = v_whole + Σ v_ngram`; n-gram (wal, alk…) trùng từ đã biết → ghép được vector OOV.
- **A sai:** đó là *contextual* embedding (ELMo/BERT); fastText vẫn static.
- **C sai:** ma trận đồng xuất hiện toàn cục là của GloVe.
- **D sai:** fastText vẫn tokenize; mấu chốt là subword.
</details>

---

**Câu 9. (Khó)** Negative sampling lấy mẫu nhiễu theo `P(w) ∝ freq(w)^{3/4}`. Tác dụng của số mũ 3/4 (<1) là:
- A. Nâng tương đối từ hiếm, hạ từ siêu phổ biến như 'the', 'of'
- B. Làm phân phối lấy mẫu trở nên hoàn toàn đồng đều trên cả từ điển
- C. Giảm chi phí tính softmax từ O(V) xuống còn O(1) cho mỗi cặp từ
- D. Loại bỏ hoàn toàn mọi từ chức năng ra khỏi tập nhiễu được chọn

<details><summary>Đáp án</summary>

**Đúng: A.** Lũy thừa <1 nén khoảng cách tần suất → tránh 'the'/'of' chiếm hết mẫu nhiễu.
- **B sai:** không đồng đều tuyệt đối; từ phổ biến vẫn được lấy nhiều hơn.
- **C sai:** giảm chi phí là công của *ý tưởng* negative sampling nói chung.
- **D sai:** từ chức năng bị *giảm*, không *loại bỏ hoàn toàn*.
</details>

---

**Câu 10.** "dog bites man" và "man bites dog" cho cùng vector nếu trung bình embedding, nhưng RNN/attention phân biệt được. Điều này minh họa:
- A. Trung bình embedding giữ trật tự nên hai câu vốn đã có vector khác nhau
- B. Bag-of-words vứt bỏ trật tự, còn mô hình chuỗi/attention giữ cấu trúc kết hợp
- C. RNN và bag-of-words đều bất biến với hoán vị từ trong một câu bất kỳ
- D. Attention chỉ hoạt động được khi hai câu đầu vào có độ dài khác nhau

<details><summary>Đáp án</summary>

**Đúng: B.** Trung bình embedding = bag-of-words → mất thứ tự; RNN/attention giữ *cách kết hợp*.
- **A sai:** trung bình *không* giữ trật tự — đó là lý do hai câu trùng.
- **C sai:** RNN *không* bất biến hoán vị (nó nhạy thứ tự).
- **D sai:** attention phân biệt được bất kể độ dài.
</details>

---

**Câu 11. (Khó)** LSTM có `∂c_t/∂c_{t−1} = f_t`. Vì sao điều này chống vanishing gradient trên chuỗi dài?
- A. Vì f_t luôn bằng 0 nên gradient bị chặn không cho bùng nổ ra vô hạn
- B. Vì gradient qua cell state chỉ nhân f_t (≈1 khi cần nhớ), không qua W hay tanh lặp
- C. Vì cell state được khởi tạo lại về 0 ở đầu mỗi bước thời gian mới
- D. Vì output gate luôn bằng 1 nên hidden state truyền thẳng gradient về sau

<details><summary>Đáp án</summary>

**Đúng: B.** Đường cell state chỉ nhân `f_t`; khi cần nhớ `f_t≈1` → gradient chảy gần nguyên vẹn, không bị squash bởi tanh/nhân ma trận W lặp ("gradient highway").
- **A sai:** `f_t=0` sẽ *xóa* nhớ và triệt tiêu gradient; mấu chốt là `f_t≈1`.
- **C sai:** cell state không reset về 0.
- **D sai:** output gate điều khiển hidden lộ ra, không phải cơ chế chống vanishing.
</details>

---

**Câu 12.** So sánh GRU và LSTM, phát biểu đúng cả về cấu trúc lẫn hệ quả:
- A. GRU có 3 cổng và 2 state nên nhiều tham số hơn nhưng luôn chính xác hơn LSTM
- B. LSTM có 3 cổng + cell state; GRU có 2 cổng, gộp cell vào hidden, ít tham số hơn, hiệu năng tương đương
- C. GRU luôn vượt LSTM trên mọi tác vụ nhờ có kiến trúc đơn giản gọn nhẹ hơn
- D. Cả GRU và LSTM đều không giải quyết được vanishing gradient của RNN thường

<details><summary>Đáp án</summary>

**Đúng: B.** LSTM: 3 cổng + cell state (nhiều tham số). GRU: 2 cổng, gộp cell vào hidden, ~25% ít tham số, hiệu năng thường tương đương.
- **A sai:** đảo số cổng/state; không có kết luận "luôn chính xác hơn".
- **C sai:** GRU *không* luôn thắng.
- **D sai:** cả hai *đều* giải vanishing.
</details>

---

**Câu 13.** Attention (Bahdanau) được đưa vào seq2seq chủ yếu để khắc phục:
- A. Việc nén cả câu nguồn vào một context vector cố định duy nhất
- B. Hiện tượng vanishing gradient bên trong cell state của mạng LSTM
- C. Chi phí softmax O(V) khi huấn luyện word embedding từ điển lớn
- D. Việc ảnh đầu vào có nhiều kênh màu cần được hợp nhất lại một

<details><summary>Đáp án</summary>

**Đúng: A.** Encoder-decoder cổ điển nén cả câu vào một vector cuối → nghẽn với câu dài; attention tính context mới mỗi bước decoder.
- **B sai:** vanishing của cell state đã được LSTM/GRU xử lý.
- **C sai:** đó là bối cảnh negative sampling.
- **D sai:** không liên quan kênh màu ảnh.
</details>

---

**Câu 14. (Khó)** Mô hình ngôn ngữ có average NLL `L = 2.30` (cơ số e). Perplexity xấp xỉ và diễn giải:
- A. 2.30 — mô hình gần như chắc chắn về từ tiếp theo trong câu
- B. 5.0 — mô hình lưỡng lự giữa khoảng năm lựa chọn khả dĩ
- C. 10.0 — mô hình mơ hồ như chọn giữa ~10 từ đồng khả năng
- D. 100.0 — mô hình gần như đoán ngẫu nhiên trên cả từ điển lớn

<details><summary>Đáp án</summary>

**Đúng: C.** `PPL = e^{2.30} ≈ 10` → mơ hồ như chọn giữa ~10 từ đồng khả năng.
- **A sai:** nhầm PPL bằng chính L.
- **B sai:** `e^{2.30}≈10`, không phải 5.
- **D sai:** nhầm `e^{2.30}` với 100.
</details>

---

**Câu 15.** Hoán vị thứ tự node được viết `A' = P A Pᵀ`. Mô hình đồ thị tốt nên:
- A. Nhạy cảm với hoán vị, để phân biệt các cách đánh số node khác nhau
- B. Bất biến/đẳng biến với hoán vị, vì đánh số lại node không đổi ý nghĩa
- C. Chỉ hoạt động khi ma trận kề đối xứng và đồ thị không có self-loop
- D. Bất biến với hoán vị chỉ khi tổng số node nhỏ hơn tổng số cạnh

<details><summary>Đáp án</summary>

**Đúng: B.** Đánh số lại node không đổi đồ thị → cần **bất biến/đẳng biến hoán vị** (message passing với aggregation giao hoán).
- **A sai:** nhạy hoán vị = gán ý nghĩa cho thứ tự tùy tiện.
- **C, D sai:** bất biến hoán vị không phụ thuộc đối xứng/self-loop hay số node–cạnh.
</details>

---

**Câu 16.** Static embedding gán một vector cho mỗi *loại* từ nên "bank" trong "river bank" và "money bank" dùng chung vector. Cách khắc phục đa nghĩa:
- A. Tăng số chiều embedding để mỗi nghĩa của từ chiếm một vùng riêng biệt
- B. Dùng embedding ngữ cảnh (ELMo/BERT), mỗi lần xuất hiện một vector riêng
- C. Thêm nhiều n-gram ký tự như fastText để tự phân tách các nghĩa của từ
- D. Chuẩn hóa mọi vector về độ dài đơn vị 1 trước khi đem ra tra cứu

<details><summary>Đáp án</summary>

**Đúng: B.** Đa nghĩa cần **contextual embedding** (ELMo/BERT) — mỗi token trong ngữ cảnh một vector khác.
- **A sai:** tăng chiều vẫn là *một* vector cho *một* loại từ.
- **C sai:** fastText giải OOV/morphology, vẫn static.
- **D sai:** chuẩn hóa độ dài không tạo nghĩa theo ngữ cảnh.
</details>

---

**Câu 17. 🔗** Sự kiện "bàn thắng" quan sát qua video (lưới 2D+thời gian), text (chuỗi), tiếng ồn (thời gian–tần số); mỗi modality cần họ mô hình khác nhau. Điều này phản ánh:
- A. Các modality này về bản chất là đồng nhất nên có thể dùng chung một mô hình
- B. Khác biệt về cấu trúc/inductive bias giữa modality quy định lựa chọn kiến trúc
- C. Chỉ cần một mô hình vạn năng duy nhất vì mọi modality đều là chuỗi token
- D. Video luôn cần nhiều tham số nhất nên phải dùng mô hình lớn nhất cho cả ba

<details><summary>Đáp án</summary>

**Đúng: B.** Đây là **heterogeneity** ([cụm A](A-tong-quan-6-thach-thuc.md)): mỗi modality có cấu trúc/bias riêng → **modality profile** quy định kiến trúc.
- **A sai:** chúng *dị thể*, không đồng nhất.
- **C sai:** "mọi thứ là token" là giả định đơn giản hóa (điểm yếu của mô hình unified — [cụm H](H-transference.md)).
- **D sai:** kích thước mô hình không phải tiêu chí chọn theo modality.
</details>

---

**Câu 18.** Tree-LSTM (kết hợp theo cây cú pháp) có ưu thế gì so với RNN tuần tự khi mô hình hóa câu?
- A. Không cần cây parse nên hoàn toàn tránh được lỗi từ bộ phân tích cú pháp
- B. Cho hai từ liên quan ở xa kết hợp qua đường ngắn hơn trên cây cú pháp
- C. Luôn nhanh hơn RNN tuần tự vì xử lý được mọi node hoàn toàn song song
- D. Loại bỏ hoàn toàn nhu cầu về các cổng (gate) nhờ vào cấu trúc dạng cây

<details><summary>Đáp án</summary>

**Đúng: B.** Trên cây, từ liên quan kết hợp qua **đường ngắn hơn** → gradient path ngắn, mô hình quan hệ xa tốt hơn.
- **A sai:** Tree-LSTM *cần* cây parse; lỗi parser lan truyền (nhược điểm).
- **C sai:** không hẳn nhanh hơn; khó song song theo batch.
- **D sai:** Tree-LSTM *vẫn* dùng cổng (forget riêng cho mỗi con).
</details>
