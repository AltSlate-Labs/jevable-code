# Example jevability audit — `sample-repo`

This is an illustrative report produced by running **find-jevable-code** against
[`sample-repo/support_router.py`](sample-repo/support_router.py). It shows the
expected shape and grounding of the output. No Jev call was executed; the
question contracts below are illustrative.

## Scope

Repository: `examples/sample-repo`. Revision: fixture. Reviewed: `support_router.py`
(single module, 3 decision functions + orchestrator). Excluded/unavailable: no tests,
prompts, or traffic data present. Evidence: static inspection only. Interface
reference: `references/jev-contract.md` snapshot (2026-09-21).

## Best opportunities

The strongest opportunity is `route` (`support_router.py:23`): a keyword-count
cascade that approximates *intent* from free-text tickets and silently collapses
ties into `general`. It is a bounded selection over a fixed queue set with all
evidence available at the call site — a direct **Choice** candidate. `urgency_weight`
is a plausible **Score**; the human-request half of `needs_human` is a **Noul**, but
its wait-time half is exact policy that must stay in code.

| ID | Location and symbol | Current decision | Primitive(s) | Status | Priority | Evidence confidence | Main benefit hypothesis / blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| J01 | `support_router.py:23` `route` | keyword-count → queue | Choice | Direct | High | Medium | Handles paraphrase/negation the keyword list misses; tie-to-`general` is lossy |
| J02 | `support_router.py:40` `urgency_weight` | hand-weighted severity 0..1 | Score | Decompose | Medium | Low | Ordinal severity is semantic; the 0.2/0.4/0.3 weights are arbitrary |
| J03 | `support_router.py:33` `needs_human` | keyword OR wait>30 | Noul (+ keep code) | Decompose | Medium | Medium | "Asked for a human" is semantic; `minutes_waiting > 30` is exact policy — keep it |

## Candidate J01: ticket → support queue

- **Evidence:** `route` (`support_router.py:23`), consumed by `handle` (`support_router.py:52`) as the `queue` field. `_BILLING` / `_TECH` keyword lists at the top of the module.
- **Current behavior:** counts substring hits per list; returns `general` when both are zero (`:29`) and breaks ties toward `billing` (`:30`). Misses synonyms, negation ("I was *not* charged"), and multi-topic tickets.
- **Boundary:** replace the count-and-compare in `route` with one Choice over `QUEUES`; keep `QUEUES` as the application-owned option registry.
- **State:** `state.message <- f"{subject} {body}"` (available at `:24`); `state.allowed_queues <- QUEUES`. No retrieval needed.
- **Question contract:**
  ```json
  {
    "queue": {
      "type": "choice",
      "instructions": "Which allowed queue should handle the main request in `message`?",
      "criteria": {
        "billing": "Invoices, charges, refunds, or payment questions.",
        "technical": "Product malfunction, errors, or technical help.",
        "general": "Anything else, unclear, or spanning multiple queues."
      }
    }
  }
  ```
- **Result consumption:** the returned `choice` becomes `handle(...)["queue"]` unchanged. Keep a deterministic default to `general` on low `confidence`.
- **Composition:** J01 and J02 share the same `state.message` and can batch in one request; J03's human-request Noul can join the same batch (all read the ticket text). None depends on another's answer.
- **Fallback:** on unknown/low-confidence or API error, fall back to the existing keyword `route`. Threshold untuned — select on a labeled dev set.
- **Expected value:** hypothesis only — better recall on paraphrased/negated tickets and no silent tie-to-`general`. No baseline accuracy is measured here.
- **Validation:** label a sample of real tickets; per-class precision/recall + confusion matrix vs. the keyword baseline; measure added latency/cost of the remote call.
- **Unknowns:** no traffic volume, no existing labels, no measured misroute cost.

## Composition opportunities

| Group | Shared state | Questions | Execution | Why |
| --- | --- | --- | --- | --- |
| G1 | `message` (ticket subject+body) | J01 queue · J02 severity · J03 human-request | Same request | All three read only the ticket text; none consumes another's answer |

`minutes_waiting > 30` (J03) and the priority **sort** over `urgency_weight` stay
in code — independent Score/Noul answers do not form a joint ranking.

## Keep as code / rejected leads

| Location | Tempting mapping | Why it should remain unchanged |
| --- | --- | --- |
| `support_router.py:37` `minutes_waiting > 30` | Noul from a boolean | Exact SLA policy, not a semantic judgment |
| priority sort over `urgency_weight` | "let the model rank" | Sorting known floats is exact code; only score *creation* is semantic |

## Recommended first pilot

Pilot **J01** alone (smallest boundary, clearest baseline). Data: a held-out sample
of labeled tickets. Baseline: current keyword `route`. Proposed target: no worse
per-class recall and elimination of silent tie-to-`general`, measured before rollout.
Ship behind the existing keyword path as fallback; roll back by feature flag.
Coverage limit: one file, no tests or traffic — treat every number above as a
proposal, not a measurement.
