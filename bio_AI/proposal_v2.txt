# DataMate: Proposal v2 (literature-informed revision)

**Status:** proposed 2026-11-01 (D3). It revises §2.2–2.6 of [PROPOSAL.md](PROPOSAL.md). Ingestion
(§2.1), Docker (§2.5), compliance (§9) and the constraints (solo, prompting only, ≤ 15B, offline)
are unchanged.
**Inputs:** the current MVP, the dev120 runs in `outputs/`, and the 45 papers in `pdf_papers/`
(gitignored, local only). Papers are cited as *Name (Venue)*.

---

## 0. TL;DR

Today the pipeline asks one 9B model to do everything in one shot: read the rulebook, pick the
meaning, and write correct pandas. The dev runs show it gets the **meaning** wrong far more often
than the **code**. Five changes, in order of expected gain:

1. **Plan first, then compute (semantic parsing into a typed plan).** The LLM fills a small JSON
   *plan* (intent, metric, period, filters, k, comparison, answer type). A **deterministic
   executor** in `dm` turns the plan into the answer, and the rulebook defaults are coded into the
   executor. Free-form code stays as a **fallback** for intents outside the catalog.
   *DIN-SQL (NeurIPS'23), Binder (ICLR'23), PURPLE (ICDE'24), DTS-SQL (EMNLP-F'24).*
2. **Two independent paths, then agree or abstain.** Path A is the plan executor and path B is
   free pandas code. When they agree, answer with high confidence. When they disagree, select a
   winner or abstain. *CHASE-SQL (ICLR'25), MCS-SQL (COLING'25), Rethinking Tabular Understanding
   (NAACL'24), Self-Consistency (ICLR'23).*
3. **Evidence next to the question.** Put the 2–4 rulebook clauses relevant to the question
   *directly beside it*, plus normalized dates and entity candidates. The full rulebook stays in
   the cached prefix. *BIRD evidence (NeurIPS'23), Knowledge-to-SQL (ACL-F'24), CHESS, CodeS
   (SIGMOD'24).*
4. **Verified examples, retrieved by skeleton.** Build the example bank (plans and code) from
   train with Claude. Retrieve examples by *masked question skeleton*, with a difficulty-aware
   count. *DAIL-SQL (VLDB'24), AID-SQL (ICDE'25), PURPLE (ICDE'24).*
5. **Selective prediction tuned for the −1 penalty.** Decide answer, unanswerable or abstain
   from path agreement, sanity checks and intent-level precision. Unanswerable is decided from
   schema capability flags, not from wording. *TrustSQL (penalty-based scoring), EHRSQL
   (NeurIPS'22), Know What I Don't Know (ACL-F'23), Abstention survey (TACL), Semantic
   Uncertainty (ICLR'23).*

Not adopted: fine-tuning (ROUTE, OmniSQL, CodeS training), heavy multi-agent loops (MAC-SQL, Data
Interpreter, Spider 2.0-style exploration) and table-as-text reasoning (Chain-of-Table, Dater).
See §6.

---

## 1. Evidence from our own runs

`outputs/dev120_v1` (Qwen3.5-9B, Ollama, 1 sample, k=4 examples without code, repair=1):

| type | n | correct | wrong | abstain | PA |
|---|---|---|---|---|---|
| number | 67 | 35 | 24 | 8 | +0.16 |
| percent | 23 | 8 | 12 | 3 | −0.17 |
| list | 8 | 1 | 5 | 2 | −0.50 |
| date / boolean | 10 | 9 | 0 | 1 | +0.90 |
| table / string / unans. | 12 | 4 | 4 | 4 | 0.00 |
| **all** | 120 | 57 | 45 | 18 | **+0.10** (precision 56%) |

`dev120_v2` (shorter-plan prompt, `sales_lines()` helper) is a partial run: on 64 questions,
**PA +0.23 at 65% precision**. It took about 30 s per question on the Mac.

The wrong answers in v2 fall into these groups:

| failure | example (question → wrong / gold) | what fixes it |
|---|---|---|
| wrong intent or metric | "lãi gộp tháng 2" → refused as *net* profit; "bn đơn bị hủy" → 1.48 (a rate) / 65 (a count) | typed plan with an explicit `metric` enum |
| wrong period | "bữa qua dthu" → 1.23 B (a long range) / 5.09 M (yesterday) | deterministic date parser, then the period goes into the plan |
| a rule applied wrong | % change for "tháng 5 vs tháng trước" → −3.42 / −1.79; average order value off by 2% | the executor encodes the rulebook defaults once and is tested |
| missing helper | debt top-k tables, shift revenue = 0, unit price on day D, price-change effect | executor intents for debt, shift, price |
| ranking details | top-5 list missing `Gạo ST25` (a base-unit or tie issue) | `rank_top` reached only through the executor |
| refusing an answerable question | "giá bán hôm 02/07" → None | capability flags decide unanswerable; the LLM's own refusal alone does not |

**Conclusion.** The model is the bottleneck for *rule-correct semantics*, not for Python syntax.
That matches what DIN-SQL and DTS-SQL report for small models: they do much better when
classification and linking are split from generation. It also matches TrustSQL: under a
penalty metric, the decision to abstain matters as much as accuracy.

---

## 2. Revised architecture

```
question ─► hints (deterministic): dates/periods, entity candidates, k, type cues
         ─► rule evidence: top-3 rulebook clauses (BM25 over rulebook sections)
         ─► examples: top-k verified (plan, code) by masked-skeleton similarity
                                │
        ┌───────────────────────┴───────────────────────┐
  Path A: PLAN (JSON, short)                      Path B: CODE (pandas over dm)
  LLM fills typed plan → validate                 existing pipeline, sees the plan
  → dm.execute(plan), deterministic               as a hint; 1 repair round
        └───────────────────────┬───────────────────────┘
                                ▼
   normalize like the scorer → agreement + sanity checks + capability guards
                                ▼
           answer | unanswerable | (extra samples if hard) | abstain
```

### 2.1 Path A: typed plan and deterministic executor (the main change)

**Plan schema** (validated with a small JSON schema; on a validation error, one retry):

```json
{"intent": "revenue_change_pct",
 "period": {"kind": "month", "y": 2026, "m": 5},
 "compare": {"kind": "prev_period_same_days"},
 "filters": {"product": null, "group": null, "customer": null, "shift": null, "channel": null},
 "k": null, "unit": null, "metric": "revenue",
 "answer_type": "percent",
 "overrides": []}
```

- `intent` comes from a **catalog of about 25–30 intents**, drafted from the train buckets in
  CLAUDE.md §3.5:
  - sales: revenue, revenue_change_pct, order_count, avg_order_value, cancel_count, cancel_rate,
    top_products, units_sold, group_share, customers_with_min_orders, top_customers, best_day,
    monotonic_growth, shift_revenue, tet_compare, price_change_effect, unit_price_on_day
  - debt: debt_top, debt_aging, debt_customer_flow
  - stock and imports: stock_at, stock_value, slow_movers, import_total, nearest_expiry
  - profit: gross_profit, net_profit
  - fallbacks: `other` and `unanswerable_subjective`
- `period` and `compare` are **parsed deterministically first** (`th7/26`, `quý 2`, `bữa qua`,
  `tuần trước`, `N ngày gần nhất`, Tết). The LLM only confirms or corrects that parse; it does
  not invent one.
- `overrides` is how a **private rulebook clause that differs from our defaults** reaches the
  executor, for example `{"rule":"include_returned_orders"}`. Every executor default is a named
  flag with a docstring citing its rulebook clause (as in PROPOSAL §2.2).
- `dm.execute(plan)` composes the existing helpers (`sales_lines`, `revenue`, `rank_top`, periods,
  `answer_*`) and raises `Unanswerable` from **capability guards** (`has_payments`, `has_stock`,
  `has_cost_on_line`, …).

**Why it fits the papers:**
- DIN-SQL routes each question by class to a class-specific prompt.
- Binder and PURPLE have the LLM emit a constrained program and leave execution to a
  deterministic engine.
- DTS-SQL shows that small models do better when the task is decomposed.

A plan of about 80 output tokens is also **about 5× cheaper** than code, which helps the 6 h
budget, and it is **deterministic** under greedy decoding, which helps the 0.03 reproducibility
rule.

**Generalization guard** (private test has unseen business types): an unknown intent →
`intent: "other"` → Path B only, with a stricter answer threshold. The catalog is never keyed on
business IDs (Rule 3). It is keyed on the meaning of the question.

**Build cost:** most executors are thin wrappers over helpers that already exist. The new pieces
are debt (`debt_at`, `debt_aging`, `debt_customer_flow`), shift revenue, price history and stock
at date. Each executor is tested on train against gold through the Claude-labelled set (§2.4).

### 2.2 Path B: code generation (current pipeline, tightened)

- Keep the current prompt, with additions:
  - the **Path A plan** is passed in as a hint ("a planner proposed: …; verify or correct")
  - the rule evidence (§2.3)
  - examples that show **code**, not just answers. Today `assets/examples.jsonl` does not exist,
    so examples carry no programs.
- **Repair beyond exceptions** (Self-Debug, ICLR'24): repair is triggered by an exception, but
  also by an empty frame, a 0 for money or count where the data is not empty, a period outside
  coverage, a type that does not match the plan's `answer_type`, or a string not found in the
  entity index. One round only.

### 2.3 Evidence next to the question

- **Rule evidence:**
  - Split `rulebook.md` into sections by its headings and bullets, and index them with BM25 over
    diacritic-free text (zero parameters).
  - Insert the top 3 clauses next to the question under `Rules that apply:`. The full rulebook
    stays in the cached system prefix, because the private rulebook changes and we never trim it.
  - BIRD and Knowledge-to-SQL both show that explicit evidence placed next to the question is a
    large win.
  - A small model loses clauses buried in 10k tokens of context. Repeating the relevant clauses
    beside the question costs about 300 tokens.
- **Value and entity linking** (CHESS, CodeS):
  - Use the existing `dm.find` fuzzy index to list the top-3 products, customers or groups for
    each noun phrase, with codes, in the hint block.
  - The plan's `filters` must reference a code from that list.

### 2.4 Example bank, retrieval and difficulty routing

- **Build the bank** (train only, Claude, as in PROPOSAL §4), now storing
  `{question, as_of, plan, code, answer, intent}`.
  - A plan or program counts as verified only if it reproduces the gold answer.
  - The same run gives **intent labels** for all 3000 train questions. Those labels measure the
    catalog's coverage and give per-intent precision for calibration (§2.5).
- **Retrieval** (DAIL-SQL):
  - Mask entities, numbers and dates in the question (`<SP>`, `<NUM>`, `<DATE>`), then rank
    examples by similarity of the masked skeleton.
  - Re-rank to prefer examples whose *plan intent* matches the predicted intent and whose
    required capabilities the current business has.
  - Exclude the current business during evaluation.
- **Difficulty-aware budget** (AID-SQL):
  - Easy intents (revenue, order_count, cancel_rate; train precision > 90%): Path A plus Path B
    greedy, stop if they agree.
  - Hard intents (debt, stock_at, price_change_effect, other): add 2 seeded Path B samples and
    turn thinking on.
  - The split is decided per intent from the train precision table, not by hand.

### 2.5 Decision: answer, unanswerable or abstain

**Answer** when P(correct) > τ. τ is tuned on train under leave-business-out to maximize PA,
starting near 0.5. P(correct) comes from a logistic model on these features:

- A/B agreement after scorer-style normalization (the strongest feature; Rethinking Tabular and
  CHASE-SQL both rely on cross-path consistency)
- vote share among Path B samples
- whether a repair was needed
- whether the result type matches the plan type
- sanity checks
- per-intent train precision
- whether the intent is `other`

**Unanswerable** (TrustSQL, EHRSQL):
- Emit it only when **(a)** a capability guard fired, **(b)** the period is entirely outside the
  data coverage, or **(c)** the intent is `unanswerable_subjective` (subjective or
  external-knowledge questions) *and* Path B agrees.
- A refusal from the LLM alone means **abstain**, never unanswerable. Several of v2's wrong
  answers were exactly this case.

**Abstain** in every other case. Remember that 70% coverage at 93% precision scores higher than
85% coverage at 85% precision (PROPOSAL §1).

### 2.6 Model

- Keep a single general model of 9–14B. The bake-off stays as in PROPOSAL §3: Qwen3.5-9B against
  Qwen3-14B, with thinking on and off.
- Path A suits a 9B model, since it is mostly classification and slot-filling. A 9B model also
  leaves room for more Path B samples.
- OmniSQL (VLDB'25) and CodeS (SIGMOD'24) show that SQL-specialized small models are strong, but
  our target is pandas plus Vietnamese plus rulebook semantics, and they would use the whole
  parameter budget. Consider them only if the design moves to DuckDB SQL, which this proposal
  does not recommend in the time left.

### 2.7 Teacher–student diagnosis (train only, dev time)

Goal: for every failure, find out whether it comes from the **pipeline** (ingestion, helpers,
rules) or from the **model's capacity**, so each day goes to the right fix.

- **Teacher.** A large open-weights model served with vLLM on a rented GPU, for example a ~27B
  dense Qwen or an ~80B MoE; pick the strongest one that fits the rental. It is used only during
  development, so the 15B limit does not apply to it. It never ships in the Docker image and is
  never declared as an inference model. It gets **exactly the same prompt and sandbox** as the
  student (Paths A and B, the same examples, hints and rule evidence).
- **Run** on train: dev120 first, then all 3000 questions if the rental time allows. Score
  against the `answers.jsonl` gold with our scorer.
- **Sort each question into one of four cells:**

  | gold vs teacher | gold vs student | meaning | action |
  |---|---|---|---|
  | wrong | wrong | pipeline problem | fix ingestion, helpers or rule encoding |
  | right | wrong | capacity gap | better examples, plan path, rule evidence, more samples, thinking on |
  | wrong | right | noise | feeds calibration; check the gold reading |
  | right | right | solved | nothing |

  Report the counts per intent, per answer type and per data family. The share of "both wrong"
  is the main **pipeline health metric**, and the share of "teacher right, student wrong" bounds
  what model-side work can recover.
- **Leave-family-out** (for example, pharmacy questions with no pharmacy examples) on both
  models estimates how the private test's unseen business types will behave.
- **Example bank.** Teacher plans and programs that reproduce the gold answer join
  `assets/examples.jsonl` next to the Claude ones (§2.4). This is cheaper than the API, and it
  avoids the open question of whether API-generated data is allowed.

**Public test boundary (Rule 6: no collecting answers to test questions by any means).** No
model, of any size, produces per-question reference answers for public or private test, and
nobody inspects such answers. Public test stays limited to what PROPOSAL §5 already allows:
robustness checks (crashes, empty tables, ingestion warnings) and the leaderboard score as the
only accuracy signal.

---

## 3. Mapping from papers to components

| component | papers (folder in `pdf_papers/`) | what we borrow |
|---|---|---|
| plan / DSL + executor | DIN-SQL, DTS-SQL (2, 3), Binder, StructGPT (5), PAL, Program-of-Thoughts (7) | decompose; LLM emits a constrained program; computation is deterministic |
| examples | DAIL-SQL, PURPLE, AID-SQL (2) | masked-skeleton retrieval; intent-matched demonstrations; difficulty-aware count |
| evidence and linking | BIRD (4), Knowledge-to-SQL, CHESS (2), CodeS (3) | rule clauses next to the question; value retrieval for entities |
| multiple candidates and selection | CHASE-SQL, MCS-SQL (2), Self-Consistency (8), Rethinking Tabular (5) | diverse generators, execution-based voting, cross-path agreement |
| repair | Self-Debug (7), DIN-SQL self-correction | execution feedback, including semantic sanity signals |
| abstention | TrustSQL, EHRSQL, Know What I Don't Know, Abstention survey, Semantic Uncertainty (8) | penalty-aware thresholds; schema-based unanswerability; consistency as uncertainty |
| messy ingestion | Auto-Tables, SpreadsheetLLM (6) | LLM fallback for unseen sheet structure, with a compact sheet encoding for header and region detection |
| evaluation framing | the TKDE surveys, Dawn of NL2SQL (1), DS-1000, InfiAgent-DABench, TableBench (4) | error taxonomy for triage; per-category reporting |

---

## 4. Time budget (2× RTX 5090, vLLM, ~3000 questions assumed)

| step | per question | note |
|---|---|---|
| Path A plan | ~0.3k decode tokens with a short rationale | prefix-cached prompt |
| Path B greedy code | ~0.5k decode | as today |
| extra samples (hard intents only, ~35% of questions) | 2 × 0.5k | thinking on for these only |
| total | ~1.2k decode tokens on average | about 3.6M tokens for 3000 questions, well under the old estimate of 6–8M |

The time guard is as in PROPOSAL §2.5. When behind schedule, drop the extra samples first, then
Path B on easy intents (keep Path A, which is cheap and deterministic).

---

## 5. Plan for the remaining days (D3 = 2026-11-01 to D12 = 2026-11-10)

| day | deliverable | done when |
|---|---|---|
| D3 | finish the dev120_v2 run; Claude or teacher (§2.7) run on ~600 train questions → plans, code and intent labels; teacher on dev120 for the four-cell table | intent coverage table; `assets/examples.jsonl` exists; pipeline vs capacity split known |
| D4 | plan schema plus deterministic date and period parser plus `dm.execute` for the top 12 intents (revenue family, counts, cancel, top-k, AOV, best day) | executors match gold on ≥ 95% of their labelled train questions |
| D5 | rule-evidence retrieval; entity candidates in hints; Path A wired in; dev120 run (A only, B only, A+B) | PA of A+B > PA of B alone on dev120 |
| D6 | remaining executors (debt, stock_at, shift, price change, profit, expiry, Tết); Claude labels for all of train | **first public submission** |
| D7 | semantic repair triggers; difficulty routing; skeleton retrieval | dev PA tracked per intent |
| D8 | logistic decision model; τ tuned under leave-business-out; unanswerable policy | **second public submission** |
| D9 | robustness on public formats (phone, repair, mother & baby); `other`-intent path checked under leave-family-out | 0 crashes; precision on `other` measured |
| D10–D12 | Docker, timing and determinism dry run on 2× 5090, freeze (PROPOSAL §7 D10–D12) | image pushed |

**Gates:**
- If by D5 Path A does not beat Path B on dev120, keep Path A only as a **hint and voter** for
  Path B, and stop building more executors.
- If the Claude bank shows the catalog covers < 70% of train, spend D6 on Path B quality
  instead.

---

## 6. Considered and not adopted

| idea | source | why not now |
|---|---|---|
| fine-tuning a small text-to-SQL model | ROUTE (ICLR'25), OmniSQL (VLDB'25), CodeS (SIGMOD'24) | the constraints say prompting only; < 10 days left |
| multi-agent pipelines (selector, decomposer, refiner agents) | MAC-SQL (COLING'25), Data Interpreter | many LLM calls per question; time budget; little gain over A+B at 9B |
| agentic schema exploration | Spider 2.0 (ICLR'25), ReAct | our schemas are small and pre-carded; exploration adds latency and nondeterminism |
| reasoning over tables as text | Chain-of-Table (ICLR'24), Dater (SIGIR'23), TAPEX-style | tables have up to 100k+ rows; we need exact numeric aggregation |
| switching the engine to DuckDB SQL | most text-to-SQL work | the rules (forward-fill, returns, base units, lunar Tết) already live in pandas helpers; a rewrite is too risky |
| LLM-first ingestion | SpreadsheetLLM, Auto-Tables | deterministic ingestion already has 0 warnings on all 44 businesses; LLM only as a fallback for unseen layouts |

---

## 7. Risks specific to this revision

| risk | mitigation |
|---|---|
| the intent catalog overfits train or public phrasings | the `other` → Path B route; leave-family-out check on D9; intents defined by meaning, never by business |
| the private rulebook changes a default the executor hard-codes | `overrides` flags; rule evidence shown to the planner; when the evidence clause contradicts a default and no override was emitted, lower confidence |
| A and B make the same mistake together (shared hint) | Path B sees the plan only as a *suggestion*; log how often B overrides A; if agreement is not predictive on dev, drop the hint from B |
| more moving parts for a solo developer | each piece can be switched off by a flag; the gate on D5 decides whether to keep it |
