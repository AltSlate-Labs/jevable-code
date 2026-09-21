# Jevability audit report template

Replace bracketed fields with inspected evidence. Omit irrelevant sections and compress small audits. Include no invented findings, outputs, metrics, or API execution claims. Detail the top three candidates by default; add more if requested.

## Scope

Repository: [name/path]. Revision: [if available]. Reviewed: [specific areas]. Excluded/unavailable: [areas]. Evidence: [static inspection / existing tests / measurements actually run]. Interface reference: [verified SDK/docs, or dated snapshot].

## Best opportunities

[One short paragraph naming the strongest opportunity and the reason, or explaining why no candidate qualifies.]

| ID | Location and symbol | Current decision | Primitive(s) | Status | Priority | Evidence confidence | Main benefit hypothesis / blocker |
| --- | --- | --- | --- | --- | --- | --- | --- |
| J01 | [path, line reference, symbol] | [behavior] | Choice / Score / Noul | Direct / Decompose / Blocked | High / Medium / Low | High / Medium / Low | [grounded reason] |

Use source links supported by the environment. Keep line references tied to the inspected version. Priorities are qualitative judgments, not model outputs.

## Candidate J01: [decision name]

- **Evidence:** [definition, caller, output consumer, tests; short relevant excerpts when helpful].
- **Current behavior:** [what happens and its known limitations].
- **Boundary:** [exact logic to replace/extract; surrounding deterministic behavior].
- **State:** [field → origin mapping, availability, missing values, proposed retrieval if any].
- **Question contract:** [concrete `type`, `instructions`, and `criteria` if applicable].
- **Result consumption:** [typed field → existing return value or code branch; preserve other outputs].
- **Composition:** [batch group, conditional consumption, or true preceding dependency].
- **Fallback:** [unknown/ambiguous answer, missing evidence, timeout/service error, original path].
- **Expected value:** [what may improve; evidence versus unmeasured hypothesis].
- **Validation:** [baseline, data, metric, threshold tuning, downstream error costs, success criteria].
- **Unknowns:** [what prevents a stronger recommendation].

For a direct candidate, include a concrete request fragment or clearly labeled adapter pseudocode. For a blocked candidate, state what is missing rather than inventing a ready-to-run integration.

## Composition opportunities

| Group | Shared state | Questions | Execution | Why |
| --- | --- | --- | --- | --- |
| [G1] | [actual fields] | [candidate IDs / question IDs] | Same request / later request | [state availability or real dependency] |

Use a compact diagram only if it clarifies actual branching or dependencies. If candidate outputs must satisfy joint constraints, name the code-side check and inconsistent-result behavior.

## Keep as code / rejected leads

| Location | Tempting mapping | Why it should remain unchanged or is unsuitable |
| --- | --- | --- |
| [symbol] | [e.g. Noul from boolean return type] | [exact policy / math / generation / missing evidence / no value] |

## Recommended first pilot

[One candidate, the smallest integration boundary, test data source, baseline, error budget or proposed target, quality/latency/cost measures, fallback rate, and rollback behavior. Label targets as proposals.]

[Close with coverage limits and unanswered questions that materially affect the recommendation.]

## Optional JSON representation

Emit only when requested or needed for another tool. Use null for unknown measurements. Keep `type` limited to `choice`, `score`, and `noul`; represent a composition as several question objects. This is an audit schema, not a Jev API request.

```json
{
  "scope": {"repository": "...", "revision": null, "reviewed": [], "excluded": []},
  "interface": {"verified_at": null, "sources": [], "sdk_version": null},
  "candidates": [
    {
      "id": "J01",
      "locations": [{"path": "...", "symbol": "...", "line": 1}],
      "evidence": [],
      "current_behavior": "...",
      "status": "direct",
      "priority": "high",
      "finding_confidence": "medium",
      "state_fields": [{"field": "...", "origin": "...", "available": true}],
      "questions": [{"id": "...", "type": "noul", "instructions": "..."}],
      "result_policy": "...",
      "batch_group": null,
      "depends_on": [],
      "fallback": "...",
      "benefit_hypothesis": "...",
      "measurements": null,
      "validation": "...",
      "unknowns": []
    }
  ],
  "rejected": [],
  "recommended_pilot": "J01",
  "limitations": []
}
```
