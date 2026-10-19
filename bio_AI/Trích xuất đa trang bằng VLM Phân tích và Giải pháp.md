# Trích xuất hóa đơn đa trang bằng VLM: Phân tích và Giải pháp

Oct 20, 2026 · @hydrochii

## Tóm tắt điều hành

Cả hai lỗi đều có chung một gốc: hệ thống đang giao cho mô hình những việc nó làm kém (đếm ký tự, tự phán định format, tự báo độ tin cậy, quyết định khi thiếu ngữ cảnh toàn tài liệu). Hướng giải là **để VLM hiểu bố cục, để OCR và code đảm bảo độ chính xác ký tự và logic gộp**.

| Vấn đề | Triệu chứng | Nguyên nhân gốc | Giải pháp chính |
| --- | --- | --- | --- |
| 1. Mã code 4-6 bị đếm thành 4-7 | Chunk (1,2) chạy riêng thì đúng, chạy song song với chunk (3) thì trả rỗng | Batch khác nhau làm logits lệch nhỏ (FP8, chunked prefill); mô hình tự đếm ký tự nên quyết định nằm sát ranh giới, dễ lật | Mô hình chỉ liệt kê mã nguyên văn; code lọc bằng regex và đối chiếu OCR; logprobs + đọc lại vùng crop cho chỗ lưỡng lự |
| 2. Quantity tổng hợp ở trang cuối | Lấy nhầm quantity của bảng ở trang 2 thay vì bảng tổng hợp ở trang 3 | Mọi chunk trả về cùng một field `quantity` không có vai trò; chunk không biết vị trí trang; gộp theo confidence tự báo (cùng 0.95) | Gắn `role` cho từng quantity; chèn "Trang k/N"; gộp bằng luật và kiểm tra grand total = tổng các bảng; luồng toàn cục song song |

Mục tiêu ràng buộc: giữ trên 1 GPU L40, độ chính xác ưu tiên, latency tổng không vượt quá xa một lượt (không chấp nhận gấp đôi).

## Bối cảnh hệ thống hiện tại

Hệ thống trích xuất khoảng 10+ trường từ hóa đơn do nhiều đối tác thứ ba tổng hợp, mỗi đối tác một layout riêng; vì vậy VLM là bắt buộc để hiểu bố cục.

| Hạng mục | Hiện trạng |
| --- | --- |
| Mô hình | Qwen 3.6 35B-A3B (MoE), FP8, dùng chung cho VLM và LLM |
| Phần cứng | 1 GPU L40 48GB |
| Serving | vLLM (image latest), `max_model_len` ≈ 24.000, `gpu_memory_utilization` ≈ 0.9, bật prefix caching và chunked prefill |
| Render ảnh | pypdfium2, khoảng 300 DPI |
| Chunking | 2 trang/chunk, các chunk gửi song song, không overlap |
| Decoding | temperature 0, top\_p 0.1, không bật thinking mode (chậm) |
| Ép output | Prompt + xgrammar (JSON schema) |
| Kỹ thuật hiện có | Field `reason` bắt mô hình liệt kê mọi mã trong một dòng ảo trước khi chọn |
| Gộp kết quả | Field rỗng được điền từ chunk khác; field trùng lấy theo confidence tự báo |
| OCR phụ trợ | YoloX trên Triton, trả text + bounding box; nhanh nhưng yếu hơn Qwen về nhận diện ký tự |
| Độ dài tài liệu | Thường 3–5 trang; đột biến 20, 30, 40 trang |

**Đặc điểm dữ liệu quan trọng:**

- Mã code cần lấy theo format `XXXX-XXXXXX` (4-6), nằm trong một **dòng ảo** của bảng (một dòng ảo gồm nhiều dòng vật lý). Cùng dòng có các mã khác không theo luật 4-6, không cần lấy. Dòng ảo có thể vắt qua hai trang.
- Hóa đơn gồm nhiều bảng nối tiếp; cuối mỗi bảng có quantity tổng của bảng đó. Sau bảng cuối cùng có **một bảng tổng hợp nhỏ** cộng dồn quantity của mọi bảng. Đây là giá trị cần lấy.
- Bảng mã code trả về dạng JSON theo dòng; tài liệu nhiều dòng làm output dài.

## Vấn đề 1: Mã code bị đếm thành 4-7 khi chạy song song

Kết luận: hai request song song **không nhìn thấy nội dung của nhau**; trang 3 không "làm nhiễu" trang 1–2. Kết quả đổi vì **số học thay đổi theo batch**, và quyết định của mô hình nằm sát ranh giới vì nó đang phải tự đếm ký tự.

### Hiện tượng

- Gửi chunk (1,2) một mình: mô hình ghi `1234-567812 (4-6)` và trả đúng.
- Gửi chunk (3) một mình: đúng.
- Gửi tài liệu 3 trang (chunk (1,2) và (3) song song): mô hình ghi `(4-7)` cho cùng mã đó và trả rỗng.
- Lặp lại cùng một kịch bản nhiều lần: kết quả giống hệt nhau. Điều này chỉ chứng tỏ **cùng tải thì cùng kết quả**, không chứng tỏ ổn định khi tải đổi.

### Nguyên nhân 1: không tất định theo batch

1. vLLM gom các request đang chạy vào cùng batch. Chạy một mình và chạy cùng chunk (3) cho kích thước ma trận khác nhau.
2. Kernel GEMM/attention có thể chọn cách chia tile và thứ tự cộng dồn khác nhau; chunked prefill chia prompt khác nhau tùy tải.
3. Phép cộng số thực không có tính kết hợp tuyệt đối; với FP8, sai số làm tròn càng lớn.
4. Logits lệch rất nhỏ. Ở token mà hai lựa chọn gần ngang nhau, greedy decoding (temperature 0) chọn khác, và toàn bộ phần sinh sau đó rẽ hướng.

### Nguyên nhân 2: mô hình đang tự đếm ký tự

- Tokenizer cắt `567812` thành các mảnh nhiều chữ số (ví dụ `567` + `812`), nên mô hình không "thấy" từng chữ số riêng lẻ. Đếm ký tự là điểm yếu kinh điển của LLM.
- Phép đếm `(4-6)` vốn đã là quyết định xác suất sát ranh giới. Chỉ cần nhiễu số học nhỏ ở nguyên nhân 1 là nó lật thành `(4-7)`.
- Field `reason` giúp mô hình nhìn kỹ hơn (đúng hướng), nhưng **bước phán định cuối vẫn dựa vào khả năng đếm**, nên vẫn mong manh.

### Yếu tố khuếch đại: 300 DPI

Trang A4 ở 300 DPI là khoảng 2480×3508 pixel. Với họ Qwen-VL, mỗi visual token ứng với khoảng 32×32 pixel, tức xấp xỉ 8.000+ token/trang nếu processor không resize. Hai trang khoảng 17.000 token, sát `max_model_len` 24.000, chưa kể prompt và output JSON dài. Context dày visual token làm độ chính xác chi tiết giảm và tăng độ nhạy với nhiễu. Cần log `prompt_tokens` thực tế để xác nhận.

### Thí nghiệm xác nhận

- [ ] Gửi chunk (1,2) song song với một request text bất kỳ không liên quan. Nếu ra `(4-7)`: nguyên nhân là batch composition, không phải nội dung trang 3.
- [ ] Bật chế độ batch-invariant của vLLM (biến môi trường `VLLM_BATCH_INVARIANT`, kiểm tra docs phiên bản đang dùng) và chạy lại. Lỗi biến mất là xác nhận.
- [ ] Log `prompt_tokens` và `finish_reason` của từng request.

## Vấn đề 2: Quantity tổng hợp nằm ở trang cuối

Kết luận: lỗi không nằm ở khả năng đọc mà ở **thiết kế schema và logic gộp**. Mỗi chunk trả về cùng một field `quantity` mang cùng ý nghĩa, nên lúc gộp không có thông tin nào để phân biệt quantity của một bảng với quantity tổng hợp.

### Ví dụ

| Trang | Nội dung | Quantity | Cần lấy? |
| --- | --- | --- | --- |
| 2 | Tổng bảng 1 | 1000 | Không |
| 2 | Tổng bảng 2 | 2000 | Không |
| 3 | Bảng tổng hợp cuối tài liệu | 3000 | **Có** |

Chunk (1,2) trả 2000 (hoặc 1000), chunk (3) trả 3000, cả hai đều tự báo confidence 0.95. Logic gộp không có căn cứ để chọn.

### Bốn nguyên nhân

1. **Field không có vai trò.** Schema chỉ có `quantity`, không phân biệt tổng bảng với tổng hợp toàn tài liệu.
2. **Chunk không biết vị trí trang.** Ảnh được gửi theo danh sách nhưng prompt không ghi "đây là trang 3/3, trang cuối". Chunk (1,2) không biết còn trang sau; chunk (3) không biết mình là cuối.
3. **Confidence tự báo vô nghĩa.** Con số 0.95 do mô hình viết ra như một token bình thường, không phản ánh xác suất thật, nên không dùng để phân xử được.
4. **Chunking không overlap, không có góc nhìn toàn cục.** Không request nào thấy đủ cấu trúc "các bảng → bảng tổng hợp" để nhận ra đâu là giá trị cuối cùng.

### Điểm mạnh có thể khai thác

Cấu trúc dữ liệu tự chứa một **bất biến kiểm tra được**: quantity tổng hợp phải bằng tổng các quantity của từng bảng (trong ví dụ trên: 1000 + 2000 = 3000). Bất biến này không phụ thuộc layout của đối tác nào, nên dùng làm phép kiểm tra chéo mà không cần hardcode.

## Đánh giá hướng OCR → LLM sửa lỗi → index RAG → LLM trích xuất

Kết luận: **không dùng làm pipeline chính**. Layout đa dạng giữa các đối tác đòi hỏi VLM nhìn ảnh; bước sửa lỗi bằng text còn có rủi ro bịa ký tự. Tuy vậy, hai ý tưởng con của hướng này rất có giá trị khi đặt đúng chỗ: **ID cho dòng OCR** và **RAG theo đối tác**.

| Thành phần | Đánh giá | Lý do | Giữ lại dưới dạng |
| --- | --- | --- | --- |
| LLM text-only thay VLM | Không phù hợp | Lệch cột, bảng không kẻ khung, dòng ảo nhiều dòng vật lý: chỉ dựa vào tọa độ dễ gom sai; layout mỗi đối tác một kiểu | VLM vẫn là trung tâm |
| LLM sửa lỗi OCR chỉ bằng text | Rủi ro cao | Mã code là chuỗi tùy ý, không có ngữ cảnh ngôn ngữ. OCR mất một chữ số thì LLM không có ảnh không thể khôi phục, và có thể **bịa thêm chữ số cho đủ format**, vượt qua cả regex | VLM đọc lại vùng crop độ phân giải cao |
| RAG theo embedding trên nội dung tài liệu | Không cần (3–5 trang) | Text OCR 3–5 trang vừa một request. Retrieval cắt vụn cấu trúc, đúng thứ vấn đề 2 cần | Chia theo cấu trúc cho tài liệu dài |
| Gắn ID cho từng dòng OCR | Rất tốt | LLM/VLM trả về ID thay vì chép chữ số, code lấy giá trị gốc; output ngắn, truy vết được | Input lai ảnh + text OCR có ID |
| RAG theo đối tác | Rất tốt | Layout khác nhau giữa đối tác nhưng gần như cố định trong cùng đối tác | Hồ sơ đối tác + few-shot tự động |

Nguyên tắc rút ra: **thông tin đã mất ở bước OCR chỉ lấy lại được từ ảnh, không lấy lại được từ text.**

## Kiến trúc đề xuất

VLM vẫn là trung tâm để hiểu bố cục đa dạng của các đối tác; OCR và code đảm nhận độ chính xác ký tự và logic gộp. Hai luồng A và B chạy song song nên latency xấp xỉ lượt dài hơn, không cộng dồn.

&#91;embedded content: pipeline lai VLM + OCR · 2 luồng song song, kiểm tra bằng code\]

Bước đọc lại crop chỉ chạy cho field lưỡng lự; bản đồ của luồng B quyết định giá trị nào là grand total khi gộp.

## Giải pháp chi tiết

Tám giải pháp dưới đây độc lập với nhau, có thể triển khai dần; mỗi giải pháp ghi rõ vấn đề nó giải quyết.

### G1. Mô hình chỉ trích xuất, code kiểm tra format (vấn đề 1)

- Schema yêu cầu mỗi dòng ảo trả về `all_codes_in_row`: danh sách **mọi** mã nhìn thấy, chép nguyên văn. Mô hình không đếm, không chọn.
- Code Python lọc bằng regex `^\d{4}-\d{6}$` (hoặc pattern thật). Bước này tất định, không phụ thuộc batch.
- Không dùng xgrammar để ép regex vào field mã: mô hình sẽ bị buộc bịa đủ 6 chữ số khi đọc sai, và mất tín hiệu lỗi. Xgrammar chỉ dùng cho cấu trúc JSON.

### G2. Đối chiếu với OCR (vấn đề 1)

- Mã hợp lệ từ VLM phải khớp một chuỗi trong output OCR của cùng trang (có bbox).
- Khớp hoàn toàn: chấp nhận. Lệch 1–2 ký tự hoặc không tìm thấy: chuyển sang G4 (đọc lại crop), không tự quyết.
- Lưu ý: YoloX yếu hơn Qwen về ký tự, nên OCR là **bằng chứng đối chiếu**, không phải nguồn sự thật. Khi hai nguồn bất đồng, ảnh crop là trọng tài.

### G3. Logprobs thay confidence tự báo (vấn đề 1 và 2)

- Bật `logprobs` trong request vLLM. Với mỗi field quan trọng (mã code, quantity), lấy **logprob thấp nhất** trong các token của giá trị đó làm độ tin cậy.
- Logprob thấp đúng là tình huống "token sát ranh giới" gây lật kết quả ở vấn đề 1. Chỉ những field này đi vào G4.
- Bỏ field confidence do mô hình tự viết.

### G4. VLM đọc lại vùng crop (vấn đề 1)

- Dùng bbox OCR (hoặc vị trí dòng ảo) để crop đúng ô/dòng từ ảnh 300 DPI gốc.
- Gửi crop cho Qwen với yêu cầu "đọc chính xác chuỗi ký tự trong ảnh". Mỗi crop chỉ vài chục đến vài trăm visual token.
- Gom nhiều crop vào vài request song song. Với MoE A3B, bước này nhỏ so với lượt chính; cần đo trên dữ liệu thật.

### G5. Input lai: ảnh độ phân giải vừa + text OCR có ID (vấn đề 1)

- Gửi ảnh trang ở khoảng 150 DPI (hoặc đặt `max_pixels`) để VLM hiểu bố cục, kèm text OCR của trang với ID mỗi dòng: `[p2:L14] 1234-567812 AB-99 500`.
- Prompt: nhìn ảnh để hiểu cấu trúc; với mã và số, trả về ID dòng OCR chứa nó (hoặc chép lại để code đối chiếu với dòng đó).
- Lợi ích: VLM vẫn xử lý layout lạ; chữ số cuối cùng lấy từ nguồn được kiểm chứng; tổng token có thể giảm vì không cần 300 DPI cho toàn trang; output ngắn hơn với bảng nhiều dòng.

### G6. Schema `role` cho quantity, chèn "Trang k/N", gộp bằng luật (vấn đề 2)

1. Trước mỗi ảnh chèn text `Trang k/N` và thêm `(trang cuối của tài liệu)` khi k = N.
2. Mỗi chunk trả về **mọi** quantity kèm `role` ∈ {`line_item`, `table_total`, `grand_total`} và `page_num`. Định nghĩa vai trò theo ngữ nghĩa, không theo vị trí: grand\_total là bảng/ô tổng hợp nằm sau tất cả các bảng dữ liệu, cộng dồn quantity của nhiều bảng.
3. Thứ tự field: danh sách quantity có role đứng trước, kết luận đứng sau (mô hình sinh tuần tự, field trước là bước suy nghĩ cho field sau).
4. Luật gộp trong code:
   1. Có `grand_total`: lấy giá trị ở trang lớn nhất (vị trí thấp nhất trên trang).
   2. Không có: lấy `table_total` cuối cùng và đánh dấu review.
   3. Kiểm tra `grand_total == Σ table_total`. Khớp: tin cậy cao. Lệch: review hoặc chạy lại phần liên quan.

### G7. Luồng bản đồ tài liệu song song (vấn đề 2, tài liệu dài)

- **Luồng A** (như hiện tại, đã áp dụng G1–G6): chunk 1–2 trang, trích xuất chi tiết.
- **Luồng B** (chạy cùng lúc): toàn bộ tài liệu ở độ phân giải rất thấp, khoảng 300–600 token/trang. B không đọc chi tiết, chỉ lập bản đồ: mỗi trang có khối gì (bảng dữ liệu, dòng tổng bảng, bảng tổng hợp cuối, chữ ký) và bảng tổng hợp nằm ở trang/vùng nào.
- Khi gộp, bản đồ của B quyết định giá trị nào từ A là grand total; nếu cần, crop đúng vùng B chỉ ra để đọc lại.
- Latency ≈ max(A, B), không phải A + B. Tài liệu 20–40 trang: B chỉ nhận trang 1 và 3 trang cuối.

### G8. Hồ sơ đối tác (RAG theo đối tác)

1. Nhận diện đối tác từ trang 1 (mã số thuế, tên công ty qua regex trên OCR; hoặc embedding ảnh header thu nhỏ).
2. Mỗi đối tác có hồ sơ: 1–2 ví dụ đã xác minh (few-shot) và ghi chú bố cục, ví dụ "mã hàng ở dòng 2 của dòng ảo, cột 3; tổng hợp ở cuối trang cuối, nhãn 'Grand Total'".
3. Chèn hồ sơ vào prompt khi trích xuất.
4. Hồ sơ tạo **tự động**: khi người dùng xác nhận hoặc sửa một hóa đơn của đối tác, LLM sinh ghi chú bố cục từ ví dụ đó và lưu lại. Không hardcode; đối tác mới dùng prompt chung và tốt dần lên.

### Bổ sung: chunking và output

- **Overlap bằng dải ảnh:** ghép dải cuối trang trước (15–20% chiều cao) vào đầu chunk sau, ghi chú "chỉ là ngữ cảnh, không trích xuất lại". Khử trùng lặp theo `(mã, page_num)`.
- **Bảng dài:** chunk 1 trang/request cho phần bảng; kiểm tra `finish_reason == "length"` để phát hiện JSON bị cắt cụt.
- **Độ phân giải:** log `prompt_tokens`, thử 150–200 DPI hoặc `max_pixels`, so sánh trên golden set.
- **Batch-invariant mode:** dùng để debug và xác nhận nguyên nhân; không phải giải pháp production vì giảm throughput.

## Lộ trình triển khai

Bắt đầu bằng bộ đánh giá, sau đó là các thay đổi rẻ có tác động lớn (G6, G1, G2), rồi mới đến các thay đổi kiến trúc. Mỗi giai đoạn chỉ chuyển tiếp khi golden set cho thấy cải thiện và không có hồi quy.

| Giai đoạn | Việc | Giải quyết | Công sức | Tác động | Điều kiện chuyển tiếp |
| --- | --- | --- | --- | --- | --- |
| 0 | Golden set 100–200 hóa đơn + script đo độ chính xác theo field, theo đối tác; chạy các thí nghiệm xác nhận ở vấn đề 1 | Nền tảng | Trung bình | Bắt buộc | Có số liệu baseline |
| 1 | G6: "Trang k/N", schema `role`, gộp bằng luật, kiểm tra tổng | Vấn đề 2 | Thấp | Cao | Độ chính xác grand total tăng rõ |
| 1 | G1 + G2: liệt kê mã nguyên văn, lọc regex, đối chiếu OCR | Vấn đề 1 | Thấp | Cao | Hết lỗi đếm 4-7 trên golden set |
| 2 | G3 + G4: logprobs, đọc lại crop cho field lưỡng lự | Vấn đề 1 | Trung bình | Trung bình–cao | Latency p95 tăng trong ngưỡng chấp nhận |
| 2 | Tinh chỉnh DPI/`max_pixels`, overlap dải ảnh, chunk 1 trang cho bảng dài | Cả hai | Thấp | Trung bình | Không giảm độ chính xác, giảm token |
| 3 | G5: input lai ảnh + text OCR có ID | Vấn đề 1, bảng dài | Trung bình | Cao | So sánh A/B với giai đoạn 2 |
| 3 | G7: luồng bản đồ tài liệu song song | Vấn đề 2, tài liệu dài | Trung bình | Trung bình | Cải thiện trên nhóm 20–40 trang |
| 4 | G8: hồ sơ đối tác + few-shot tự động | Bền vững | Cao | Cao theo thời gian | Có luồng xác nhận từ người dùng |

**Việc cần đo trước giai đoạn 3:** tỷ lệ YoloX đọc đúng nguyên văn mã code. Nếu trên khoảng 95%, G5 rất mạnh. Nếu thấp hơn nhiều, G4 sẽ chạy thường xuyên; khi đó cân nhắc cho VLM đọc crop toàn bộ ô mã code.

## Đo lường, đánh giá và rủi ro

Mọi thay đổi prompt, DPI, chunking hay schema đều phải chạy lại trên golden set; không có bộ này thì sửa một ca sẽ làm hỏng ca khác mà không biết.

### Golden set

- 100–200 hóa đơn có nhãn đúng, phủ các đối tác chính và các ca khó: tài liệu 3 trang, quantity xuất hiện ở nhiều trang, dòng ảo vắt qua trang, tài liệu 20–40 trang.
- Chạy mỗi tài liệu ở **hai chế độ tải**: một mình và cùng nhiều request khác, để bắt lỗi kiểu vấn đề 1.

### Chỉ số theo dõi

| Chỉ số | Cách đo |
| --- | --- |
| Độ chính xác theo field | Khớp tuyệt đối với nhãn, tách theo đối tác |
| Độ chính xác bảng mã code | Precision / recall theo dòng ảo |
| Độ ổn định theo tải | Tỷ lệ tài liệu có output khác nhau giữa chạy đơn và chạy song song |
| Tỷ lệ qua kiểm tra tổng | Tỷ lệ grand total = Σ table total |
| Tỷ lệ cần đọc lại crop | Số field logprob thấp hoặc OCR bất đồng / tổng số field |
| Tỷ lệ JSON bị cắt | `finish_reason == "length"` |
| Latency | p50 và p95 theo nhóm số trang (3–5, 6–19, 20–40) |
| Token | `prompt_tokens` trung bình mỗi trang |

### Rủi ro và cách giảm

| Rủi ro | Cách giảm |
| --- | --- |
| YoloX đọc sai ký tự nhiều, G2/G5 kém hiệu quả | Đo trước ở giai đoạn 0; ảnh crop là trọng tài, không tin OCR một chiều |
| Bảng không kẻ khung, ô gộp, checkbox, mộc đỏ | VLM vẫn nhìn ảnh; khi kiểm tra chéo thất bại, fallback sang pipeline VLM đầy đủ cho tài liệu đó |
| Bước đọc lại crop làm tăng latency | Chỉ chạy cho field lưỡng lự; gom crop thành request song song; theo dõi p95 |
| Hồ sơ đối tác học từ ví dụ sai | Chỉ học từ hóa đơn được người dùng xác nhận; lưu phiên bản hồ sơ |
| Hóa đơn không có bảng tổng hợp hoặc tổng không khớp do làm tròn | Luật dự phòng lấy `table_total` cuối + đánh dấu review; cho phép sai số làm tròn có cấu hình |
| Tài liệu dài vượt `max_model_len` | Chunk 1 trang cho bảng; luồng B chỉ nhận trang 1 + 3 trang cuối |

## Phụ lục: schema, prompt và code mẫu

Code mẫu cho G1, G3 và G6; cần điều chỉnh tên field và pattern theo hệ thống thật trước khi dùng.

### A. JSON schema (dùng với xgrammar)

```json
{
  "type": "object",
  "properties": {
    "rows": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "page_num": {"type": "integer"},
          "all_codes_in_row": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["page_num", "all_codes_in_row"]
      }
    },
    "quantities": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "page_num": {"type": "integer"},
          "label": {"type": "string"},
          "role": {"enum": ["line_item", "table_total", "grand_total"]},
          "value": {"type": "string"}
        },
        "required": ["page_num", "label", "role", "value"]
      }
    }
  },
  "required": ["rows", "quantities"]
}
```

`value` để dạng chuỗi nguyên văn (giữ dấu phân cách hàng nghìn), code tự chuẩn hóa sang số.

### B. Đoạn prompt mô tả vai trò

```text
Mỗi ảnh được đánh dấu "Trang k/N". Hãy liệt kê MỌI giá trị quantity bạn thấy, mỗi giá trị kèm role:
- line_item: số lượng của một dòng hàng.
- table_total: số lượng tổng kết ở cuối MỘT bảng dữ liệu.
- grand_total: số lượng trong bảng/ô tổng hợp nằm SAU tất cả các bảng dữ liệu, cộng dồn quantity của nhiều bảng.
Không tự tính toán, không chọn giá trị cuối cùng. Chép nguyên văn giá trị như trong ảnh.
Với mỗi dòng ảo của bảng, liệt kê MỌI mã xuất hiện trong dòng đó vào all_codes_in_row, chép nguyên văn, không lọc.
```

### C. Dựng message có "Trang k/N"

```python
def build_content(images_b64: list[str], page_nums: list[int], total_pages: int) -> list[dict]:
    content = []
    for img, k in zip(images_b64, page_nums):
        tag = f"Trang {k}/{total_pages}" + (" (trang cuối của tài liệu)" if k == total_pages else "")
        content.append({"type": "text", "text": tag})
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})
    return content

resp = client.chat.completions.create(
    model=MODEL,
    messages=[{"role": "system", "content": SYSTEM_PROMPT},
              {"role": "user", "content": build_content(imgs, pages, n_pages)}],
    temperature=0,
    logprobs=True,
    response_format={"type": "json_schema",
                     "json_schema": {"name": "invoice", "schema": SCHEMA}},
)
```

### D. Lọc mã code (G1) và đối chiếu OCR (G2)

```python
import re
CODE_RE = re.compile(r"^\d{4}-\d{6}$")

def norm(s: str) -> str:
    return re.sub(r"\s+", "", s)

def extract_codes(rows: list[dict], ocr_tokens_by_page: dict[int, set[str]]):
    accepted, to_recheck = [], []
    for r in rows:
        for raw in r["all_codes_in_row"]:
            code = norm(raw)
            if not CODE_RE.match(code):
                continue
            if code in ocr_tokens_by_page.get(r["page_num"], set()):
                accepted.append((r["page_num"], code))
            else:
                to_recheck.append((r["page_num"], code))  # -> G4: crop và đọc lại
    # khử trùng lặp do overlap giữa các chunk
    return sorted(set(accepted)), to_recheck
```

### E. Gộp quantity bằng luật (G6)

```python
def to_num(s: str) -> float:
    return float(re.sub(r"[^\d.\-]", "", s.replace(",", "")))

def merge_quantity(chunks: list[dict], tol: float = 0.0) -> dict:
    qs = [q for c in chunks for q in c["quantities"]]
    grands = [q for q in qs if q["role"] == "grand_total"]
    tables = [q for q in qs if q["role"] == "table_total"]
    if grands:
        best = max(grands, key=lambda q: q["page_num"])
        value, status = to_num(best["value"]), "grand_total"
    elif tables:
        best = max(tables, key=lambda q: q["page_num"])
        value, status = to_num(best["value"]), "fallback_review"
    else:
        return {"value": None, "status": "missing"}
    # kiểm tra chéo: grand total = tổng các table total
    if status == "grand_total" and tables:
        s = sum(to_num(t["value"]) for t in tables)
        status = "verified" if abs(s - value) <= tol else "sum_mismatch_review"
    return {"value": value, "status": status, "page_num": best["page_num"]}
```

Lưu ý: nếu dùng overlap dải ảnh, một `table_total` có thể xuất hiện ở hai chunk; khử trùng lặp theo `(page_num, label, value)` trước khi cộng.

### F. Lấy logprob thấp nhất của một giá trị (G3)

```python
def value_min_logprob(resp, value: str) -> float | None:
    toks = resp.choices[0].logprobs.content  # list token + logprob
    text, spans = "", []
    for t in toks:
        spans.append((len(text), len(text) + len(t.token), t.logprob))
        text += t.token
    start = text.find(value)
    if start < 0:
        return None
    end = start + len(value)
    lps = [lp for s, e, lp in spans if s < end and e > start]
    return min(lps) if lps else None

# field có min logprob < ngưỡng (ví dụ -0.5, hiệu chỉnh trên golden set) -> G4
```

Nếu cùng một giá trị xuất hiện nhiều lần trong JSON, cần tìm theo vị trí của field thay vì `text.find` đơn giản.
