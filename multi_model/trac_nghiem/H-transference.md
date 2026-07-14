# TRẮC NGHIỆM — Cụm H: Chuyển giao (Transference) (16 câu)
Nguồn: `Lecture11.2-Transference`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Hệ nhận diện tiếng nói ít tài nguyên được cải thiện nhờ tri thức từ mô hình ngôn ngữ lớn. Nhiệm vụ này thuộc:
- A. Representation, vì nó học một biểu diễn chung dùng chung cho cả hai modality
- B. Transference, vì tri thức được chuyển sang giúp modality chính ít tài nguyên
- C. Generation, vì mô hình phải sinh ra dữ liệu tiếng nói hoàn toàn mới để bổ sung
- D. Alignment, vì nó căn chỉnh tín hiệu âm thanh với văn bản dựa theo trục thời gian

<details><summary>Đáp án</summary>

**Đúng: B.** Chuyển tri thức để **giúp modality chính ít tài nguyên** = **Transference**.
- **A sai:** tuy có biểu diễn chung, mục tiêu là *chuyển tri thức không cân xứng*.
- **C sai:** không có bước sinh dữ liệu tiếng nói mới.
- **D sai:** không phải căn chỉnh phần tử theo thời gian.
</details>

---

**Câu 2.** Ba sub-challenge của Transference là:
- A. Transfer (dùng pretrained), Co-learning (chia sẻ biểu diễn), Model Induction
- B. Fusion, Coordination, và Fission như các sub-challenge của Representation
- C. Summarization, Translation, và Creation như sub-challenge của Generation
- D. Heterogeneity, Interactions, và Learning như sub-challenge của Quantification

<details><summary>Đáp án</summary>

**Đúng: A.** Transfer, Co-learning, Model Induction.
- **B sai:** đó là Representation.
- **C sai:** đó là Generation.
- **D sai:** đó là Quantification.
</details>

---

**Câu 3.** Đặc điểm phân biệt của Co-learning là:
- A. Cả hai modality đều bắt buộc phải có mặt lúc test thì mới dự đoán được kết quả
- B. Modality phụ chỉ có mặt lúc train; lúc test chỉ cần dùng modality chính là đủ
- C. Không cần bất kỳ dữ liệu ghép cặp nào giữa hai modality trong lúc huấn luyện
- D. Các mô hình đơn thể thức được giữ hoàn toàn tách biệt riêng rẽ với nhau về sau

<details><summary>Đáp án</summary>

**Đúng: B.** Modality phụ **chỉ có lúc train**; test chỉ dùng modality chính.
- **A sai:** ngược — test không cần modality phụ.
- **C sai:** co-learning thường *cần* ghép cặp lúc train.
- **D sai:** đó là Model Induction.
</details>

---

**Câu 4.** Trong zero-shot visual classification của Socher (2013), lúc test mô hình dùng gì?
- A. Chỉ text (word embedding), để phân loại các nhãn văn bản cho từng bức ảnh
- B. Chỉ ảnh, nhờ không gian word embedding đã căn chỉnh sẵn từ lúc huấn luyện
- C. Cả ảnh và cả text cùng một lúc, để nâng cao độ chính xác của việc phân loại
- D. Chỉ audio, để có thể nhận dạng ra âm thanh tương ứng với đối tượng trong ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** **Test chỉ dùng ảnh**, nhờ không gian word embedding đã căn chỉnh → phân loại zero-shot (coordination từ [cụm C](C-fusion-coordination-fission.md)).
- **A sai:** test dùng *ảnh*.
- **C sai:** test *chỉ* dùng ảnh.
- **D sai:** không liên quan audio.
</details>

---

**Câu 5.** Co-learning via representation khác co-learning via generation ở cơ chế:
- A. Via representation dùng modality phụ làm mục tiêu sinh; via generation chia sẻ biểu diễn
- B. Via representation chia sẻ/căn chỉnh không gian biểu diễn; via generation dùng làm target sinh
- C. Via representation cần cả hai modality lúc test; còn via generation thì lại không cần
- D. Hai cơ chế này hoàn toàn giống hệt nhau, chỉ khác nhau về mặt tên gọi mà thôi

<details><summary>Đáp án</summary>

**Đúng: B.** Via representation = **chia sẻ/căn chỉnh không gian**; via generation = dùng modality phụ làm **generation target**.
- **A sai:** đảo ngược.
- **C sai:** cả hai đều test bằng một modality.
- **D sai:** chúng khác nhau về cơ chế.
</details>

---

**Câu 6.** "Found in Translation" (Pham 2019) dùng cyclic translation để:
- A. Bắt buộc cả hai modality phải có mặt lúc test nhằm nâng cao độ chính xác dự đoán
- B. Lúc test chỉ cần text, đồng thời robust với visual thiếu/nhiễu (dịch chéo lúc train)
- C. Sinh ra được các bức ảnh có độ phân giải cao từ một đoạn mô tả bằng văn bản
- D. Tăng số modality của bài toán từ hai lên thành ba để mô hình học được nhiều hơn

<details><summary>Đáp án</summary>

**Đúng: B.** Cyclic translation lúc train → **test chỉ cần text**, robust với visual thiếu/nhiễu.
- **A sai:** mục tiêu là *chỉ cần text* lúc test.
- **C sai:** không nhằm sinh ảnh chất lượng cao.
- **D sai:** không tăng số modality.
</details>

---

**Câu 7.** Vokenization (Tan & Bansal 2020) cải thiện hiểu ngôn ngữ bằng cách:
- A. Chỉ dùng masked language modeling thuần text, không hề dùng đến tín hiệu thị giác
- B. Dự đoán ảnh (voken) tương ứng với ngôn ngữ, kèm MLM; nhưng test chỉ dùng text
- C. Sinh ra video từ văn bản đầu vào để tăng cường thêm dữ liệu cho việc huấn luyện
- D. Dùng optimal transport để căn chỉnh các word với các region tương ứng trong ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** Gán mỗi token một "voken" và **dự đoán ảnh tương ứng** kèm MLM; **test chỉ dùng text**.
- **A sai:** điểm nhấn là *thêm giám sát thị giác*.
- **C sai:** không sinh video.
- **D sai:** OT căn word–region là ViLT/UNITER.
</details>

---

**Câu 8.** Phát biểu nào đúng về giới hạn của co-learning (Yun 2021)?
- A. Vision-language pretraining luôn cải thiện mạnh mẽ trên tất cả tác vụ ngôn ngữ
- B. Vision-language pretraining cải thiện rất ít trên lexical grounding / semantic role labeling
- C. Co-learning chỉ hoạt động được khi lúc test ta dùng đồng thời cả hai modality
- D. Co-learning không bao giờ mang lại được bất kỳ sự cải thiện nào cho mô hình cả

<details><summary>Đáp án</summary>

**Đúng: B.** Co-learning cải thiện **rất ít (marginal)** trên lexical grounding, SRL, physical commonsense QA.
- **A sai:** ngược với phát hiện.
- **C sai:** co-learning test bằng một modality.
- **D sai:** quá tuyệt đối — nó *có* cải thiện ở một số tác vụ.
</details>

---

**Câu 9.** Định nghĩa Model Induction (sub-challenge 5c) là:
- A. Gộp các mô hình đơn thể thức lại thành một mô hình thống nhất duy nhất về sau
- B. Giữ các mô hình đơn thể thức riêng biệt nhưng cảm ứng hành vi chung giữa chúng
- C. Chuyển các tham số đã pretrained sang một tác vụ downstream hoàn toàn mới khác
- D. Sinh ra dữ liệu cho modality bị thiếu trong lúc huấn luyện mô hình đa thể thức

<details><summary>Đáp án</summary>

**Đúng: B.** Giữ model đơn thể thức **riêng biệt**, **cảm ứng hành vi chung** (co-training, co-regularization).
- **A sai:** không gộp thành một model.
- **C sai:** đó là Transfer via pretrained.
- **D sai:** đó là hướng robustness.
</details>

---

**Câu 10. (Khó)** Giả định "multi-view redundancy" nền tảng cho model induction được viết là:
- A. `I(X1; X2) = ∞`
- B. `X1 ⊥ X2 | Y`, tức `I(X1; X2 | Y) = 0`
- C. `H(X1) = H(X2)`
- D. `p(X1) = p(X2)`

<details><summary>Đáp án</summary>

**Đúng: B.** Hai view **độc lập có điều kiện** cho nhãn, cộng **sufficiency**.
- **A sai:** không phải chia sẻ vô hạn thông tin.
- **C, D sai:** entropy bằng nhau / cùng phân phối biên không phải điều kiện co-training.
</details>

---

**Câu 11.** Khác biệt cơ bản giữa self-training và co-training về số view là:
- A. Self-training dùng 2 view; còn co-training thì chỉ dùng có 1 view mà thôi
- B. Self-training 1 view (tự pseudo-label); co-training 2 view, pseudo-label chéo cho nhau
- C. Cả hai đều chỉ dùng dữ liệu có nhãn và không hề dùng đến dữ liệu không nhãn
- D. Co-training không cần bất kỳ dữ liệu có nhãn nào để có thể khởi động được

<details><summary>Đáp án</summary>

**Đúng: B.** Self-training: **1 view** (tự pseudo-label). Co-training: **2 view**, pseudo-label chéo.
- **A sai:** đảo ngược số view.
- **C sai:** cả hai *đều* dùng dữ liệu không nhãn.
- **D sai:** co-training *cần* ít dữ liệu có nhãn khởi động.
</details>

---

**Câu 12. (Khó)** Hai giả định cốt lõi của co-training (Blum & Mitchell 1998) là:
- A. Mỗi view đủ để dự đoán nhãn một mình; và hai view độc lập nhất có thể với nhau
- B. Hai view phải giống hệt nhau về nội dung; và không cần bất kỳ dữ liệu có nhãn nào
- C. Chỉ một view là đủ dự đoán nhãn, còn view còn lại thì hoàn toàn chỉ là nhiễu
- D. Hai view bắt buộc phải có cùng số chiều đặc trưng thì thuật toán mới hoạt động

<details><summary>Đáp án</summary>

**Đúng: A.** ① **Sufficiency** (mỗi view đủ dự đoán); ② **Independence** (hai view độc lập nhất có thể).
- **B sai:** hai view giống hệt thì không bổ sung được gì.
- **C sai:** *cả hai* view đều phải đủ.
- **D sai:** số chiều không phải giả định.
</details>

---

**Câu 13. 🔗** Co-regularization (Sridharan & Kakade 2008) thêm số hạng loss nào?
- A. `L = (f1(X1) − f2(X2))²`, nhắc lại ý tưởng representation coordination
- B. `L = −log p(y|x)`, chính là hàm cross-entropy tiêu chuẩn cho phân loại
- C. `L = KL(q‖p)`, chính là số hạng KL regularization ở trong ELBO của VAE
- D. `L = ‖X1 − X2‖`, đo trực tiếp khoảng cách giữa hai đầu vào thô của hai view

<details><summary>Đáp án</summary>

**Đúng: A.** `L=(f1(X1)−f2(X2))²` ép hai view đồng thuận → **representation coordination** ([cụm C](C-fusion-coordination-fission.md)).
- **B sai:** cross-entropy là loss phân loại chuẩn.
- **C sai:** KL/ELBO thuộc VAE.
- **D sai:** co-regularization so khớp *dự đoán*, không phải đầu vào thô.
</details>

---

**Câu 14. 🔗** Transfer via Pretrained Models coi "tri thức" được chuyển giao ở dạng nào?
- A. Dữ liệu huấn luyện thô của mô hình nguồn được đóng gói lại để dùng cho tác vụ mới
- B. Tham số mạng `θ*` của mô hình pretrained (VD BERT), adapt qua finetuning/prefix
- C. Nhãn của tập test đích, được suy ra sẵn từ mô hình nguồn để giúp mô hình đích
- D. Ma trận đồng xuất hiện của corpus nguồn, dùng để khởi tạo trọng số mô hình đích

<details><summary>Đáp án</summary>

**Đúng: B.** Tri thức = **tham số mạng `θ*`** (BERT…); adapt trùng với conditioning generative ([cụm G](G-generation.md)).
- **A sai:** chuyển *tham số*, không phải dữ liệu thô.
- **C sai:** nhãn test không phải thứ được chuyển.
- **D sai:** ma trận đồng xuất hiện là của GloVe.
</details>

---

**Câu 15.** Trong HighMMT/Gato, thành phần nào đưa các modality dị thể về dạng dùng chung được?
- A. Modality-specific embeddings → standardized input sequence chuẩn hóa đầu vào
- B. Optimal transport tính giữa mọi cặp modality để tìm ánh xạ tối ưu giữa chúng
- C. Một mô hình diffusion chung được dùng cho tất cả các modality đầu vào khác nhau
- D. Beam search thực hiện trên không gian các modality để chọn ra tổ hợp tốt nhất

<details><summary>Đáp án</summary>

**Đúng: A.** **Modality-specific embeddings** → **standardized input sequence** → shared model (cùng tham số).
- **B sai:** OT không phải cơ chế thống nhất modality ở đây.
- **C sai:** diffusion là mô hình sinh.
- **D sai:** beam search là giải mã chuỗi.
</details>

---

**Câu 16. (Khó) 🔗** Đâu là một giả định NGẦM (điểm yếu) của mô hình high-modality thống nhất kiểu Gato/HighMMT?
- A. Mọi modality có thể biểu diễn thành chuỗi mà không hề bị mất thông tin nào
- B. Mỗi modality bắt buộc phải có một mô hình riêng hoàn toàn tách biệt với nhau
- C. Không thể chia sẻ tham số giữa các tác vụ khác nhau trong cùng một mô hình
- D. Hệ thống chỉ có thể hoạt động được khi đầu vào có đúng chính xác hai modality

<details><summary>Đáp án</summary>

**Đúng: A.** Giả định ngầm: mọi modality **biểu diễn được thành chuỗi** không mất thông tin (+ heterogeneity bắt trọn bởi embeddings; interactions chia sẻ) — nối cảnh báo ở [cụm B](B-bieu-dien-don-the-thuc.md).
- **B, C sai:** trái với thiết kế "unified + parameter sharing" (là điều Gato *làm được*).
- **D sai:** high-modality xử lý *nhiều* modality.
</details>
