# TRẮC NGHIỆM — Cụm D: Alignment & Biểu diễn Căn chỉnh (18 câu)
Nguồn: `lecture4.1-MultimodalAlignment`, `lecture4.2-AlignedRepresentations`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần tính toán/phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Tác vụ "nối từng vùng ảnh với từng cụm từ trong caption, dựa trên cấu trúc cả hai" thuộc thách thức nào?
- A. Representation, vì mục tiêu là học một vector chung cho cả ảnh và caption
- B. Alignment, vì trọng tâm là nối các phần tử của hai modality theo cấu trúc
- C. Generation, vì mô hình phải sinh ra một caption hoàn toàn mới từ ảnh
- D. Transference, vì tri thức được chuyển từ modality ảnh sang modality ngôn ngữ

<details><summary>Đáp án</summary>

**Đúng: B.** Nối *phần tử ↔ phần tử* theo cấu trúc = **Alignment**.
- **A sai:** học một vector chung là Fusion.
- **C sai:** không có bước sinh caption mới.
- **D sai:** không có modality yếu được hỗ trợ.
</details>

---

**Câu 2.** Hard attention chọn một vùng rời rạc, soft attention lấy trung bình có trọng số mọi vùng. Hệ quả huấn luyện:
- A. Hard attention khả vi end-to-end; soft attention lại cần bước sampling
- B. Soft attention khả vi end-to-end; hard attention thường cần sampling (RL)
- C. Cả hai đều khả vi và được huấn luyện theo cùng một cách giống hệt nhau
- D. Cả hai đều cần reinforcement learning vì bản chất đều là lựa chọn rời rạc

<details><summary>Đáp án</summary>

**Đúng: B.** Soft **khả vi** (mặc định seq2seq/transformer); hard **không** khả vi → thường train bằng **sampling/RL**.
- **A sai:** đảo ngược tính khả vi.
- **C sai:** hai cơ chế train khác nhau.
- **D sai:** soft attention khả vi, không cần RL.
</details>

---

**Câu 3.** Hai tập phần tử **cùng kích thước**, cần ghép **1-1 cứng**, mọi phần tử đều được gán. Bài toán và cách giải:
- A. Optimal transport, giải bằng Wasserstein distance với ghép mềm many-to-many
- B. Assignment problem, giải bằng linear programming / thuật toán Hungarian
- C. Dynamic time warping, giải bằng quy hoạch động trên ma trận chi phí
- D. Contrastive learning, giải bằng InfoNCE trên các cặp có trong một batch

<details><summary>Đáp án</summary>

**Đúng: B.** Ghép **1-1 cứng**, tập bằng nhau = **assignment problem**; `x_ij∈{0,1}`, giải bằng **LP/Hungarian**.
- **A sai:** OT dành cho ghép mềm, tập khác kích thước.
- **C sai:** DTW căn tín hiệu thời gian, không phải ghép hai tập.
- **D sai:** contrastive dạy ranking, không giải bài toán ghép 1-1.
</details>

---

**Câu 4.** Khi hai tập phần tử **kích thước khác nhau** và cần ghép **mềm (many-to-many)**, ta dùng optimal transport. Đại lượng gắn với nghiệm tối ưu là:
- A. Hệ số tương quan Pearson
- B. Khoảng cách Wasserstein
- C. Độ đo perplexity
- D. Entropy có điều kiện

<details><summary>Đáp án</summary>

**Đúng: B.** OT (`x(i,j)≥0`) xử lý tập khác kích thước; nghiệm tối ưu liên hệ **Wasserstein distance**.
- **A sai:** Pearson là hàm coordination (cụm C).
- **C sai:** perplexity đo mô hình ngôn ngữ.
- **D sai:** entropy có điều kiện là khái niệm thông tin.
</details>

---

**Câu 5. (Khó)** Đâu KHÔNG phải một ràng buộc của Dynamic Time Warping?
- A. Monotonicity — đường căn chỉnh không đi lùi về quá khứ theo thời gian
- B. Boundary conditions — bắt đầu và kết thúc tại điểm đầu-cuối tương ứng
- C. Orthogonality — các phép chiếu căn chỉnh phải trực giao với nhau
- D. Continuity — đường căn chỉnh không có khoảng nhảy hoặc bỏ trống

<details><summary>Đáp án</summary>

**Đúng: C.** Ràng buộc DTW: monotonicity, continuity, boundary, warping window, slope. **Orthogonality** thuộc **CCA** — bẫy trộn hai chủ đề.
- **A, B, D** đều là ràng buộc *đúng* của DTW.
</details>

---

**Câu 6. 🔗** Canonical Time Warping (CTW) căn hai chuỗi có **không gian đặc trưng khác nhau** bằng cách kết hợp DTW với:
- A. CTC; trong đó `W` căn thời gian còn CTC gán nhãn phoneme cho mỗi frame
- B. CCA; trong đó `W_x, W_y` căn thời gian còn `U, V` căn chéo modality
- C. Optimal transport; cả hai phần cùng đảm nhận việc căn chỉnh không gian
- D. BERT; trong đó BERT sinh biểu diễn ngữ cảnh trước khi thực hiện warping

<details><summary>Đáp án</summary>

**Đúng: B.** CTW = **DTW + CCA** ([cụm C](C-fusion-coordination-fission.md)): `W` căn **thời gian**, `U,V` căn **chéo modality**.
- **A sai:** CTC là gán nhãn segmentation.
- **C sai:** CTW dựa trên DTW (căn thời gian), không phải OT.
- **D sai:** BERT không phải thành phần của CTW.
</details>

---

**Câu 7.** Token **blank (∅)** và quy tắc collapse (gộp trùng liên tiếp rồi bỏ blank) trong CTC giải quyết:
- A. Xác định vị trí bắt đầu và kết thúc câu trả lời trong tác vụ hỏi–đáp
- B. Căn many-to-1 (nhiều frame → một nhãn), không cần cắt đoạn trước
- C. Sinh pseudo-label bằng K-means clustering trên tập audio không nhãn
- D. Nối text token với image region thành một chuỗi chung cho transformer

<details><summary>Đáp án</summary>

**Đúng: B.** Blank hấp thụ khác biệt thời lượng, collapse gộp trùng → giải "nhiều frame → một nhãn" **không cần segmentation trước**.
- **A sai:** đó là fine-tuning QA của BERT.
- **C sai:** pseudo-label bằng clustering là HuBERT.
- **D sai:** nối chuỗi text–region là transformer one-stream (cụm E).
</details>

---

**Câu 8.** HuBERT khác CTC ở điểm cốt lõi nào?
- A. HuBERT là giám sát (supervised) còn CTC là tự giám sát (self-supervised)
- B. Target của HuBERT là pseudo-label từ clustering, không phải nhãn phoneme
- C. HuBERT không dùng transformer mà dùng mạng RNN để mã hóa audio
- D. HuBERT không dùng masking khi huấn luyện, chỉ dự đoán trực tiếp toàn bộ

<details><summary>Đáp án</summary>

**Đúng: B.** HuBERT **self-supervised**: clustering tạo *hidden units* làm target, mask spans rồi dự đoán — khác CTC (nhãn phoneme, supervised).
- **A sai:** đảo ngược — HuBERT mới là self-supervised.
- **C sai:** HuBERT *dùng* transformer.
- **D sai:** HuBERT *có* masking.
</details>

---

**Câu 9. 🔗** Local alignment (nối một vùng ảnh với một cụm từ) thực chất tái sử dụng kỹ thuật nào của cụm Representation?
- A. Tensor fusion, để gộp hai modality thành một vector chung duy nhất
- B. Coordinated representations / contrastive learning trên các cặp phần tử
- C. Fission, để tách phần chung và phần riêng của mỗi modality ra rõ ràng
- D. Modality-shift, để dịch biểu diễn ngôn ngữ bằng tín hiệu từ thị giác

<details><summary>Đáp án</summary>

**Đúng: B.** Local alignment = **coordinated representations/contrastive learning** trên *cặp phần tử* ([cụm C](C-fusion-coordination-fission.md)), cần paired data.
- **A sai:** tensor fusion tạo một vector chung.
- **C sai:** fission không nói về nối phần tử chéo.
- **D sai:** modality-shift là cơ chế fusion.
</details>

---

**Câu 10. 🔗** Self-attention là hoán vị-đẳng biến: xáo trộn token thì đầu ra chỉ hoán vị theo. Hệ quả thiết kế bắt buộc:
- A. Phải thêm position embedding để đưa thông tin vị trí vào đầu vào mô hình
- B. Phải dùng hàm softmax để chuẩn hóa các trọng số attention về tổng bằng 1
- C. Phải thay self-attention bằng convolution nếu muốn giữ được trật tự token
- D. Phải giảm số lượng head để tránh trùng lặp thông tin về vị trí giữa chúng

<details><summary>Đáp án</summary>

**Đúng: A.** Không mã hóa vị trí nội tại → **bắt buộc thêm position embedding** (liên hệ "dog bites man" ở [cụm B](B-bieu-dien-don-the-thuc.md)).
- **B sai:** softmax chuẩn hóa trọng số nhưng không đưa thông tin vị trí.
- **C sai:** không cần bỏ self-attention.
- **D sai:** số head không liên quan mã hóa vị trí.
</details>

---

**Câu 11.** Trong scaled dot-product attention, trọng số `α` giữa query i và các vị trí j được tính bằng:
- A. `softmax(q_i · k_j / √d)` — query nhân key, chia căn số chiều
- B. `softmax(q_i · v_j / √d)` — query nhân value, chia căn số chiều
- C. `‖q_i − k_j‖²` — bình phương khoảng cách giữa query và key
- D. `sigmoid(q_i + k_j)` — tổng của query và key rồi qua sigmoid

<details><summary>Đáp án</summary>

**Đúng: A.** `α = softmax(q_i·k_j/√d)`; rồi `h_i = Σ α_{ij} v_j`. Query nhân **Key** để tính trọng số; **Value** mới được tổng hợp.
- **B sai:** dùng nhầm Value ở bước tính trọng số.
- **C sai:** attention dùng tích vô hướng, không phải khoảng cách.
- **D sai:** không phải tổng qua sigmoid, và bỏ mất softmax.
</details>

---

**Câu 12.** Multi-head self-attention cho phép mô hình làm gì mà single-head không làm được?
- A. Giảm tổng số tham số so với một single-head cùng kích thước biểu diễn
- B. Chú ý đồng thời tới nhiều không gian con (subspace) khác nhau của biểu diễn
- C. Loại bỏ hoàn toàn nhu cầu về position embedding cho chuỗi đầu vào
- D. Thay thế cho residual connection ở bên trong mỗi khối transformer encoder

<details><summary>Đáp án</summary>

**Đúng: B.** Nhiều bộ `W_q,W_k,W_v` song song → mỗi head chú ý một **subspace** khác, rồi nối lại + linear.
- **A sai:** không nhằm giảm tham số.
- **C sai:** vẫn cần position embedding.
- **D sai:** residual tồn tại độc lập với multi-head.
</details>

---

**Câu 13.** Hai mục tiêu tiền huấn luyện tự giám sát của BERT là:
- A. CTC và optimal transport — căn chuỗi và ghép các phần tử với nhau
- B. Masked Language Model và Next Sentence Prediction — đoán token và quan hệ câu
- C. Contrastive InfoNCE và DTW — kéo gần cặp đúng và căn chỉnh theo thời gian
- D. Autoregressive next-token và beam search — sinh từng token một cách tuần tự

<details><summary>Đáp án</summary>

**Đúng: B.** **MLM** (che token → đoán, 2 chiều) + **NSP** (hai câu có kề nhau không).
- **A, C sai:** CTC/OT/InfoNCE/DTW không phải mục tiêu pretrain BERT.
- **D sai:** next-token autoregressive là kiểu GPT.
</details>

---

**Câu 14.** Trong NSP và phân loại câu, BERT đưa ra dự đoán dựa trên đại lượng nào?
- A. Trung bình tất cả hidden state của mọi token trong toàn bộ câu đầu vào
- B. Linear head đặt trên vector `h_{[CLS]}` (token cấp câu)
- C. Hidden state thô của token `[SEP]` dùng để ngăn cách hai câu
- D. Position embedding của token đầu tiên trong chuỗi đầu vào mô hình

<details><summary>Đáp án</summary>

**Đúng: B.** `[CLS]` là token cấp câu; NSP/phân loại dùng **linear head trên `h_{[CLS]}`**.
- **A sai:** không phải trung bình toàn bộ token.
- **C sai:** `[SEP]` chỉ ngăn cách hai câu.
- **D sai:** position embedding không mang nội dung để phân loại.
</details>

---

**Câu 15.** Ba loại embedding cộng lại tạo đầu vào cho BERT là:
- A. Token + Position + Segment (câu)
- B. Query + Key + Value
- C. Word2Vec + GloVe + fastText
- D. Encoder + Decoder + Cross-attention

<details><summary>Đáp án</summary>

**Đúng: A.** BERT cộng **token + position + segment embedding**.
- **B sai:** Q/K/V là các phép chiếu *bên trong* attention.
- **C sai:** đó là ba họ static embedding riêng biệt.
- **D sai:** đó là các *khối* kiến trúc.
</details>

---

**Câu 16.** So sánh self-attention của encoder và decoder trong seq2seq transformer:
- A. Encoder dùng masked self-attention còn decoder được nhìn cả hai chiều
- B. Decoder dùng masked self-attention + cross-attention; encoder nhìn hai chiều
- C. Cả hai đều dùng masked self-attention giống hệt nhau ở mọi tầng
- D. Encoder hoàn toàn không dùng self-attention mà chỉ dùng feed-forward

<details><summary>Đáp án</summary>

**Đúng: B.** Encoder: self-attention *hai chiều*. Decoder: **masked self-attention** (chỉ nhìn quá khứ) + **cross-attention** (Q từ decoder, K/V từ encoder).
- **A sai:** đảo ngược vai trò mask.
- **C sai:** encoder *không* mask.
- **D sai:** encoder *có* self-attention.
</details>

---

**Câu 17. (Khó) 🔗** So với Bi-LSTM và convolution, self-attention có bộ ba ưu điểm nào — và điều kiện đi kèm?
- A. Song song hóa + long-range trực tiếp + trọng số động; nhưng cần position embedding
- B. Ít tham số nhất + mô hình long-range tốt + không cần dùng position embedding
- C. Tuần tự nhưng chính xác hơn + trọng số tĩnh + không đòi hỏi dữ liệu lớn để train
- D. Song song hóa + kernel cố định + có sẵn tính bất biến tịnh tiến ngay từ đầu

<details><summary>Đáp án</summary>

**Đúng: A.** Bi-LSTM khó song song; convolution cần nhiều tầng cho long-range và **kernel tĩnh** ([cụm B](B-bieu-dien-don-the-thuc.md)). Self-attention: **song song + long-range + động**, nhưng **cần position embedding**.
- **B sai:** self-attention *cần* position embedding.
- **C sai:** self-attention không tuần tự, trọng số động.
- **D sai:** kernel cố định/bias tịnh tiến là của convolution.
</details>

---

**Câu 18. (Khó) 🔗** Về contrastive alignment kiểu CLIP trong một batch, phát biểu nào đúng?
- A. CLIP căn từng vùng ảnh với từng token một cách trực tiếp, cho grounding chi tiết
- B. Đường chéo ma trận similarity là positive, ngoài chéo là negative; loss đối xứng
- C. Batch càng lớn thì càng ít negative nên càng bất lợi cho quá trình học biểu diễn
- D. Temperature τ không hề ảnh hưởng đến độ tách của cặp đúng khỏi các cặp sai

<details><summary>Đáp án</summary>

**Đúng: B.** Ma trận `S(i,j)=cos(z_i^I,z_j^T)/τ`: **chéo = positive**, ngoài chéo = negative; loss **đối xứng**. CLIP căn *toàn cục* ảnh↔caption (dạy ranking).
- **A sai:** CLIP *không* grounding vùng–token trực tiếp.
- **C sai:** batch lớn cho *nhiều* hard negative → lợi.
- **D sai:** τ *có* ảnh hưởng (ép cặp đúng nổi bật).
</details>
