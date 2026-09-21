# Examples

A worked, end-to-end illustration of the **find-jevable-code** skill.

| File | Role |
| --- | --- |
| [`sample-repo/support_router.py`](sample-repo/support_router.py) | **Input** — a toy support-ticket router that approximates meaning with keyword lists and hand-tuned weights. This is the kind of code the skill audits. |
| [`audit-report.md`](audit-report.md) | **Output** — the jevability audit the skill produces for that file: three ranked candidates (Choice / Score / Noul), a composition group, rejected leads, and one pilot. |

The report is illustrative — no Jev API call was made, and every threshold and
benefit is labeled as a hypothesis. Line references in the report point at real
lines in `support_router.py`, which is exactly the source-grounding the skill
requires.

To try it yourself, from a Claude Code or Codex session in this repo:

> Use find-jevable-code to audit `examples/sample-repo` for Jev opportunities.
