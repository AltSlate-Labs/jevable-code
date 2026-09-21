# Jev decision contract

Verified against TypeSafe's official documentation on **2026-09-21**. Treat API limits and SDK details as a dated snapshot. During an audit, check the repository's pinned SDK/model and refresh any details material to the recommendation against the primary links below. If lookup is unavailable or disallowed, continue conceptual analysis, disclose the snapshot, and leave unverified integration details explicit.

## The three primitives

| Primitive | Model judgment | Result used by code | Common audit target |
| --- | --- | --- | --- |
| Choice | Select one supplied alternative | `choice`, `probabilities`, `confidence` | Semantic dispatch, intent, categorization, candidate selection |
| Score | Locate content on described ordered levels | `score`, `legend`, `probabilities`, `confidence` | Severity, quality, relevance, rubric-based priority |
| Noul | Evaluate a defined yes/no proposition | `noul`, the probability of yes | Semantic flags, matching, evidence sufficiency, escalation signals |

**Choice:** use mutually distinguishable options; include an unknown/other outcome when the task requires it. The documented limit is 255 options per question. A Choice selects one option, not a multi-label set. More than 255 requires a candidate-reduction or hierarchy design, with coverage/error analysis. [Choice documentation](https://docs.typesafe.ai/primitives/choice).

**Score:** use 2–10 descriptive levels, ordered from low to high. With K levels, `score` is the probability-weighted level index, from 0 to K−1, and may be fractional. It is not unconstrained numerical regression or a physical measurement. Two different distributions can share a mean; retain the distribution when that matters. Make every level self-contained: the model does not see its ordinal number or neighboring descriptions. A code-side rescaling changes units, not what was measured. [Score documentation](https://docs.typesafe.ai/primitives/score).

**Noul:** `noul` is P(proposition is true), not an intensity or degree. Around 0.5 expresses uncertainty; around 0 expresses confidence in no. There is no separate `confidence` field. Optional criteria use `true` and `false` descriptions. For multi-label detection, one Noul per label may fit. Avoid ambiguous compound propositions. [Noul documentation](https://docs.typesafe.ai/primitives/noul).

**Confidence:** Choice/Score `confidence` summarizes distribution shape; it is not necessarily the selected option probability or a calibrated probability of correctness. Type-constrained output does not establish factual accuracy. Validate the task and thresholds locally. [Confidence documentation](https://docs.typesafe.ai/confidence).

## Contract shape

Use this as an illustrative request body shape, not as evidence that a call ran. Replace fields and questions with repository-specific content. Choose a verified model identifier when writing an executable integration; the placeholder below is not a real model name.

```json
{
  "model": "<verified-model-id>",
  "state": {
    "message": "<value from the inspected call site>",
    "allowed_queues": ["billing", "technical", "general"]
  },
  "questions": {
    "queue": {
      "type": "choice",
      "instructions": "Which allowed queue should handle the main request in `message`?",
      "criteria": {
        "billing": "Invoices, charges, or payment questions.",
        "technical": "Product malfunction or technical help.",
        "general": "General requests, unclear requests, or requests outside the other queues."
      }
    },
    "disruption": {
      "type": "score",
      "instructions": "How much work disruption is described in `message`?",
      "criteria": [
        "Work continues normally; only a cosmetic inconvenience is described.",
        "Work is impaired, but an available workaround allows it to continue.",
        "Work is blocked and no available workaround is described."
      ]
    },
    "human_requested": {
      "type": "noul",
      "instructions": "Does `message` ask to speak with a human support agent?"
    }
  }
}
```

The request contains shared `state` and a map of `questions`; each answer appears under its question ID. IDs identify results for the caller and are not model instructions. State field paths can be named explicitly in instructions. Confirm exact serialization against the installed SDK when implementing. [Primitives documentation](https://docs.typesafe.ai/primitives).

## Composition boundaries

Questions in one request use the same state and do not consume each other's answers. Batch questions that are constructible from that state, including conditionally used answers. Make a later request when an earlier answer changes required evidence or options. [Primitives: dependencies](https://docs.typesafe.ai/primitives#when-one-question-depends-on-another).

Apply these engineering checks when proposing a design:

- Preserve mathematical distinctions: per-question independence of execution is not independence of the underlying events.
- Keep code-side ranking and constraints explicit. Do not compare within-list Choice probabilities from unrelated candidate lists as universal relevance scores.
- Account for recall lost during retrieval or pruning. Choosing among retrieved candidates cannot recover an omitted correct candidate.
- Supply evidence through application code. An interface that produces labels cannot fetch missing facts or generate an explanation for the caller.
- Distinguish semantic screening from exact constraint enforcement. Sampling, seeds, action execution, and validity checks belong in ordinary code.
- Recheck state-size and per-request limits if batching materially affects feasibility. Do not infer unbounded capacity from the presence of many questions.

## Source policy

Use official `docs.typesafe.ai`, `typesafe.ai`, and official TypeSafe SDK sources for current API claims. Independent Jev guide sites are not authoritative SDK references. Do not import claims about undisclosed architecture, training recipes, guaranteed calibration on new domains, or universal speedups into the audit.

For a later implementation task, the [official TypeSafe agent skill](https://docs.typesafe.ai/agent-skill) can provide SDK guidance. This audit skill does not require installing it or obtaining a Jev API key.
