# TRẮC NGHIỆM — Cụm C: Fusion, Coordination & Fission (18 câu)
Nguồn: `lecture3_1-MultimodalFusion`, `lecture3_2-MultimodalCoordinationFission`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — mọi lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần suy luận công thức; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Trong `z = w0 + w1·x_A + w2·x_B + w3·(x_A×x_B) + ε`, để kiểm tra "hiệu ứng x_A có phụ thuộc x_B không", ta xét:
- A. Số hạng `w1·x_A`, kiểm tra hệ số `w1` khác 0 có ý nghĩa thống kê
- B. Số hạng `w3·(x_A×x_B)`, kiểm tra khoảng tin cậy `w3` không chứa 0
- C. Số hạng `w0`, kiểm tra xem giá trị intercept có dương hay không
- D. Số hạng `ε`, kiểm tra phần dư có tuân theo phân phối chuẩn không

<details><summary>Đáp án</summary>

**Đúng: B.** "Hiệu ứng x_A phụ thuộc x_B" = tương tác nhân ở `w3·(x_A×x_B)`; kết luận khi CI của `w3` **không chứa 0**.
- **A sai:** `w1` là hiệu ứng *riêng* của x_A (additive).
- **C sai:** `w0` là mức nền chung.
- **D sai:** phân phối phần dư là giả định hồi quy, không phải tương tác.
</details>

---

**Câu 2.** Additive fusion `z = f_A(x_A) + f_B(x_B)` tương đương dạng nào và có hạn chế gì?
- A. Tương đương tensor fusion; hạn chế là số tham số bùng nổ theo số modality
- B. Tương đương late fusion/ensemble; hạn chế là bỏ qua tương tác nhân
- C. Tương đương bilinear fusion; hạn chế là bắt buộc phải có dữ liệu ghép cặp
- D. Tương đương gated fusion; hạn chế là gate rất khó tính được gradient

<details><summary>Đáp án</summary>

**Đúng: B.** Cộng đầu ra hai encoder = **late fusion/ensemble**; hạn chế: **không có số hạng nhân** nên bỏ qua tương tác chéo.
- **A sai:** tensor fusion mới bắt tương tác nhân và bị bùng nổ tham số.
- **C sai:** bilinear là dạng nhân; ghép cặp là đặc điểm coordination.
- **D sai:** gated fusion có gate/attention, khác additive.
</details>

---

**Câu 3. (Khó)** Tensor Fusion (Zadeh 2017) lấy tích ngoài của các vector `[x;1]`. So với additive fusion, nó được gì và mất gì?
- A. Được: bắt đồng thời số hạng uni/bi/tri-modal; Mất: tham số tăng cấp số nhân theo số modality
- B. Được: giảm mạnh số tham số nhờ chia sẻ trọng số; Mất: chỉ dùng được cho một modality duy nhất
- C. Được: không cần bất kỳ dữ liệu ghép cặp nào; Mất: hội tụ chậm hơn nhiều so với late fusion
- D. Được: loại bỏ được hoàn toàn overfitting; Mất: không biểu diễn được quan hệ phi tuyến

<details><summary>Đáp án</summary>

**Đúng: A.** Tích ngoài sinh đồng thời số hạng unimodal ("1"), bimodal, trimodal → nhưng tham số **tăng cấp số nhân** theo số modality (động lực cho Low-rank Fusion).
- **B sai:** tensor fusion *tăng* tham số; dùng cho nhiều modality.
- **C sai:** ghép cặp không phải điểm phân biệt; tốc độ hội tụ không phải "mất" chính.
- **D sai:** nó *có* biểu diễn tương tác, và không "loại bỏ overfitting".
</details>

---

**Câu 4.** Low-rank Multimodal Fusion (Liu 2018) giải quyết vấn đề gì của Tensor Fusion, bằng cách nào?
- A. Thiếu tương tác phi tuyến; giải bằng cách xếp chồng thêm nhiều tầng MLP
- B. Chi phí tham số/tính toán lớn; giải bằng phân rã low-rank (CP) weight và input
- C. Không xử lý được dữ liệu thiếu; giải bằng cách suy diễn các modality bị vắng
- D. Không dùng được cho quá hai modality; giải bằng cách nối chuỗi các modality

<details><summary>Đáp án</summary>

**Đúng: B.** LMF phân rã tensor trọng số theo **low-rank factors (CP)** → tính hiệu quả mà không dựng tensor đầy đủ, giữ biểu diễn tương tác nhưng **giảm chi phí**.
- **A sai:** vấn đề tensor fusion là *chi phí*, không phải thiếu phi tuyến.
- **C sai:** suy diễn modality thiếu là hướng robustness.
- **D sai:** tensor fusion vốn dùng được nhiều modality.
</details>

---

**Câu 5. (Khó) 🔗** EMAP (Hessel & Lee 2020) chiếu mô hình fusion phi tuyến về additive tốt nhất. Phát hiện đáng chú ý:
- A. Mô hình phi tuyến luôn vượt xa additive, nên nên ưu tiên kiến trúc phức tạp
- B. Chênh lệch hiệu năng thường nhỏ, nhiều mô hình không thực dùng tương tác chéo
- C. EMAP là một toán tử fusion mới, mạnh hơn tensor fusion trên hầu hết tác vụ
- D. EMAP đo mutual information giữa hai modality để phục vụ việc chọn mô hình

<details><summary>Đáp án</summary>

**Đúng: B.** Sau khi chiếu về additive, **chênh lệch thường rất nhỏ** → nhiều mô hình "phức tạp" gần additive. Liên hệ [cụm I](I-quantification.md): `μ` của EMAP đo tổng lượng tương tác chéo; "có tương tác" = `f` không phân rã được thành `f_A+f_B`.
- **A sai:** ngược — additive là baseline mạnh bất ngờ.
- **C sai:** EMAP là *công cụ đo/chiếu*, không phải toán tử fusion.
- **D sai:** EMAP đo tương tác *non-additive*, không phải MI.
</details>

---

**Câu 6. 🔗** Trong gated fusion, chọn "hard gating" (0/1) thay vì "soft gating" (0–1) kéo theo hệ quả huấn luyện:
- A. Hard gating khả vi nên train được bằng gradient thông thường, dễ hơn soft gating
- B. Hard gating rời rạc nên khó lấy gradient, thường phải train bằng reinforcement learning
- C. Soft gating rời rạc nên cần reinforcement learning, còn hard gating thì không cần
- D. Cả hai loại gating đều không ảnh hưởng gì tới cách tính gradient của mô hình

<details><summary>Đáp án</summary>

**Đúng: B.** Soft (softmax) khả vi; **hard** (0/1) rời rạc → đạo hàm khó, thường dùng **RL** (liên hệ REINFORCE ở [cụm F](F-interaction-inference.md)).
- **A sai:** hard gating *không* khả vi trơn.
- **C sai:** đảo ngược — soft mới khả vi.
- **D sai:** rời rạc/liên tục *có* ảnh hưởng trực tiếp đến gradient.
</details>

---

**Câu 7. 🔗** Bài học kiến trúc khi fuse ảnh camera (2D dày) và LiDAR (3D thưa) cho 3D detection (HMFI):
- A. Fuse thô trực tiếp hai modality luôn hiệu quả hơn việc căn chỉnh cấu trúc trước
- B. Căn chỉnh cấu trúc (đưa về voxel 3D chung) trước khi fuse thường là phần khó nhất
- C. Hai modality vốn đồng nhất về cấu trúc nên fusion rất dễ, không cần alignment gì
- D. Cần phải gán nhãn tương ứng word–region thủ công thì mới có thể fuse được

<details><summary>Đáp án</summary>

**Đúng: B.** Camera và LiDAR **dị thể** → đưa cả hai về **voxel 3D chung** trước khi fuse; **structure alignment trước fusion khó hơn cả toán tử fusion** (similarity loss làm supervision).
- **A sai:** fuse thô modality dị thể kém hiệu quả.
- **C sai:** chúng *dị thể*.
- **D sai:** HMFI dùng similarity loss tự giám sát.
</details>

---

**Câu 8.** FuseMix (2024) đạt hiệu quả dữ liệu/tính toán cao chủ yếu nhờ chiến lược nào?
- A. Huấn luyện lại toàn bộ encoder lớn từ đầu trên một tập dữ liệu khổng lồ
- B. Đóng băng encoder pretrained, chỉ train adapter nhẹ (contrastive + mixup)
- C. Thay contrastive bằng tensor fusion bậc cao để tăng khả năng biểu diễn
- D. Bỏ hoàn toàn bước căn chỉnh không gian latent để tiết kiệm tính toán

<details><summary>Đáp án</summary>

**Đúng: B.** FuseMix **freeze** encoder lớn, chỉ train ~1–2M tham số adapter với contrastive + **multimodal mixup** → giảm ~600× GPU-days.
- **A sai:** ngược — điểm mấu chốt là *không* train lại encoder.
- **C sai:** nó dùng contrastive nhẹ.
- **D sai:** căn chỉnh latent chính là mục tiêu adapter.
</details>

---

**Câu 9. 🔗** Thêm modality (RGB + Audio + Optical Flow) đôi khi *làm giảm* hiệu năng. Hai nguyên nhân là:
- A. Mọi modality luôn dư thừa thông tin của nhau nên thêm vào chỉ gây nhiễu vô ích
- B. Mạng đa thể thức dễ overfit hơn, và các modality overfit/generalize khác tốc độ
- C. Mutual information giữa các modality luôn bằng 0 nên không thể kết hợp được gì
- D. Thiếu position embedding nên mô hình không thể phân biệt được các modality

<details><summary>Đáp án</summary>

**Đúng: B.** (1) mô hình phức tạp hơn → **dễ overfit**; (2) modality **overfit/generalize khác tốc độ** (greedy learning) → giải bằng **OGR** ([cụm I](I-quantification.md)).
- **A sai:** không "luôn dư thừa"; có unique/synergy hữu ích.
- **C sai:** MI thường >0.
- **D sai:** position embedding không liên quan.
</details>

---

**Câu 10.** Tiêu chí phân biệt Fusion / Coordination / Fission là:
- A. Số lượng modality đầu vào tham gia vào mô hình đa thể thức
- B. Quan hệ giữa số modality và số biểu diễn đầu ra (`>`, `=`, `<`)
- C. Việc dùng contrastive loss hay là dùng reconstruction loss
- D. Việc encoder được pretrained hay huấn luyện chung với mạng

<details><summary>Đáp án</summary>

**Đúng: B.** Fusion `>`, Coordination `=`, Fission `<`.
- **A sai:** số modality đầu vào không phân biệt được (đều có thể 2 modality).
- **C, D sai:** loại loss / tình trạng encoder là chi tiết cài đặt.
</details>

---

**Câu 11. (Khó)** Sau huấn luyện CLIP bằng contrastive learning, hai vector `z_L` và `z_V`:
- A. Trở thành một vector đồng nhất duy nhất dùng chung cho cả ảnh lẫn text
- B. Là hai không gian riêng được phối hợp: cặp đúng kéo gần, cặp sai đẩy xa
- C. Được nối (concatenate) thành một vector chung rồi mới đưa vào dự đoán
- D. Được tách thành phần shared và phần unique bằng kỹ thuật factorization

<details><summary>Đáp án</summary>

**Đúng: B.** CLIP là **coordination**: `z_L`, `z_V` ở **hai không gian riêng** được phối hợp (không đồng nhất).
- **A sai:** chúng không hợp nhất thành một vector.
- **C sai:** nối vector là *fusion*.
- **D sai:** tách shared/unique là *fission*.
</details>

---

**Câu 12.** CCA (Canonical Correlation Analysis) khác cosine/kernel ở đặc điểm nào?
- A. Học một phép chiếu duy nhất tối đa hóa khoảng cách Euclid giữa hai view
- B. Học nhiều phép chiếu trực giao nhau, cùng tối đa hóa tương quan hai view
- C. Không hề cần dữ liệu ghép cặp giữa hai view khi tối ưu hàm mục tiêu
- D. Chỉ áp dụng được cho dữ liệu rời rạc, không dùng cho vector liên tục

<details><summary>Đáp án</summary>

**Đúng: B.** CCA học **nhiều cặp phép chiếu trực giao** để hai view tương quan tối đa (biến thể sâu: DCCAE).
- **A sai:** CCA tối đa hóa *tương quan*, không phải Euclid.
- **C sai:** CCA *cần* dữ liệu ghép cặp.
- **D sai:** CCA áp dụng cho vector liên tục.
</details>

---

**Câu 13. (Khó)** InfoNCE liên hệ với mutual information `I(X_A;X_B)` như thế nào?
- A. Tối đa hóa trực tiếp `I` mà không thông qua bất kỳ chặn nào
- B. Tối thiểu hóa `I` để buộc hai modality trở nên độc lập nhau
- C. Tối ưu một *chặn dưới* của `I`: `I ≥ log N − L*`, tăng N làm chặt hơn
- D. Không hề có liên hệ gì với mutual information giữa hai modality

<details><summary>Đáp án</summary>

**Đúng: C.** Minimize InfoNCE = maximize **chặn dưới** MI: `I ≥ log N − L*`; nhiều negative → chặn chặt hơn.
- **A sai:** không phải tối đa hóa trực tiếp mà là lower bound.
- **B sai:** contrastive *tăng* thông tin chung.
- **D sai:** liên hệ chặt qua bất đẳng thức.
</details>

---

**Câu 14. 🔗** Nguyên lý InfoMin / multi-view redundancy (Tian 2020) khuyến nghị điều gì, và lưu ý cho đa thể thức?
- A. Càng nhiều thông tin chung càng tốt; và điều này luôn đúng cho mọi cặp modality
- B. Vừa đủ thông tin task, bỏ nuisance (U ngược); giả định này có thể sai với đa thể thức
- C. Càng ít thông tin chung càng tốt tuyệt đối; và luôn đúng với mọi bài đa thể thức
- D. Không chia sẻ bất kỳ thông tin nào; hai view nên hoàn toàn độc lập với nhau

<details><summary>Đáp án</summary>

**Đúng: B.** Hiệu năng theo MI có dạng **U ngược**, sweet spot khi `I(v1;v2)=I(x;y)`. ⚠️ Multi-view redundancy có thể sai với đa thể thức (modality có unique info — [cụm I](I-quantification.md)).
- **A sai:** không "càng nhiều càng tốt".
- **C sai:** không "càng ít càng tốt tuyệt đối".
- **D sai:** hoàn toàn độc lập thì mất tín hiệu chung.
</details>

---

**Câu 15. 🔗** Partial Information Decomposition (PID) phân rã thông tin task-relevant thành bốn thành phần nào?
- A. Redundancy, Uniqueness của modality 1, Uniqueness của modality 2, và Synergy
- B. Additive, Multiplicative, Gated, và Nonlinear interactions
- C. Association, Dependency, Correspondence, và Relationship
- D. Entropy, Cross-entropy, Mutual information, và Perplexity

<details><summary>Đáp án</summary>

**Đúng: A.** PID = Redundancy + Uniqueness U1, U2 + Synergy — bốn phần **không âm**.
- **B sai:** đó là *cơ chế fusion*.
- **C sai:** đó là bốn loại *connection* ([cụm A](A-tong-quan-6-thach-thuc.md)).
- **D sai:** đó là các đại lượng lý thuyết thông tin rời rạc.
</details>

---

**Câu 16. 🔗** Thành phần **Synergy** trong PID tương ứng khái niệm nào trong phân loại Partan & Marler?
- A. Redundancy / Equivalence — hai modality mang cùng một thông tin về task
- B. Dominance — một modality lấn át và quyết định modality kia trong suy luận
- C. Emergence — thông tin mới trồi lên chỉ khi kết hợp cả hai modality
- D. Independence — hai modality đóng góp một cách tách rời hoàn toàn nhau

<details><summary>Đáp án</summary>

**Đúng: C.** Synergy = **Emergence** (VD sarcasm) — [cụm A](A-tong-quan-6-thach-thuc.md).
- **A sai:** redundancy PID ↔ Equivalence/Enhancement.
- **B, D sai:** dominance/independence ↔ uniqueness.
</details>

---

**Câu 17.** Fission ở mức modality tách một cặp ảnh–ngôn ngữ thành các phần:
- A. Một vector chung duy nhất chứa toàn bộ thông tin của cả hai modality
- B. Phần chỉ thuộc ngôn ngữ, phần chỉ thuộc thị giác, và phần chung cả hai
- C. Hai vector được kéo lại gần nhau bằng hàm cosine similarity đo góc
- D. Một chuỗi các visual token rời rạc để đưa vào một mô hình transformer

<details><summary>Đáp án</summary>

**Đúng: B.** Fission tạo **nhiều biểu diễn hơn**: tách **chỉ-ngôn-ngữ / chỉ-thị-giác / chung**.
- **A sai:** một vector chung là *fusion*.
- **C sai:** kéo gần bằng similarity là *coordination*.
- **D sai:** visual token là kỹ thuật generation/ViT.
</details>

---

**Câu 18. (Khó)** Trong factorized representation learning (Tsai 2019, MFM), để mô hình hóa phần **unique** của một modality, mục tiêu là:
- A. Tối đa hóa `I(z; modality)` và tối thiểu hóa `H(z | modality)`
- B. Tối thiểu hóa `I(z; modality)` và tối đa hóa entropy tổng `H(z)`
- C. Tối đa hóa khoảng cách Euclid giữa hai modality trong không gian latent
- D. Tối thiểu hóa perplexity của biểu diễn trên toàn bộ tập validation

<details><summary>Đáp án</summary>

**Đúng: A.** **Maximize `I(z;modality)`** + **minimize `H(z|modality)`**; MFM kết hợp loss discriminative + generative + no-overlap.
- **B sai:** tối thiểu MI sẽ *vứt* thông tin modality.
- **C, D sai:** Euclid / perplexity không phải tiêu chí factorization thông tin.
</details>
