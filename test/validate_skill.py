#!/usr/bin/env python3
"""Validate the jevable-code skill package.

Stdlib only. Checks that the package stays internally consistent so it keeps
working in BOTH Claude Code and Codex:

  * SKILL.md has valid frontmatter: kebab-case `name` matching the skill dir,
    a bounded `description`, and NO other keys (the portable cross-vendor rule).
  * agents/openai.yaml carries the Codex/OpenAI interface keys and a real icon.
  * both plugin manifests are valid JSON and point at the skill folder.
  * every local link in SKILL.md and the references resolves on disk.
  * the worked example's line references still point at real source lines.

Run:  python3 test/validate_skill.py       (exit 0 = pass, 1 = fail)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "find-jevable-code"
SKILL = ROOT / "skills" / SKILL_NAME
errors: list[str] = []
checks = 0


def check(cond: bool, msg: str) -> None:
    global checks
    checks += 1
    if not cond:
        errors.append(msg)


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# --- SKILL.md frontmatter -------------------------------------------------
skill_md = read(SKILL / "SKILL.md")
m = re.match(r"^---\n(.*?)\n---\n", skill_md, re.DOTALL)
check(m is not None, "SKILL.md: missing YAML frontmatter block")
if m:
    fm = m.group(1)
    top_keys = re.findall(r"^([A-Za-z0-9_-]+):", fm, re.MULTILINE)
    check(set(top_keys) <= {"name", "description"},
          f"SKILL.md: only name+description are portable; found {top_keys}")

    name = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
    check(bool(name), "SKILL.md: frontmatter missing `name`")
    if name:
        n = name.group(1).strip()
        check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n) is not None,
              f"SKILL.md: name '{n}' is not kebab-case")
        check(len(n) <= 64, f"SKILL.md: name '{n}' exceeds 64 chars")
        check(n == SKILL.name, f"SKILL.md: name '{n}' must match dir '{SKILL.name}'")

    desc = re.search(r"^description:\s*(.+?)(?=^\S|\Z)", fm, re.MULTILINE | re.DOTALL)
    check(bool(desc), "SKILL.md: frontmatter missing `description`")
    if desc:
        text = " ".join(desc.group(1).split())
        check(len(text) <= 1024, f"SKILL.md: description is {len(text)} chars (>1024)")
        check(len(text) >= 40, "SKILL.md: description is suspiciously short")

# body length (portability guideline: keep it lean)
body_lines = skill_md.count("\n")
check(body_lines <= 500, f"SKILL.md: {body_lines} lines (>500 portability budget)")


# --- local links resolve --------------------------------------------------
LINK = re.compile(r"\]\((?!https?://|#)([^)]+)\)")
link_files = [SKILL / "SKILL.md"]
link_files += sorted((SKILL / "references").glob("*.md"))
link_files += [ROOT / "README.md", ROOT / "examples" / "README.md",
               ROOT / "examples" / "audit-report.md"]
for f in link_files:
    if not f.exists():
        check(False, f"expected file missing: {f.relative_to(ROOT)}")
        continue
    for target in LINK.findall(read(f)):
        path = (f.parent / target.split("#", 1)[0]).resolve()
        check(path.exists(), f"{f.relative_to(ROOT)}: broken local link -> {target}")


# --- openai.yaml (Codex/OpenAI manifest) ----------------------------------
oy = read(SKILL / "agents" / "openai.yaml")
for key in ("display_name", "short_description", "default_prompt"):
    check(re.search(rf"^\s*{key}:", oy, re.MULTILINE) is not None,
          f"openai.yaml: missing interface key `{key}`")
check("codex" in oy and "chatgpt" in oy,
      "openai.yaml: policy.products should list codex + chatgpt")
for icon in re.findall(r"icon_\w+:\s*(\S+)", oy):
    check((SKILL / icon).exists(), f"openai.yaml: icon path does not exist -> {icon}")


# --- plugin manifests -----------------------------------------------------
for rel, extra in [(".claude-plugin/plugin.json", None),
                   (".codex-plugin/plugin.json", "skills")]:
    p = ROOT / rel
    check(p.exists(), f"missing manifest: {rel}")
    if not p.exists():
        continue
    try:
        data = json.loads(read(p))
    except json.JSONDecodeError as e:
        check(False, f"{rel}: invalid JSON ({e})")
        continue
    check("name" in data, f"{rel}: missing `name`")
    if extra == "skills":
        skills_dir = (p.parent.parent / data.get("skills", "")).resolve()
        check(skills_dir.is_dir(), f"{rel}: skills path not a dir -> {data.get('skills')}")
        check((skills_dir / SKILL_NAME / 'SKILL.md').exists(),
              f"{rel}: skills path does not contain {SKILL_NAME}/SKILL.md")


# --- referenced assets exist ----------------------------------------------
for rel in ["assets/icon.svg", "assets/architecture.svg"]:
    check((SKILL / rel).exists(), f"missing asset: skills/{SKILL_NAME}/{rel}")


# --- example line references stay grounded --------------------------------
src = ROOT / "examples" / "sample-repo" / "support_router.py"
n_lines = len(read(src).splitlines())
report = read(ROOT / "examples" / "audit-report.md")
cited = re.findall(r"support_router\.py:(\d+)", report)
check(len(cited) > 0, "audit-report.md: expected grounded line references, found none")
for ln in cited:
    check(1 <= int(ln) <= n_lines,
          f"audit-report.md: cites support_router.py:{ln} but file has {n_lines} lines")


# --- report ---------------------------------------------------------------
if errors:
    print(f"FAIL — {len(errors)} problem(s) across {checks} checks:\n")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
print(f"OK — {checks} checks passed.")
