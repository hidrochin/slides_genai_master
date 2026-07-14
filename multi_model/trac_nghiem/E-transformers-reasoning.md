# TRẮC NGHIỆM — Cụm E: Transformer Đa thể thức & Suy luận có Cấu trúc (18 câu)
Nguồn: `lecture5_1`, `lecture6_1` (Multimodal Transformers), `Lecture5_2` (Structured Representations & Reasoning).

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Ba mẫu thiết kế transformer đa thể thức là:
- A. Early fusion, Late fusion, và Hybrid fusion theo thời điểm kết hợp modality
- B. One-stream (nối chung), Cross-modal (co-attention), Modality-shift (dịch)
- C. Encoder-only, Decoder-only, và Encoder-decoder theo cấu hình transformer
- D. Graph Convolution, Graph Attention, và GraphSAGE theo cách gộp hàng xóm

<details><summary>Đáp án</summary>

**Đúng: B.** One-stream (VisualBERT/UNITER), Cross-modal (ViLBERT/LXMERT), Modality-shift (MAG-BERT).
- **A sai:** early/late/hybrid là góc nhìn thời điểm fusion cổ điển.
- **C sai:** encoder/decoder là cấu hình transformer tổng quát.
- **D sai:** đó là ba biến thể GNN.
</details>

---

**Câu 2.** VisualBERT/UNITER (mẫu one-stream) xử lý đầu vào thế nào?
- A. Hai luồng riêng cho ảnh và text, trao đổi qua co-attention nhiều tầng liên tiếp
- B. Nối text token và image region thành một chuỗi, full self-attention chung
- C. Giữ ngôn ngữ làm chính rồi dùng gate để dịch bằng tín hiệu từ thị giác
- D. Chỉ mã hóa ảnh và bỏ qua text hoàn toàn để giảm chi phí tính toán

<details><summary>Đáp án</summary>

**Đúng: B.** One-stream: `[CLS] text [SEP] region…` → shared transformer với **full self-attention** across text & image.
- **A sai:** mô tả ViLBERT/LXMERT.
- **C sai:** mô tả MAG-BERT.
- **D sai:** cả hai xử lý cả ảnh lẫn text.
</details>

---

**Câu 3. 🔗** Trong cross-modal attention hướng Vision → Language, Query được lấy từ đâu?
- A. Từ thị giác, vì thị giác cung cấp thông tin mới cần được truy vấn tới
- B. Từ ngôn ngữ, vì Query đến từ modality cần được cập nhật, K/V từ modality kia
- C. Từ cả hai modality cùng một lúc để đảm bảo tính đối xứng của attention
- D. Từ một modality trung gian được sinh ra bởi một bộ encoder dùng chung

<details><summary>Đáp án</summary>

**Đúng: B.** Query từ modality **cần cập nhật** (V→L nghĩa là cập nhật *ngôn ngữ*): `α=softmax(Q_L K_V^T/√d)` (dùng lại attention của [cụm D](D-alignment.md)).
- **A sai:** modality cung cấp thông tin là *Key/Value*.
- **C sai:** cross-attention một hướng lấy Query từ một phía.
- **D sai:** không có modality trung gian.
</details>

---

**Câu 4.** MAG-BERT (mẫu modality-shift) tích hợp thông tin phi ngôn ngữ bằng cách:
- A. Nối mọi modality thành một chuỗi rồi chạy self-attention chung một lần
- B. Thêm một dịch chuyển đa thể thức học được (MAG) vào hidden state của BERT
- C. Dùng optimal transport để căn các word với các region tương ứng của ảnh
- D. Sinh một scene graph rồi thực hiện suy luận tuần tự trên đồ thị đó

<details><summary>Đáp án</summary>

**Đúng: B.** MAG thêm **shift học được** vào hidden state BERT ("great" + cười → tích cực; + mỉa mai → tiêu cực).
- **A sai:** đó là one-stream.
- **C sai:** OT căn word–region là UNITER/ViLT.
- **D sai:** scene graph là Neural State Machine.
</details>

---

**Câu 5.** ViT chia ảnh thành patch 16×16 (coi như token). Điều này cho phép gì nhưng đòi hỏi gì?
- A. Cho phép dùng convolution nhiều tầng; nhưng đòi hỏi ảnh có độ phân giải thấp
- B. Cho phép dùng transformer trên ảnh; nhưng thiếu bias locality nên cần pretrain lớn
- C. Cho phép xử lý ảnh bằng một mạng RNN quét theo hàng; nhưng đòi hỏi ít dữ liệu
- D. Cho phép bỏ position embedding cho ảnh; nhưng đòi hỏi kernel cố định kiểu Gabor

<details><summary>Đáp án</summary>

**Đúng: B.** Patch→token cho phép áp **transformer** lên ảnh; ViT thiếu **bias locality** → cần **pretrain lớn** (bù lại: long-range trực tiếp, attention động).
- **A sai:** ViT thay convolution.
- **C sai:** ViT không dùng RNN, cần *nhiều* dữ liệu.
- **D sai:** ViT *vẫn* cần position embedding.
</details>

---

**Câu 6. (Khó) 🔗** Ở chế độ ít dữ liệu, CNN thường thắng ViT. Lý do bản chất:
- A. CNN có nhiều tham số hơn ViT nên học nhanh hơn khi thiếu dữ liệu
- B. CNN mang sẵn bias locality + đẳng biến tịnh tiến nên data-efficient hơn
- C. ViT không thể song song hóa được nên hội tụ chậm khi thiếu dữ liệu
- D. ViT không dùng được với ảnh có nhiều kênh màu như ảnh RGB thông thường

<details><summary>Đáp án</summary>

**Đúng: B.** CNN có **bias locality + translation equivariance** sẵn ([cụm B](B-bieu-dien-don-the-thuc.md)) → ít dữ liệu vẫn khái quát tốt.
- **A sai:** ViT thường *nhiều* tham số hơn.
- **C sai:** self-attention *song song hóa được*.
- **D sai:** ViT xử lý được ảnh nhiều kênh.
</details>

---

**Câu 7.** Masked Auto-Encoder (MAE) có đặc điểm gì về tỉ lệ mask và vai trò decoder?
- A. Mask ~15% patch; decoder được dùng cả lúc pretrain lẫn lúc inference downstream
- B. Mask ~75% patch; decoder chỉ dùng lúc pretrain; loss chỉ tính trên patch bị mask
- C. Mask 100% patch của ảnh; bỏ hẳn encoder mà chỉ giữ lại phần decoder tái tạo
- D. Không mask bất kỳ patch nào; chỉ nén ảnh qua một bottleneck rồi giải nén lại

<details><summary>Đáp án</summary>

**Đúng: B.** MAE mask **~75%**; encoder chỉ xử lý patch thấy được, decoder nhẹ **chỉ dùng lúc pretrain**, loss chỉ trên patch mask.
- **A sai:** ~15% là của MLM/BERT.
- **C sai:** MAE giữ encoder (ViT).
- **D sai:** MAE *mask rồi tái tạo*, không chỉ nén.
</details>

---

**Câu 8.** ViLT (≈ ViT + BERT) đạt inference nhanh hơn ViLBERT/LXMERT chủ yếu nhờ:
- A. Giữ nguyên object detector nặng nhưng nén lại đầu ra của bộ detector đó
- B. Bỏ object detector nặng, dùng patch embedding cho ảnh + text token chung
- C. Chỉ xử lý phần text và bỏ hoàn toàn nhánh ảnh để giảm bớt chi phí tính toán
- D. Thay thế transformer bằng một mạng RNN để giảm độ phức tạp tính toán tổng thể

<details><summary>Đáp án</summary>

**Đúng: B.** ViLT thay **object detector** (chậm) bằng **patch embedding** → inference nhanh.
- **A sai:** ViLT *bỏ* detector.
- **C sai:** ViLT vẫn xử lý ảnh (bằng patch).
- **D sai:** ViLT dùng transformer.
</details>

---

**Câu 9.** Ý tưởng "Align before Fuse" của ALBEF nghĩa là:
- A. Fuse cross-modal trước rồi mới thực hiện căn chỉnh biểu diễn hai modality
- B. Căn (contrastive) biểu diễn segment-level trước, rồi mới fuse để dễ hơn
- C. Không bao giờ căn chỉnh, chỉ thực hiện một lần fuse duy nhất giữa hai modality
- D. Chỉ căn chỉnh mà không bao giờ fuse hai modality lại với nhau trong mô hình

<details><summary>Đáp án</summary>

**Đúng: B.** ALBEF căn chỉnh (contrastive) **trước** khi fuse → biểu diễn gần nhau giúp fusion dễ hơn.
- **A sai:** đảo thứ tự.
- **C, D sai:** ALBEF làm *cả hai* (align rồi fuse).
</details>

---

**Câu 10.** VideoBERT tạo "visual words" (token thị giác rời rạc cho video) bằng:
- A. Object detector giám sát gán nhãn cho từng khung hình trong đoạn video
- B. K-means clustering trên đặc trưng video để tạo ra các token rời rạc
- C. Optimal transport giữa các khung hình và các câu bình luận tương ứng
- D. Position embedding thời gian gán cho từng khung hình theo thứ tự xuất hiện

<details><summary>Đáp án</summary>

**Đúng: B.** VideoBERT dùng **K-means clustering** trên đặc trưng để tạo "visual words" rời rạc.
- **A sai:** không dùng detector giám sát để tạo token.
- **C sai:** OT không phải cách tạo visual words.
- **D sai:** position embedding là thông tin vị trí, không rời rạc hóa nội dung.
</details>

---

**Câu 11.** Với dữ liệu video **weakly-paired** (clip ngắn + ít từ, có thể lệch nhau), hai kỹ thuật được dùng là:
- A. Optimal transport và CTC
- B. Multi-instance learning và contrastive learning
- C. Beam search và teacher forcing
- D. Batch normalization và dropout

<details><summary>Đáp án</summary>

**Đúng: B.** **Multi-instance learning** xử lý misalignment; **contrastive learning** học self-supervised.
- **A sai:** CTC/OT không phải cặp kỹ thuật này.
- **C sai:** beam search/teacher forcing thuộc sinh chuỗi.
- **D sai:** batch norm/dropout là kỹ thuật huấn luyện chung.
</details>

---

**Câu 12. 🔗** Quan hệ đúng giữa transformer self-attention và GNN là:
- A. Transformer self-attention là một trường hợp đặc biệt của convolution CNN
- B. Transformer self-attention tương đương GNN chạy trên đồ thị đầy đủ (fully-connected)
- C. GNN chính là transformer nhưng đã bỏ đi bước chuẩn hóa bằng hàm softmax
- D. Hai mô hình hoàn toàn không liên quan gì tới nhau về mặt cơ chế hoạt động

<details><summary>Đáp án</summary>

**Đúng: B.** Self-attention nối **mọi token với mọi token** = message passing trên **đồ thị đầy đủ**; GNN dùng cấu trúc đồ thị thay vì fully-connected.
- **A sai:** transformer không phải trường hợp của CNN.
- **C sai:** khác biệt nằm ở *cấu trúc kết nối*, không ở softmax.
- **D sai:** hai mô hình liên hệ chặt.
</details>

---

**Câu 13.** Graph Attention Network (GAT) khác Graph Convolution Network (GCN) khi gộp hàng xóm ở chỗ:
- A. GAT dùng cùng một trọng số cho mọi hàng xóm, chỉ khác nhau ở cách chuẩn hóa
- B. GAT học trọng số attention `α_uv` riêng cho từng cạnh khi aggregate hàng xóm
- C. GAT không hề dùng neighborhood aggregation mà nối các node thành một chuỗi
- D. GAT chỉ áp dụng được cho đồ thị vô hướng chứ không dùng cho đồ thị có hướng

<details><summary>Đáp án</summary>

**Đúng: B.** GAT học **attention weight `α_uv`** cho mỗi cạnh. GCN dùng **cùng trọng số, khác normalization** (chính là phương án A).
- **A sai:** đó là mô tả *GCN*.
- **C sai:** GAT *có* neighborhood aggregation.
- **D sai:** GAT dùng được cho đồ thị có hướng.
</details>

---

**Câu 14. (Khó)** Neural Module Network V2 (Hu 2017) cải tiến gì so với V1 (Andreas 2016) về việc tạo layout suy luận?
- A. Thêm nhiều module thủ công hơn để phủ được nhiều loại câu hỏi khác nhau
- B. Dùng RNN dự đoán layout (policy) — không cần parse câu hỏi hay luật thủ công
- C. Bỏ hoàn toàn cơ chế attention trong các module để đơn giản hóa mô hình
- D. Chuyển từ suy luận thị giác sang xử lý tín hiệu âm thanh đa thể thức

<details><summary>Đáp án</summary>

**Đúng: B.** V2 dùng **RNN policy dự đoán layout end-to-end** → không cần parse, không cần luật thủ công.
- **A sai:** cải tiến là *học* layout, không phải thêm module thủ công.
- **C sai:** module vẫn dùng attention.
- **D sai:** vẫn là visual reasoning.
</details>

---

**Câu 15.** Neuro-Symbolic VQA (Yi 2018) đạt tính diễn giải cao bằng cách tách bạch:
- A. Suy luận (reasoning) khỏi nhận thức thị giác/ngôn ngữ (perception)
- B. Bộ encoder khỏi bộ decoder ở trong kiến trúc tổng thể của mô hình
- C. Token embedding khỏi position embedding ở đầu vào của mô hình
- D. Tập dữ liệu huấn luyện khỏi tập dữ liệu kiểm tra khi đánh giá mô hình

<details><summary>Đáp án</summary>

**Đúng: A.** Tách **reasoning khỏi perception** ("Disentangling Reasoning from Vision and Language Understanding").
- **B, C sai:** đó là tách các *thành phần kiến trúc*.
- **D sai:** tách train/test không liên quan diễn giải suy luận.
</details>

---

**Câu 16.** Neural State Machine (Hudson & Manning 2019) suy luận bằng cách:
- A. Nối ảnh và text thành một chuỗi rồi chạy self-attention chung một lần duy nhất
- B. Sinh scene graph, coi như state machine, dịch câu hỏi thành soft instructions
- C. Dùng K-means clustering để tạo visual words rồi thực hiện phân loại chúng
- D. Mask 75% patch ảnh rồi tái tạo lại chúng để học biểu diễn thị giác tốt hơn

<details><summary>Đáp án</summary>

**Đúng: B.** NSM: sinh **scene graph** → coi như **state machine** → câu hỏi thành **soft instructions** → suy luận tuần tự.
- **A sai:** đó là one-stream transformer.
- **C sai:** đó là VideoBERT.
- **D sai:** đó là MAE.
</details>

---

**Câu 17.** Dataset CLEVR đặc biệt phù hợp với neural module networks vì:
- A. Nó gồm ảnh tự nhiên có độ nhiễu cao và rất sát với các tình huống thực tế
- B. Nó là dataset chẩn đoán suy luận hợp thành, câu hỏi có cấu trúc chương trình
- C. Nó chỉ có nhãn nhị phân đơn giản nên mô hình rất dễ huấn luyện và hội tụ
- D. Nó không hề có câu hỏi kèm theo, chỉ có các bức ảnh để đem đi phân loại

<details><summary>Đáp án</summary>

**Đúng: B.** CLEVR = dataset **compositional visual reasoning**, câu hỏi có cấu trúc chương trình (attend/filter/count/compare) → khớp layout module.
- **A sai:** CLEVR là ảnh *tổng hợp có kiểm soát*.
- **C sai:** câu hỏi *đa bước, có cấu trúc*.
- **D sai:** CLEVR *có* câu hỏi.
</details>

---

**Câu 18. 🔗** Trong khối transformer encoder, vai trò của các thành phần là:
- A. FFN trộn thông tin giữa các token, self-attention biến đổi từng token riêng lẻ
- B. Self-attention trộn thông tin giữa token, FFN biến đổi từng token, Add&Norm ổn định
- C. Position embedding thay thế cho self-attention, còn FFN chỉ được dùng khi decode
- D. Cross-attention là bắt buộc trong mọi encoder, và encoder không hề có FFN nào

<details><summary>Đáp án</summary>

**Đúng: B.** `MHSA → Add&Norm → FFN → Add&Norm`: self-attention **trộn token**, FFN **biến đổi từng token**, Add&Norm **ổn định** (residual liên hệ ResNet ở [cụm B](B-bieu-dien-don-the-thuc.md)).
- **A sai:** đảo vai attention/FFN.
- **C sai:** position embedding *bổ sung* cho self-attention; FFN dùng cả ở encoder.
- **D sai:** encoder không cần cross-attention; FFN là chuẩn.
</details>
