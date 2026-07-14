# TRẮC NGHIỆM — Cụm A: Tổng quan & 6 Thách thức cốt lõi (16 câu)
Nguồn: `multimodal Learning` (nhập môn, CMU 11-777).

> **Cách dùng để ôn hiệu quả:** Bốn phương án được viết **ngắn, song song, dài cân bằng** — mọi lý giải "vì…" nằm ở phần đáp án ẩn, không thể đoán qua hình thức. Tự chọn đáp án **trước**, rồi mở "Đáp án" xem phần **mổ xẻ từng phương án**. Câu **(Khó)** đòi phân biệt bẫy tinh vi; câu 🔗 cần nối kiến thức nhiều phần.

---

**Câu 1.** Định nghĩa "nghiên cứu" của multimodal nhấn mạnh hai tính chất nào của dữ liệu?
- A. Độ phân giải cao, thu từ nhiều loại cảm biến vật lý khác nhau
- B. Dị thể (heterogeneous) và liên kết (interconnected) với nhau
- C. Kết hợp thị giác máy tính và xử lý ngôn ngữ tự nhiên quy mô lớn
- D. Được gán nhãn đầy đủ, cùng chia sẻ một không gian biểu diễn

<details><summary>Đáp án</summary>

**Đúng: B.** Hai từ khóa của cả môn là **heterogeneous** và **interconnected**.
- **A sai:** đánh đồng "modality" với "cảm biến vật lý" (modality gồm cả loại trừu tượng như sentiment, category); độ phân giải không nằm trong định nghĩa.
- **C sai:** đó chỉ là một *cặp modality cụ thể*, quá hẹp.
- **D sai:** mô tả một *mục tiêu mô hình hóa*, không phải bản chất dữ liệu.
</details>

---

**Câu 2.** So với tín hiệu ảnh/âm thô, các biểu diễn trừu tượng ("object category", "sentiment intensity") có xu hướng:
- A. Dị thể hơn, do bị nén nên mất nhiều cấu trúc chung giữa modality
- B. Dị thể hơn, do mỗi tác vụ tự định nghĩa một loại nhãn riêng biệt
- C. Đồng nhất hơn, do càng xa cảm biến thì chất lượng càng tương đồng
- D. Đồng nhất hơn, do tín hiệu thô luôn được chuẩn hóa trước khi dùng

<details><summary>Đáp án</summary>

**Đúng: C.** Slide nêu: *abstract modalities are more likely to be homogeneous* — càng xa cảm biến, các modality càng dễ đồng nhất/so sánh.
- **A, B sai:** cùng kết luận "dị thể hơn", ngược chiều trục raw→abstract.
- **D sai:** kết luận đúng chiều nhưng lý do bịa (không có bước "chuẩn hóa tín hiệu thô" nào quyết định điều này).
</details>

---

**Câu 3.** "Cấu trúc temporal/spatial/hierarchical" và "mật độ, tần suất thông tin" là hai thứ thuộc về:
- A. Hai trong sáu chiều của tính dị thể (heterogeneity) giữa modality
- B. Hai sub-challenge của thách thức Representation cần được tối ưu
- C. Hai loại kết nối (connection) thống kê giữa các modality với nhau
- D. Hai dạng phản hồi tương tác trong phân loại Partan & Marler

<details><summary>Đáp án</summary>

**Đúng: A.** "Structure" và "Element distribution" là 2 trong **6 chiều heterogeneity**.
- **B sai:** sub-challenge của Representation là Fusion/Coordination/Fission.
- **C sai:** connection thống kê là Association/Dependency.
- **D sai:** phản hồi tương tác là redundancy/dominance/emergence — bẫy trộn bốn danh sách của cụm A.
</details>

---

**Câu 4.** "Ảnh và caption cùng mô tả một cảnh" (biết trước) so với "hai modality phối hợp để trả lời câu hỏi" (khi chạy) lần lượt là:
- A. Interaction (trước khi chạy) và connection (khi chạy mô hình)
- B. Connection (thuộc tính dữ liệu có sẵn) và interaction (khi inference)
- C. Redundancy (dữ liệu) và synergy (dữ liệu), cả hai đều tĩnh sẵn
- D. Alignment (dữ liệu) và fusion (khi inference), thuộc Representation

<details><summary>Đáp án</summary>

**Đúng: B.** "Cùng mô tả cảnh" = **connection** (có sẵn); "phối hợp để trả lời" = **interaction** (khi inference).
- **A sai:** đảo ngược hai khái niệm.
- **C sai:** redundancy/synergy là *loại* interaction, không phải thuộc tính tĩnh.
- **D sai:** alignment/fusion là *thách thức/kỹ thuật*, không phải cặp connection–interaction.
</details>

---

**Câu 5.** Hai tín hiệu kết hợp tạo ra một phản hồi **mới về chất**, không suy được từ tín hiệu đơn lẻ. Đó là:
- A. Enhancement, thuộc redundancy vì hai tín hiệu củng cố lẫn nhau
- B. Dominance, thuộc non-redundancy vì một tín hiệu lấn át tín hiệu kia
- C. Equivalence, thuộc redundancy vì hai tín hiệu cho ra cùng kết quả
- D. Emergence, thuộc non-redundancy vì phản hồi mới trồi lên từ tổ hợp

<details><summary>Đáp án</summary>

**Đúng: D.** Phản hồi *mới về chất* = **Emergence** (non-redundancy).
- **A sai:** Enhancement chỉ làm phản hồi *mạnh hơn* nhưng cùng loại (redundancy).
- **B sai:** Dominance là một modality thắng thế, không sinh nghĩa mới.
- **C sai:** Equivalence là a và b cho *cùng* kết quả — trái hẳn "mới về chất".
</details>

---

**Câu 6.** Ba hướng xử lý ảnh + caption — (i) nén thành một vector chung, (ii) giữ hai vector riêng nhưng kéo gần, (iii) tách thành nhiều vector con — ứng với tiêu chí phân loại nào?
- A. Số modality đầu vào tham gia: bimodal, trimodal, high-modal
- B. Quan hệ giữa số modality và số biểu diễn đầu ra (`>`, `=`, `<`)
- C. Việc dùng encoder pretrained hay huấn luyện từ đầu cùng mạng
- D. Loại hàm mất mát: contrastive, cross-entropy, hoặc reconstruction

<details><summary>Đáp án</summary>

**Đúng: B.** (i) Fusion `#mod>#rep`, (ii) Coordination `#mod=#rep`, (iii) Fission `#mod<#rep`.
- **A sai:** đó là chiều "input modalities" của *interaction*.
- **C sai:** encoder pretrained hay không đều dùng được cho cả ba.
- **D sai:** loại loss là chi tiết cài đặt, không định nghĩa ba sub-challenge.
</details>

---

**Câu 7. (Khó)** Hai vector đã **trừ trung bình** đưa vào coordination bằng cosine similarity. Giá trị này trùng với đại lượng nào?
- A. Khoảng cách Euclid bình phương giữa hai điểm trong không gian
- B. Hệ số tương quan Pearson giữa hai vector đặc trưng
- C. Kernel RBF với σ = 1 đo độ tương đồng phi tuyến
- D. Hiệp phương sai chưa chuẩn hóa của hai vector đầu vào

<details><summary>Đáp án</summary>

**Đúng: B.** Sau *centering*, cosine giữa hai vector đúng bằng **hệ số tương quan Pearson** (tử = hiệp phương sai, mẫu = tích hai độ lệch chuẩn).
- **A sai:** cosine đo *góc*, không phải khoảng cách; Euclid không chuẩn hóa về [−1,1].
- **C sai:** RBF là kernel khác (dựa trên khoảng cách).
- **D sai:** hiệp phương sai *chưa chuẩn hóa* thiếu bước chia hai độ lệch chuẩn — chính bước đó biến nó thành Pearson.
</details>

---

**Câu 8.** Mỗi modality được đưa qua bộ dự đoán riêng cho `ŷ_A`, `ŷ_B`, rồi mới gộp hai quyết định. So với nối đặc trưng thô từ đầu, đây là:
- A. Early fusion, vì hai modality được xử lý ngay trong cùng một mạng
- B. Late fusion, vì kết hợp diễn ra ở mức quyết định sau khi dự đoán riêng
- C. Coordination, vì hai biểu diễn được kéo gần nhau bằng similarity
- D. Fission, vì một modality được tách thành nhiều dự đoán con khác nhau

<details><summary>Đáp án</summary>

**Đúng: B.** Mỗi modality dự đoán riêng rồi gộp *quyết định* = **late fusion**; nối đặc trưng thô từ đầu mới là early fusion.
- **A sai:** mô tả early fusion — trái tình huống.
- **C sai:** coordination dùng *hàm tương đồng*, không gộp hai dự đoán.
- **D sai:** fission tạo nhiều *biểu diễn*, không phải gộp đầu ra dự đoán.
</details>

---

**Câu 9.** Winoground cho thấy CLIP/ViLT/ViLBERT gần mức ngẫu nhiên khi phân biệt hai ảnh–câu chỉ khác nhau ở *cách sắp xếp* cùng một tập từ. Bài học là:
- A. Các mô hình vision–language yếu ở khái quát hợp thành (compositional)
- B. Object detection đã đủ để giải quyết bài toán grounding từ ngôn ngữ
- C. Tri thức ngoài là yếu tố duy nhất còn thiếu ở các mô hình hiện tại
- D. Các mô hình đã bão hòa, đạt hiệu năng gần tối đa trên suy luận thị giác

<details><summary>Đáp án</summary>

**Đúng: A.** Cùng bộ từ, khác *cấu trúc* mà đoán mò → yếu ở **compositional generalization**.
- **B sai:** grounding/detection không xử lý được việc *sắp xếp* quan hệ.
- **C sai:** compositionality cần cả structure/concepts/inference, không chỉ knowledge.
- **D sai:** "gần ngẫu nhiên" nghĩa là rất kém, trái với "bão hòa".
</details>

---

**Câu 10.** Xếp theo lượng content của đầu ra so với đầu vào: tóm tắt video, dịch text→ảnh, sinh đồng thời nhiều modality mới. Thứ tự đúng:
- A. Tóm tắt tăng content, dịch giữ nguyên, sinh mới giảm content
- B. Tóm tắt tăng content, dịch giảm, sinh mới giữ nguyên content
- C. Tóm tắt giảm (`>`), dịch giữ (`=`), sinh mới tăng (`<`)
- D. Cả ba đều giữ nguyên content, chỉ khác modality đầu ra

<details><summary>Đáp án</summary>

**Đúng: C.** Summarization = reduction, Translation = maintenance, Creation = expansion.
- **A, B sai:** đảo sai vai của tóm tắt/dịch/sinh.
- **D sai:** ba tác vụ khác nhau *ở lượng content*, không chỉ khác modality.
</details>

---

**Câu 11.** Một mô hình dùng word embedding lúc train để phân loại cả lớp **chưa từng thấy ảnh**, lúc test **chỉ dùng ảnh**. Cơ chế "modality phụ chỉ có lúc train" này thuộc:
- A. Representation, vì nó học một không gian biểu diễn chung cho hai modality
- B. Alignment, vì nó căn chỉnh phần tử ảnh với phần tử từ tương ứng
- C. Transference (co-learning), vì tri thức ngôn ngữ giúp modality ảnh còn thiếu
- D. Quantification, vì nó đo mức đóng góp của mỗi modality vào kết quả

<details><summary>Đáp án</summary>

**Đúng: C.** Modality phụ **chỉ có lúc train** để giúp modality chính, test chỉ dùng ảnh → **co-learning** (Socher 2013).
- **A sai:** tuy dùng biểu diễn chung, *mục tiêu* là chuyển tri thức không cân xứng → transference.
- **B sai:** alignment nói về nối phần tử↔phần tử.
- **D sai:** quantification là *phân tích*, không phải cơ chế học zero-shot.
</details>

---

**Câu 12. 🔗** Image captioning gán "ổ khóa" với nam, "tạp dề" với nữ dù ảnh không ủng hộ; thêm thị giác lại khiến mô hình *tự tin hơn* vào định kiến. Kết luận đúng theo Quantification:
- A. Kết hợp thị giác và ngôn ngữ luôn làm giảm thiên lệch xã hội có sẵn
- B. Tương tác chéo modality có thể khuếch đại thiên lệch xã hội sẵn có
- C. Thiên lệch chỉ tồn tại ở modality ngôn ngữ, thị giác luôn trung tính
- D. Mô hình captioning không thể học tương quan giả giữa hai biến

<details><summary>Đáp án</summary>

**Đúng: B.** "Worst of Both Worlds" + "Women also Snowboard": tương tác chéo **khuếch đại bias**.
- **A sai:** ngược — kết hợp modality làm bias *tệ hơn*.
- **C sai:** bias có ở cả hai modality.
- **D sai:** captioning *có* học tương quan giả (gender↔action).
</details>

---

**Câu 13.** Reasoning được định nghĩa là kết hợp tri thức qua nhiều bước, *khai thác* thứ gì làm tiền đề?
- A. Kết quả của Generation, vì suy luận cần dữ liệu được sinh ra trước
- B. Multimodal alignment và cấu trúc bài toán đã được nối các phần tử
- C. Kết quả của Quantification, vì cần đo tương tác trước khi suy luận
- D. Kết quả của Transference, vì cần chuyển tri thức trước mỗi bước

<details><summary>Đáp án</summary>

**Đúng: B.** Định nghĩa nêu rõ Reasoning *exploits multimodal alignment and problem structure*.
- **A, C, D sai:** Generation/Quantification/Transference không phải tiền đề *trong định nghĩa* của Reasoning — bẫy ghép sai cặp quan hệ.
</details>

---

**Câu 14.** Quan hệ bao trùm đúng giữa Multimodal AI và Multimodal ML là:
- A. Multimodal ML bao trùm Multimodal AI vì học máy rộng hơn AI
- B. Hai khái niệm tương đương, chỉ khác tên theo cộng đồng nghiên cứu
- C. Multimodal AI bao trùm Multimodal ML vì AI gồm cả reasoning/planning
- D. Không có quan hệ bao trùm; hai lĩnh vực tách biệt hoàn toàn

<details><summary>Đáp án</summary>

**Đúng: C.** Slide nêu *Multimodal AI is a superset of Multimodal ML*.
- **A sai:** đảo ngược quan hệ.
- **B sai:** chúng không tương đương — một là tập con của kia.
- **D sai:** có quan hệ bao trùm rõ ràng.
</details>

---

**Câu 15.** Trong bốn "chiều của tương tác", "additive / multiplicative / nonlinear" rơi vào chiều nào?
- A. Interaction responses, vì chúng mô tả loại phản hồi thu được sau cùng
- B. Interaction mechanics, vì chúng mô tả cách toán học các modality kết hợp
- C. Input modalities, vì chúng đếm số modality tham gia vào suy luận
- D. Context, vì chúng phụ thuộc ngữ cảnh và độ liên quan của tác vụ

<details><summary>Đáp án</summary>

**Đúng: B.** Additive/multiplicative/nonlinear/causal/logical là **interaction mechanics** (cách kết hợp).
- **A sai:** responses là redundancy/dominance/emergence (kết quả).
- **C sai:** input modalities đếm unimodal/bimodal/trimodal.
- **D sai:** context là structure context/task relevance — bẫy vì cả bốn đều là "chiều".
</details>

---

**Câu 16. (Khó)** Ảnh gợi "phòng khách", nhưng caption có "laptop" khiến kết luận đổi thành "phòng làm việc" và câu trả lời từ caption thắng. Đây là:
- A. Unimodal redundancy — hai modality độc lập cho cùng một đáp án
- B. Multimodal enhancement — hai modality cùng củng cố một đáp án mạnh hơn
- C. Unimodal non-redundancy với multimodal dominance — một modality lấn át
- D. Emergence — một đáp án hoàn toàn mới không có ở bất kỳ modality nào

<details><summary>Đáp án</summary>

**Đúng: C.** Hai modality cho đáp án *khác nhau* (non-redundancy), modality mạnh (caption) **lấn át** để đổi kết luận → **dominance**.
- **A sai:** redundancy là *cùng* đáp án; ở đây hai modality mâu thuẫn.
- **B sai:** enhancement giả định cùng hướng rồi mạnh hơn, không đổi hẳn đáp án.
- **D sai:** emergence tạo đáp án *mới về chất*; "phòng làm việc" vốn đã là một khả năng từ caption.
</details>
