# CHEAT-SHEET — Cụm H: Chuyển giao (Thách thức 5 – Transference)
Nguồn: `Lecture11.2-Transference`. Chuyển tri thức giữa modality để hỗ trợ modality chính/yếu.

> **Định nghĩa Transference:** *Chuyển tri thức giữa modality, thường để **giúp modality chính (primary/target)** vốn có thể nhiễu hoặc ít tài nguyên.* **3 sub-challenge:** **Transfer** (từ pretrained) · **Co-learning** (chia sẻ không gian biểu diễn) · **Model Induction** (giữ model đơn thể thức riêng, cảm ứng hành vi chung).

---

## 5a. TRANSFER via Pretrained Models ⭐
**Định nghĩa:** chuyển tri thức từ mô hình pretrained quy mô lớn (tri thức = **tham số mạng `θ*`**, VD BERT) sang tác vụ downstream của modality chính.
- **Các cách adapt (giống Cụm G):** ① finetuning · ② prefix/prompt tuning (Frozen — adapter, "This is a dax") · ③ representation tuning (MAG shift) · ④ classifier gradient / classifier-free tuning.
- **Multitask & Transfer Learning ⭐:** chuyển tri thức qua nhiều tác vụ, mỗi tác vụ trên **tập modality khác nhau** → quan trọng khi có tác vụ **low-resource**.
  - **HighMMT / Gato (Generalist Agent):** **1 model thống nhất + chia sẻ tham số + multitask**. Thành phần: **modality-specific embeddings** → **standardized input sequence** → shared multimodal model → **task-specific classifiers**. Cùng kiến trúc & cùng tham số cho video/sentiment/robot...
  - **Kết quả:** thêm source task từ modality/lĩnh vực khác → cải thiện target task (MIMIC 67.7→68.5%, UR-FUNNY 63.3→65.7%).
  - **Giả định ngầm (điểm yếu):** ① mọi modality biểu diễn được thành **chuỗi** không mất thông tin; ② heterogeneity bắt trọn bởi modality-specific embeddings; ③ connections/interactions **chia sẻ** giữa modality/tác vụ.

---

## 5b. CO-LEARNING ⭐⭐
**Định nghĩa:** chuyển thông tin từ **modality phụ (secondary) → modality chính (primary)** bằng cách **chia sẻ không gian biểu diễn**. Modality phụ **CHỈ có lúc train** (test chỉ dùng modality chính).

### 5b.1. Co-learning via Representation
- **Representation coordination** (nhắc lại Cụm C): dùng không gian **word embedding** cho **zero-shot visual classification** (Socher 2013) — **test chỉ dùng ảnh** → zero-shot. Scale: **ALIGN** (Jia 2021, noisy text supervision).
- **Foundations of Co-learning (Zadeh 2020):** train **multimodal** nhưng **test chỉ dùng text** (điền 0 cho modality thiếu) → **co-learning đa thể thức > học chỉ text**.

### 5b.2. Co-learning via Generation ⭐
- **Định nghĩa:** dùng modality phụ làm **mục tiêu sinh (generation target)**.
- **Found in Translation (Pham 2019):** vấn đề — nếu cần cả 2 modality lúc test → nhạy cảm với visual thiếu/nhiễu. Giải: **cyclic translation** (dịch text→visual→text lúc train) → **test chỉ cần text**, robust. Cyclic để đảm bảo **cả hai modality được dùng**.
- **Vokenization (Tan & Bansal 2020):** dự đoán ảnh từ ngôn ngữ tương ứng ("voken" = visual token) + **masked language modeling** → **test chỉ dùng text**, co-learning > chỉ text.
- **Shaping visual representations with language** (few-shot classification).
- ⚠️ **Co-learning không phải lúc nào cũng hiệu quả** (Yun 2021): vision-language pretraining cải thiện **rất ít** trên lexical grounding / semantic role labeling / physical commonsense QA.

---

## 5c. MODEL INDUCTION ⭐⭐
**Định nghĩa:** giữ các **model đơn thể thức RIÊNG BIỆT** nhưng **cảm ứng hành vi chung** giữa chúng.
- **Giả định multi-view redundancy:** lý tưởng `X1 ⊥ X2 | Y` ⟺ `I(X1; X2 | Y) = 0` (hai view độc lập có điều kiện cho nhãn) + **sufficiency** (mỗi view đủ dự đoán Y nếu đủ data).

### 5c.1. Self-training (khởi động, 1 view)
- Train `f1` trên data có nhãn → dùng `f1` **pseudo-label** các mẫu **tự tin nhất** trong data không nhãn → thêm vào tập nhãn → lặp. **Then chốt:** ① không label hết 1 lần (sẽ chỉ ra classifier gốc); ② chuỗi pseudo-label dịch dần biên; ③ **input consistency regularization** (điểm giống nhau → nhãn giống nhau; qua augmentation/noise).

### 5c.2. Co-training (Blum & Mitchell 1998) ⭐
- **2 view `x1, x2` + 2 classifier**; ít data có nhãn `(x1,x2,y)`, nhiều data không nhãn.
- **Giả định:** ① mỗi view **đủ** để dự đoán nhãn một mình; ② hai view **độc lập** nhất có thể (mẫu `f1` tự tin mà `f2` không, và ngược lại).
- **Thuật toán:** `f1` pseudo-label mẫu tự tin → thêm vào tập train của `f2`; `f2` pseudo-label → thêm vào tập train của `f1`; lặp. Test: **ensemble** `f1(x1)` và `f2(x2)`. → data từ view kia **bổ sung không gian nhãn**; hai view phải **đồng thuận** (input consistency) → cross-view pseudo-labeling.
- **VD kinh điển:** phân loại trang web — `x1` = text trang, `x2` = text hyperlink trỏ vào.
- **Ứng dụng gần đây:** co-training RGB↔optical flow (Han 2020 — positive khó tìm ở RGB dễ tìm ở flow); co-training cho LLM prompting.

### 5c.3. Co-regularization
- Thêm số hạng loss ép hai model đồng thuận: `L = (f1(X1) − f2(X2))²`. → **nhắc lại representation coordination** (Sridharan & Kakade 2008).

---

## SO SÁNH 3 SUB-CHALLENGE ⭐
| | Model | Modality phụ lúc test? | Cơ chế |
|---|---|---|---|
| **Transfer** | dùng model **pretrained** làm khởi tạo | — | tham số `θ*` |
| **Co-learning** | 1 model, **chia sẻ không gian biểu diễn** | **không** (chỉ lúc train) | representation/generation |
| **Model Induction** | **nhiều model riêng biệt** | — | cảm ứng chéo (self/co-training, co-reg) |

## THÁCH THỨC MỞ
- Low-resource (ít data downstream, thiếu paired data, robustness); **beyond redundancy/joint information** (giới hạn transfer); modality có SOTA encoder không phải deep learning (tabular); domain adaptation/shift; interpretability. Core: **representation, alignment, reasoning**.

---

## 🎯 CÂU HAY RA THI (Cụm H)
1. 3 sub-challenge của Transference? Modality chính là modality nào (yếu/nhiễu/ít tài nguyên).
2. Trong co-learning, modality phụ có mặt lúc nào? (chỉ lúc train, test chỉ dùng modality chính).
3. Socher 2013 zero-shot: test dùng gì? Co-learning via representation vs via generation khác gì?
4. Cyclic translation (Pham 2019) giải quyết vấn đề gì? Vokenization là gì?
5. Model induction giả định gì? (`I(X1;X2|Y)=0`, multi-view redundancy + sufficiency).
6. Self-training vs Co-training: số view, cơ chế pseudo-label chéo?
7. 2 giả định của co-training (Blum & Mitchell)? Co-regularization dùng loss gì?
8. HighMMT/Gato dùng thành phần gì để thống nhất modality? 3 giả định ngầm?
