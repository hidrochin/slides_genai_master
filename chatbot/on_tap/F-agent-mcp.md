# F — Agent, LangGraph/Langfuse & giao thức MCP / A2A

> Bài 10 (Agentic Frameworks + MCP-A2A). ⇐ [ONE-PAGER](00-ONE-PAGER.md)

---

## 1. Vì sao cần Agent?
1 lời gọi LLM đơn lẻ có **trần cứng**: không truy cập dữ liệu real-time, không gọi API, không tự sửa. **Agent** = **reason → act → observe → adjust** (vòng lặp).

**Định nghĩa:** phần mềm tự chủ **perceive → reason → act** hướng mục tiêu, có reasoning/planning/memory + tự chủ ra quyết định.
**Thành phần điển hình:** **Reasoner** (thường là LLM — "bộ não") · **Tools** (API/function/retriever) · **Memory** (ngắn & dài hạn) · **Planner** (routing/control flow).

## 2. Các pattern của Agent ⭐
| Pattern | Cơ chế | Hợp với |
|---|---|---|
| **ReAct** (Yao 2022) | **Thought → Action → Observation** (loop) | mặc định; task khám phá, bước kế phụ thuộc quan sát |
| **Plan-and-Execute** (Wang 2023) | Lập **kế hoạch đầy đủ** trước → thực thi tuần tự; replan khi fail | task đa bước rõ ràng; **ít lãng phí LLM call** |
| **Reflexion** (Shinn 2023) | Act → Evaluate → **Self-reflect** (tự phê bình) → retry | task hay lặp lỗi, cần học từ sai lầm |
| Tree of Thoughts | nhiều nhánh suy luận song song + backtracking | bài toán tổ hợp |
| ReWOO | reasoning **không cần observation** | tiết kiệm chi phí |

## 3. Ba lớp công cụ: LangChain / LangGraph / Langfuse ⭐
| | **LangChain** | **LangGraph** | **Langfuse** |
|---|---|---|---|
| Vai trò | **Building blocks** | **Orchestrator** | **Observability platform** |
| Bản chất | components (chat model, prompt, tool, retriever, memory, output parser) | **state machine** dạng graph (node+edge+state) | tracing/eval/prompt mgmt/dataset/playground/metrics |
| Đặc trưng | interface thống nhất trên nhiều provider | **cycle, branch, HITL, checkpoint** | framework-agnostic, self-host, **OpenTelemetry-native** |

> **Mental model:** LangChain cho **linh kiện**, LangGraph **ráp** thành agent, Langfuse **quan sát & cải thiện**.
> **v1.0:** `AgentExecutor` cũ → **legacy** (langchain-classic). Dùng **`create_agent()`** (chạy trên LangGraph runtime) + **`init_chat_model()`** (đổi provider 1 dòng).

### 3.1 Chain (LCEL) vs Graph
| | LangChain (LCEL) | LangGraph |
|---|---|---|
| Topology | tuyến tính (input→A→B→out) | graph có **cycle/branch/conditional** |
| State | ngầm (qua pipe) | **shared state object** rõ ràng, persist qua checkpointer |
| Retry/loop | thủ công try/except | **first-class** (route edge quay lại) |
| HITL | không có sẵn | **interrupt()** tại bất kỳ node |
| Hợp với | RAG, prompt chain, Q&A tuyến tính | multi-step agent, retry, branch, multi-agent |

> **Quy tắc:** cần **loop/retry/branch/pause-approval** → LangGraph; còn lại LangChain đủ.

## 4. LangGraph — 3 primitive ⭐
1. **State** — schema có kiểu (**TypedDict / Pydantic / dataclass**) chia sẻ giữa node; giữ messages, tool outputs, kết quả trung gian. Field cần tích luỹ dùng **reducer**: `Annotated[list, add_messages]` (append thay vì ghi đè). Persist qua checkpointer.
2. **Node** — hàm Python nhận state (+ config/runtime), làm việc (gọi LLM/tool/transform), **trả về partial update** (dict), **KHÔNG mutate trực tiếp**. LangGraph merge qua reducer (scalar → replace; list có `add` → append). Đăng ký `builder.add_node(name, fn)`.
3. **Edge** — điều khiển luồng, 4 loại:
   - **Normal edge**: A → B cố định (`add_edge`).
   - **Conditional edge**: hàm routing đọc state → trả tên node kế / `END` (`add_conditional_edges`).
   - **Entry Point**: node đầu (`add_edge(START, ...)`).
   - **Conditional Entry Point**: bắt đầu ở node khác nhau tuỳ input (route by query type/user tier).

**Vòng đời:** `StateGraph(State)` → `add_node/add_edge` → **`.compile()`** (validate) → **`.invoke()`** (chạy hết) / `.stream()` (yield update) / `.get_graph().draw_mermaid()`.

## 5. Tính năng production của LangGraph
- **Checkpointer** — persist state sau **mỗi node** (Postgres/Redis/SQLite) → resume sau crash, **time-travel debug**.
- **Human-in-the-Loop** — **`interrupt()`** dừng giữa graph, chờ người duyệt, resume đúng điểm.
- **Streaming** — `astream(stream_mode="updates")` stream token/state/event cho UI real-time.
- **Deterministic**: cùng input + state → cùng path (tốt cho regression test).

### 5.1 Multi-Agent patterns ⭐
- **Supervisor** (hub & spoke): 1 LLM điều phối chọn worker kế (project manager).
- **Hierarchical**: supervisor lồng nhau (nested teams), scale lớn.
- **Swarm**: agent **hand-off trực tiếp** cho nhau, **không** điều phối trung tâm.

## 6. Langfuse — Observability
Vì logging truyền thống **không scale** với hệ **non-deterministic, đa bước**. Bắt: prompt gửi/nhận, tool call & output, token/model, latency mỗi bước, error/retry, cost.
- **Trace phân cấp**: nested call tự động link thành cây; thêm `user_id` + `session_id` để debug 1 user.
- **6 năng lực**: **Observability · Metrics · Prompt Management** (version prompt, deploy không cần redeploy code) · **Playground** (so sánh model/prompt) · **Evaluation** (**LLM-as-a-judge**, dataset experiment) · **Annotations** (human review queue → dataset gán nhãn).
- Tích hợp: 1 **CallbackHandler** cho toàn bộ; hoặc `@observe()` decorator. OpenTelemetry-compatible.

## 7. MCP — Model Context Protocol (Anthropic) ⭐
**Chuẩn mở** tích hợp dữ liệu/tool/context ngoài vào AI model — "**universal port**" chuẩn hoá tương tác agent ↔ hệ ngoài. **MCP = Agent ↔ Tool** (vertical capability).

### 7.1 MCP vs Function Calling
- **Function Calling**: LLM nhận diện cần tool nào & khi nào gọi; **lập trình viên tự implement** procedure nhận request + gọi backend. Nhúng cứng tool vào từng app.
- **MCP**: viết tool **1 lần** trong MCP server → **mọi** app/agent (Claude Desktop, Cursor, LangChain) dùng được → **tái sử dụng**, an toàn hơn (**LLM ≠ execute tool**), privacy-first, scalable.

### 7.2 Kiến trúc (3 vai) ⭐
- **Host**: app AI chính user tương tác (Claude Desktop, Cursor IDE).
- **Client**: quản lý kết nối tới **1** MCP Server, **sandbox** tương tác.
- **Server**: expose **tools/resources/prompts** liên quan hệ ngoài.

### 7.3 Transport
- **stdio**: client khởi động server như **subprocess**; đọc **stdin** / ghi **stdout**; message **JSON-RPC** (không newline nhúng); log → **stderr**. Local, low-latency.
- **streamable-HTTP**: client → server qua **HTTP POST** (JSON-RPC); server → client qua **Server-Sent Events (SSE)**; server chạy độc lập, phục vụ nhiều client, async real-time. Dùng **POST (request) + GET (nhận stream)**.

### 7.4 MCP Primitives ⭐
- **Resources**: dữ liệu server expose (file, DB record, API response, screenshot); định danh bằng **URI**; **application-controlled**. Text (UTF-8) / Binary (Base64).
- **Prompts**: template prompt tái sử dụng.
- **Tools**: hàm LLM gọi được.
- **Sampling**: **server yêu cầu LLM qua client** → agentic workflow giữ privacy + **human-in-the-loop**. Flow: Server xin → Host duyệt an toàn/context → chọn model & gọi LLM → Host kiểm tra kết quả → trả về Server.
- **Roots**: URI (file path/URL) client gợi ý server tập trung → định nghĩa **workspace boundary**.

## 8. A2A — Agent to Agent (Google) ⭐
**Chuẩn mở** cho giao tiếp/liên thông **trực tiếp giữa các agent** khác framework/vendor. **A2A = Agent ↔ Agent** (horizontal collaboration). Mục tiêu: agent cộng tác & chia sẻ thông tin có cấu trúc, **không** coi agent khác là tool/API tĩnh.

**Actors:** **User** · **A2A Client** (Client Agent, thay mặt user gửi request) · **A2A Server** (Remote Agent, HTTP endpoint, xử lý task — client coi như **opaque**).

**Communication objects:**
- **Agent Card** → **discover** agent (khả năng, endpoint).
- **Task** → đơn vị công việc; lifecycle: **submitted → working → input-required → completed**.
- **Message** → trao đổi hội thoại/context giữa client & remote.
- **Artifact** → **kết quả cuối bất biến** (immutable) do remote agent tạo.
- **Parts** → khối dữ liệu tự chứa trong message/artifact (text, file blob, JSON).

## 9. MCP vs A2A ⭐
| | **MCP** | **A2A** |
|---|---|---|
| Của | Anthropic | Google |
| Kết nối | **Agent ↔ Tool/data** | **Agent ↔ Agent** |
| Hướng | **Vertical** capability | **Horizontal** collaboration |
> **Cùng nhau** → hệ Agentic AI hoàn chỉnh (agent dùng tool qua MCP + cộng tác agent khác qua A2A).

---
## ✅ Chốt nhanh mục F
- Agent = perceive/reason/act/observe; thành phần Reasoner/Tools/Memory/Planner; pattern **ReAct**(mặc định)/Plan-Execute/Reflexion.
- LangChain (blocks) / LangGraph (orchestrator, cycle+HITL+checkpoint) / Langfuse (observability). `create_agent` thay `AgentExecutor`.
- LangGraph 3 primitive: **State/Node/Edge**; edge 4 loại; `interrupt()` HITL; checkpointer persist; multi-agent Supervisor/Hierarchical/Swarm.
- **MCP** = Agent↔Tool (Host/Client/Server; stdio & streamable-HTTP/SSE; Resources/Prompts/Tools/**Sampling**/Roots). **A2A** = Agent↔Agent (Agent Card/Task/Message/Artifact/Parts).
- **MCP = vertical, A2A = horizontal**.
