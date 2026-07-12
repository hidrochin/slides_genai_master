# Trắc nghiệm A — Tổng quan Chatbot & NLU

> Lý thuyết: [on_tap/A-tong-quan-nlu](../on_tap/A-tong-quan-nlu.md). Đáp án cuối file.

---

**1.** Chatbot dùng frame để lưu thông tin và điền vào từng slot cho đến khi đủ để thực hiện hành động thuộc loại:
A. Rule-based  B. Frame-based  C. Generative  D. Retrieval-based

**2.** Điểm khác biệt cốt lõi giữa retrieval-based và generative-based chatbot là:
A. Retrieval **chọn** câu trả lời có sẵn, generative **sinh** câu trả lời mới
B. Retrieval dùng LLM, generative dùng rule
C. Retrieval nhanh hơn nên chính xác hơn
D. Không có khác biệt về nguyên lý

**3.** Kiểu retrieval-based chatbot tìm câu trả lời trong Knowledge Base / Knowledge Graph là:
A. NLP-based  B. Search-based  C. Knowledge-based  D. Frame-based

**4.** RAG chatbot thuộc nhóm nào?
A. Rule-based  B. Retrieval-based thuần  C. Generative-based  D. Frame-based

**5.** Khi user viết câu hỏi trên nhiều dòng, giải pháp KHÔNG phù hợp để tránh trả lời sớm là:
A. Đợi thêm nếu câu ngắn (<5 từ), không có động từ, kết bằng "và/nhưng"
B. Gộp nhiều tin nhắn liên tiếp trước khi xử lý
C. Trả lời ngay khi nhận dòng đầu tiên để phản hồi nhanh
D. Xác nhận hoàn chỉnh nếu kết bằng `. ? !`

**6.** Ba tác vụ lõi của NLU trong chatbot là:
A. Intent detection, NER/slot filling, sentiment analysis
B. Tokenize, stemming, lemmatization
C. Retrieval, ranking, generation
D. Chunking, embedding, indexing

**7.** Trong gán nhãn BIO cho "đi **Đà Nẵng**", nhãn của từ "Đà" và "Nẵng" là:
A. B-LOC, B-LOC  B. B-LOC, I-LOC  C. I-LOC, I-LOC  D. O, B-LOC

**8.** Phương pháp DL phổ biến nhất cho NER (slot filling) trong slide là:
A. Naive Bayes  B. BM25  C. BiLSTM + CRF  D. K-means

**9.** Trong JointIDSF, vector nào được dùng để dự đoán intent?
A. Vector `[CLS]`  B. Vector token cuối  C. Trung bình tất cả token  D. Vector `[SEP]`

**10.** JointIDSF dùng cơ chế nào để slot decoder gán nhãn cuối cùng?
A. Softmax thuần  B. CRF  C. K-NN  D. Regex

**11.** So với instruction-tuning, fine-tuning KHÁC ở điểm:
A. Dùng model lớn hơn (70B+)
B. Nhắm 1 tác vụ cụ thể, dữ liệu input→output, model nhỏ-vừa
C. Đa năng cho nhiều tác vụ qua prompt
D. Dùng cặp instruction→output

**12.** Instruction-tuning thường dùng cỡ model nào?
A. 100M–500M  B. 1B–3B  C. 7B–70B+  D. dưới 100M

**13.** Kỹ thuật fine-tuning nhẹ chỉ train vài layer chèn thêm, giữ nguyên trọng số gốc:
A. Full fine-tuning  B. Adapter / LoRA  C. Distillation  D. Quantization

**14.** Thư viện HuggingFace hỗ trợ parameter-efficient fine-tuning là:
A. PEFT  B. FAISS  C. spaCy  D. NLTK

**15.** Kỹ thuật data augmentation dịch câu sang ngôn ngữ khác rồi dịch ngược lại:
A. Paraphrasing  B. Back-translation  C. Entity swapping  D. Template-based

**16.** Dialogue State Tracking (DST) trong context-aware nhằm:
A. Nén ngữ cảnh  B. Lưu lại các slot đã được điền  C. Dịch câu hỏi  D. Xếp hạng tài liệu

**17.** Vector hoá câu bằng "Bag of Words, TF-IDF, word2vec, BERT" rồi phân loại bằng SVM/Naive Bayes là hướng:
A. Rule-based  B. Machine Learning  C. Deep Learning thuần  D. Zero-shot

**18.** Bộ dữ liệu intent tiếng Việt được nhắc trong slide:
A. ATIS  B. SNIPS  C. CLINC150  D. Zalo AI 2020

**19.** Prompt engineering với "1 ví dụ mẫu rồi hỏi câu mới" là dạng:
A. Zero-shot  B. One-shot  C. Few-shot  D. Chain-of-thought

**20.** Trong RAG cơ bản, thành phần "tạo câu trả lời dựa trên đoạn văn truy xuất" là:
A. Document Store  B. Retriever  C. Generator  D. Indexer

---
### Đáp án
1-B · 2-A · 3-C · 4-C · 5-C · 6-A · 7-B · 8-C · 9-A · 10-B · 11-B · 12-C · 13-B · 14-A · 15-B · 16-B · 17-B · 18-D · 19-B · 20-C
