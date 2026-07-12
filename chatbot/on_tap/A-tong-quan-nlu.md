# A — Tổng quan Chatbot & Hiểu ngôn ngữ tự nhiên (NLU)

> Bài 1 (Tổng quan) + Bài 2 (NLU). Nền tảng cho toàn khoá. ⇐ [ONE-PAGER](00-ONE-PAGER.md)

---

## 1. Chatbot là gì & ứng dụng
**Chatbot** = phần mềm giao tiếp với con người bằng **ngôn ngữ tự nhiên** qua messaging/web/mobile/điện thoại.
Ứng dụng: chăm sóc khách hàng (FAQ, tra đơn), bán hàng, hỏi đáp tài liệu nội bộ, giáo dục, ngân hàng–tài chính, y tế (đặt lịch, nhắc thuốc), giải trí.

## 2. Phân loại chatbot (RẤT hay ra thi)

### 2.1 Theo cơ chế
| Loại | Cơ chế | Ví dụ |
|---|---|---|
| **Rule-based** | Kịch bản cố định, `IF keyword THEN reply`. Không học từ dữ liệu mới | Bot hỗ trợ đơn giản |
| **Frame-based** | Tạo **frame** (khung), điền **slot** khi user trả lời; frame đầy → thực hiện action; không hỏi lại slot đã có | Bot đặt vé máy bay |
| **AI-based** | ML + NLP, phản hồi linh hoạt, tự động | ChatGPT, Bard |

### 2.2 AI-based chia 2 nhánh lớn
- **Retrieval-based**: **chọn** câu trả lời từ tập có sẵn. 3 kiểu:
  - **NLP-based Retrieval**: intent detection + slot filling + truy xuất CSDL.
  - **Search-based Retrieval**: dùng công cụ tìm kiếm trên kho tài liệu/CSDL.
  - **Knowledge-based Retrieval**: tìm trong **Knowledge Base / Knowledge Graph**.
- **Generative-based**: **sinh** câu trả lời bằng LLM (GPT, LLaMA, T5). Các dạng:
  - General (ChatGPT, Gemini) · Fine-tuned (MedGPT, BioBERT) · **RAG** · Multi-modal (GPT-4V, Gemini, ImageBind) · Personalized (Google Assistant, Alexa).

> **Bẫy:** Retrieval-based = **chọn**; Generative = **sinh mới**. RAG là một dạng generative có bổ sung truy xuất.

## 3. Các bước xây dựng chatbot hiệu quả
1. **Phân tích mục tiêu**: người dùng là ai, chatbot để làm gì (bán hàng/tư vấn/thu thập dữ liệu), kênh giao tiếp (FB/Zalo/web).
2. **Lựa chọn loại chatbot**: menu/button · dựa trên từ khoá · trò chuyện theo ngữ cảnh.
3. Xây dựng kịch bản → 4. Cài đặt & tích hợp đa kênh → 5. Thử nghiệm & đánh giá (khối lượng công việc, tốc độ, nhận diện đa ý định/cảm xúc, tỷ lệ phản hồi/quay lại, tỷ lệ chuyển đổi).

## 4. Các vấn đề trong quản lý hội thoại (dialogue management)
1. **Câu của user không phải luôn là câu hỏi** (chào, khen/chê, khiếu nại…).
2. **Câu liên quan tới hội thoại trước** ("phim thứ hai", "cái đó") → **lưu context/session**, tách & lưu entity/intent theo session, **tóm tắt** nếu quá dài, kết hợp CSDL khách hàng.
3. **User nhảy chủ đề / đổi ý** → cần **State Management**.
4. **User nhập thiếu thông tin** → chatbot hỏi lại, nhớ thông tin trước.
5. **Câu nhiều dòng bị hiểu nhầm đã hoàn thành** → kiểm tra câu hoàn chỉnh: câu ngắn (<5 từ)/không có động từ/kết bằng "và","nhưng" → **đợi thêm**; gộp nhiều tin nhắn liên tiếp; kết thúc bằng `. ? !` → xác nhận hoàn chỉnh; dùng Intent Classification phát hiện câu chưa xong.

## 5. Nền tảng phát triển chatbot
- **Không cần lập trình**: Google **Dialogflow**, IBM **Watson Assistant**, Facebook **Wit.ai**, Amazon **Lex** (hỗ trợ Intent/Slot Detection, tích hợp Messenger/Telegram/Web).
- **Cần lập trình (mã nguồn mở)**: Microsoft Bot Framework SDK, **Rasa**.
- **Generative open-source**: **LangChain** (RAG, memory, tool use), **Haystack** (RAG + Elasticsearch/FAISS), **LlamaIndex** (RAG trên tài liệu tùy chỉnh), **Rasa Open Source**, Chatbot UI.

---

# NLU — Hiểu ngôn ngữ tự nhiên

## 6. Các bước hoạt động của chatbot
User nhập → **tiền xử lý** (lỗi chính tả, viết tắt) → **xác định intent** → **trích entity/slot** → xử lý & trả lời.
> VD: "Đặt vé đi Hà Nội sáng mai" → intent=Đặt vé; entities: destination=Hà Nội, time=sáng mai.

## 7. Nhận diện ý định (Intent Detection)
Vai trò: hiểu yêu cầu, điều hướng chatbot đến chức năng phù hợp. Intent phổ biến: chào hỏi, đặt lịch, yêu cầu thông tin (what/why/who/when/how/yes-no), khen/chê, khiếu nại, kết thúc.

**3 tầng phương pháp:**
1. **Rule-based**: định nghĩa intent bằng keyword. Ưu: đơn giản, dễ kiểm soát. Nhược: kém linh hoạt.
2. **Machine Learning**: vector hoá câu (**BoW, TF-IDF, word2vec, BERT sentence embedding**) + classifier (**SVM, Random Forest, Logistic Regression, Naive Bayes**). Cần dữ liệu gán nhãn.
3. **Deep Learning**: RNN/LSTM/GRU, **BERT/PhoBERT** → tốt hơn ML truyền thống.

**Bộ dữ liệu Intent:** ATIS (18+, vé máy bay) · SNIPS (7) · **CLINC150** (150 intent) · BANKING77 (77) · MASSIVE (đa ngôn ngữ, 1tr+) · **Zalo AI 2020** (7, tiếng Việt).

**Các vấn đề khó với intent:** câu phức, từ viết tắt đa nghĩa, nhiều giá trị cùng loại entity, 2 entity cùng loại nhưng chỉ 1 là chính, câu ngắt quãng, câu dài nhiều thuộc tính, **câu nhiều intent**.

## 8. Nhận dạng thực thể (NER / Slot Filling)
Mục tiêu: trích thông tin → điền slot. Cần dữ liệu gán nhãn **BIO** + hậu xử lý từ đồng nghĩa (SFO ↔ San Francisco).

**Nhãn BIO:** `B-` (Begin, bắt đầu thực thể), `I-` (Inside, bên trong), `O` (Outside, ngoài).
> "đi **Đà Nẵng** lúc **7 giờ sáng**" → `B-LOC I-LOC` … `B-TIME I-TIME I-TIME`.

**Cách tiếp cận:**
- Rule-based (GATE).
- **ML**: CRF, SVM — đặc trưng **thủ công**.
- **Deep Learning**: **BiLSTM + CRF** (tự sinh đặc trưng từ embedding; có char-level representation) hoặc **BERT + Softmax/CRF**. VLSP2016 F1≈88.59%.

**Dataset NER:** EN — CoNLL-2003 (PER/LOC/ORG/MISC), OntoNotes 5.0 (18 loại), WNUT-17, ACE 2005, WikiANN. VN — **VLSP 2016/2018**, UIT-ViNERT, **PhoNER_COVID19**, ViNewsNER, ViHealthNER.

**JointIDSF (Joint Intent Detection and Slot Filling)** — mô hình học **chung**:
1. Vector `[CLS]` dự đoán **intent** (softmax).
2. Tạo **soft intent embedding** = Σ (xác suất intent × embedding intent).
3. **Attention** giữa soft intent embedding và từng token → điều chỉnh token vector.
4. Slot decoder dùng **CRF** gán nhãn slot.
> Ý nghĩa: intent và slot **bổ trợ nhau** → học chung tốt hơn học riêng.

## 9. Phân tích cảm xúc trong hội thoại
Các cấp: từng câu · toàn hội thoại · **theo khía cạnh** (aspect: "phim hay nhưng âm thanh dở") · **theo đối tượng** · **phát hiện thay đổi cảm xúc** · **theo từng người nói**.
Cách tiếp cận: Rule (từ điển cảm xúc) · ML (BoW/TF-IDF + SVM/Naive Bayes) · DL (CNN, LSTM, **BiLSTM+Attention**, BERT/PhoBERT/RoBERTa) · **Zero/Few-shot** (GPT, T5, LLaMA + prompt).

## 10. Nâng cao chất lượng chatbot với LLM (5 nhóm — hay ra thi)

### 10.1 Fine-tuning vs Instruction-tuning ⭐
| | **Fine-tuning** | **Instruction-tuning** |
|---|---|---|
| Mục tiêu | 1 **tác vụ cụ thể** | hiểu & làm theo **chỉ dẫn**, đa tác vụ qua prompt |
| Dữ liệu | cặp **input → output** | cặp **instruction → output** |
| Kích thước model | **nhỏ–vừa (100M–7B)**, VD BERT-base 110M, LLaMA-7B | **lớn (7B–70B+)**, VD FLAN-T5-XXL 11B, LLaMA-13/30/70B |
| Chi phí | thấp, ít tài nguyên | cao, tốn GPU |
| Ưu | nhanh, hiệu quả cho task cụ thể | đa năng, 1 model nhiều task |
| Nhược | phải train riêng từng task | cần dữ liệu chỉ dẫn đa dạng |

> Model **càng lớn càng hiểu chỉ dẫn tốt**. Dataset: SQuAD, QuAC, Natural Questions, DSTC, TriviaQA, CoQA, TREC, MultiWOZ.

### 10.2 Prompt Engineering
Thiết kế câu lệnh mẫu; hướng dẫn phân tích intent/entity; điều chỉnh phong cách; tối ưu hội thoại đa lượt.
Kỹ thuật: **Zero-shot** (không ví dụ) · **One-shot** (1 ví dụ) · **Few-shot** (nhiều ví dụ) · **Chain-of-Thought** (suy luận từng bước).

### 10.3 Context-aware
Ghi nhớ lượt trước: **session history** · **sliding window** (giới hạn độ dài prompt) · **tóm tắt ngữ cảnh** (T5/BART/LLM) · **Dialogue State Tracking (DST)** (lưu slot đã điền).

### 10.4 RAG (giới thiệu ngắn — chi tiết ở [C-qa-rag](C-qa-rag.md))
**Document Store** (tri thức) → **Retriever** (tìm đoạn liên quan) → **Generator** (LLM sinh câu trả lời từ đoạn truy xuất). Prompt = câu hỏi + đoạn truy xuất.

### 10.5 Adapter-based & Data Augmentation
- **Adapter**: fine-tuning nhẹ, chỉ train vài layer chèn thêm, **giữ nguyên trọng số gốc** → tiết kiệm bộ nhớ/thời gian. Thư viện: HuggingFace **PEFT**, AdapterHub. **LoRA (Low-Rank Adapter)** = bản tối ưu hơn.
- **Data Augmentation**: tạo dữ liệu mới → giảm overfitting, tăng tổng quát hoá. Cách: **Paraphrasing** · **Back-translation** (dịch qua-lại) · Template-based · **Entity swapping** · Synthetic generation bằng LLM.

---
## ✅ Chốt nhanh mục A
- Rule vs Frame vs AI (Retrieval/Generative); Retrieval 3 kiểu (NLP/Search/Knowledge).
- NLU = Intent + NER(BIO) + Sentiment; mỗi cái Rule→ML→DL.
- JointIDSF: soft intent embedding + attention + CRF.
- Fine-tuning (nhỏ, 1 task) vs Instruction-tuning (lớn, đa task).
- Adapter/LoRA = PEFT; Augmentation = paraphrase/back-translation/entity-swap.
