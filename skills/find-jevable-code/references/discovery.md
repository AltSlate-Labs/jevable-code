# Discovery and suitability examples

## Contents

1. Search leads
2. Positive and negative examples
3. Tracing checklist
4. Ranking and evaluation

## Search leads

Start with filenames and architecture, then search a bounded application directory. These are **discovery hints**, not a detector that can prove suitability. Adapt spelling and framework conventions to the repository. Do not print entire files or recursively scan dependencies when a narrow query will do.

```bash
rg --files -g '!node_modules/**' -g '!vendor/**' -g '!dist/**' -g '!build/**' -g '!*.lock'
rg -n -i 'classif|triage|intent|moderation|relevance|sentiment|severity|escalat|fuzzy|similarity|rerank' src
rg -n -i 'chat\.completions|responses\.create|messages\.create|generate_object|generateObject|with_structured_output|response_format|invoke\(' src
rg -n -i 'keyword|heuristic|rubric|confidence|threshold|priority|category|dispatch|needs_review' src
rg -n -i 'return only|respond.*(yes|no)|one of|choose.*option|rate.*(quality|severity)|classify' prompts tests src
```

Replace `src`, `prompts`, and `tests` with directories discovered in the project. Query configuration, prompt files, notebooks, jobs, and service-specific packages where relevant. Avoid broad `if|return|score` searches until narrowed to a candidate area.

Do a workflow pass even if keywords find little: inspect intake → interpretation → decision → action. A function called `process` may contain the best candidate. Follow wrappers to the actual prompt and consumer before recommending a model call replacement.

## Positive and negative examples

| Existing behavior | Possible mapping | What must be established |
| --- | --- | --- |
| LLM returns a single department enum from ticket text | Choice | Actual options, unknown behavior, downstream dispatch, baseline quality/cost |
| Keyword cascade estimates intent from varied natural language | Choice | Semantics beyond exact matching; negation/ambiguity examples; remote-call budget |
| LLM rates answer helpfulness or evidence relevance | Score | Concrete single-dimension levels and whether the caller also needs a rationale |
| Subjective weights approximate content quality | Several Scores + code weights | Which factors require semantic judgment and which are exact measurements |
| Fuzzy title matching tries to detect duplicate issues | Noul per proposed pair | Available pair evidence, candidate retrieval recall, false-merge consequences |
| Natural-language gate checks whether a user asks for escalation | Noul | Clear proposition; distinction between urgency and explicit human request |
| LLM produces a summary plus a risk flag | Noul for flag; retain summary generation | The flag is independently answerable from available evidence; generation still needed |
| LLM ranks candidate passages by relevance | Score or Noul per candidate + code sort | Consistent questions, comparable evidence, ranking evaluation, retrieval coverage |
| Tool router chooses among supplied actions | Choice for intent | Action allowlist, argument construction, authorization, and execution stay in code |
| Free-form design brief selects existing template/style options | Choice; possibly Scores/Nouls for constraints | Concrete candidate registry; hard validity checked separately; no image/code generation claim |
| Multi-field structured LLM response | Multiple primitives for compatible fields | Exact/free-text fields remain supported; cross-field constraints and dependencies are explicit |

Common false positives:

| Code | Usual verdict | Reason |
| --- | --- | --- |
| `is_admin`, ownership, tenant membership, feature flag lookup | Keep current approach | Authorization and exact configuration are explicit facts |
| Tax, invoice totals, quotas, balances, timestamps, integer thresholds | Keep current approach | Deterministic computation or policy |
| Regex validates an email shape, protocol field, or reference number | Keep current approach | Syntax/format checking, not semantic judgment |
| Router switches on an already trusted enum | Inspect its producer | Dispatch itself does not need a model |
| Sort by stored price/date/score | Keep current approach | Sorting known values is exact code; inspect score creation separately |
| Retry on known HTTP status, exponential backoff | Keep current approach | Defined operational rule |
| Choose a uniform random valid preset | Keep RNG and exact checks | A model is useful only if a separate semantic constraint needs judgment |
| Generate prose, source code, SQL, novel identifiers, or evidence spans | Unsuitable as a whole | Output is not one of the three typed judgments |
| Read an unavailable database/document to decide | Blocked | Missing evidence cannot be replaced by confidence |
| Multi-step planning, proof, unrestricted optimization | Decompose or reject | A bounded result does not make the reasoning a focused judgment |
| A tiny in-memory heuristic with no demonstrated problem | Usually low priority or reject | Added remote latency/availability/cost may outweigh any benefit |

Keep nuanced cases explicit:

- A semantic abuse flag may feed enforcement, but it does not replace account permissions or all enforcement policy.
- A schema-shaped LLM response may still depend on difficult reasoning. Inspect task complexity, not only the output schema.
- A large branching function may faithfully encode product requirements. Complexity is not evidence that the logic is fuzzy.
- A library's existing classifier is a baseline, not an automatic replacement target. Need measured value.
- A classification used only in a generated explanation may not be independently replaceable without changing consistency or cost.
- A known category of issue, an estimated probability of resolution, and a severity level are different questions even when all use numbers in code.

## Tracing checklist

For each lead, trace producer → consumer and capture:

1. Location of the evidence construction, decision, parsing, and first consequential consumer.
2. Actual input/output types, option registry, rubric, or boolean meaning.
3. Whether data is already available, requires retrieval, or is created by an earlier model output.
4. Existing tests for ambiguous and negative cases, plus observed failures when available.
5. Coupling to returned prose, citations, dynamic arguments, or side effects.
6. Call frequency, latency constraints, data volume, and error handling, if visible.
7. Current implementation's intended behavior versus a proposed product behavior change.

Prefer a source-grounded contract such as `state.message <- Ticket.body in route_ticket` over "send relevant context". If tests or traffic data are absent, say so. Do not claim a model improves quality because the old code looks inelegant.

## Ranking and evaluation

Recommend a compact pilot, not an automatic migration. Pick a decision with usable examples, an isolated caller contract, and measurable downstream value.

| Primitive or workflow | Useful measures |
| --- | --- |
| Choice | Per-class precision/recall, confusion matrix, abstention/coverage, error-weighted outcome; log loss or Brier score when probabilities drive decisions |
| Noul | False-positive/false-negative rates at operational thresholds, precision/recall, Brier/log loss and reliability assessment; positive and negative automation coverage |
| Score | Ordinal agreement or absolute error against a defined rubric, ranking agreement where relevant, distribution quality, and operational threshold errors |
| Ranking | NDCG/recall at K or task-appropriate ranking metric; retrieval recall separately from reranking |
| Batched/dependent decisions | Per-question quality, consistency of the combined result, end-to-end failure rate, and latency along the actual dependency path |

Use real labeled examples, independent review, or observed outcomes when possible. Agreement with another LLM is a proxy, not ground truth. Label construction, ambiguous cases, and annotation disagreements should be visible.

Select error budgets and success criteria from repository requirements or user priorities. When unavailable, propose criteria and mark them as untuned. Do not fabricate achieved accuracy, sample sizes, speedups, traffic, or monetary savings.

If economics matter, use measured costs for the candidate workflow:

`expected_new_cost = preparation + Jev_calls + fallback_rate * fallback_cost + downstream_costs`

Compare with the complete current workflow; shared work must not be counted twice. Count serial network calls on the critical path separately from parallel batches. Include timeouts and retries. Batch benefits must be measured at the actual state size and question count.

Keep prompt/rubric tuning, threshold selection, and final evaluation separate. Test relevant changes in option order, option set, phrasing, and question batches; do not assume interface-level independence proves empirical invariance in every workflow. Include missing/irrelevant evidence and prompt-like text in input where that is a realistic failure mode.
