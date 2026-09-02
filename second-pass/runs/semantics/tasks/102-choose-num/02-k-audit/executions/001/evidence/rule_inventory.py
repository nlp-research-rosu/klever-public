#!/usr/bin/env python3
"""Mechanical inventory of every local K declaration/rule in the audit inputs."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/102-choose-num")
SEMANTICS = SCRATCH / "reference-semantics"
FILES = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
FILES += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

START = re.compile(
    r"^(requires|module|endmodule)\b|^  (imports|configuration|syntax|context|rule|claim)\b"
)
KIND = START
ATTR = re.compile(
    r"\b(function|total|functional|simplification|concrete|owise|macro|strict|"
    r"seqstrict|priority|symbol|no-evaluators)\b"
)


def statement_entries(path: Path):
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[start:end]:
            stripped = line.strip()
            if stripped.startswith("//") or not stripped:
                continue
            block_lines.append(stripped)
        text = " ".join(block_lines)
        match = KIND.match(lines[start])
        if match:
            yield start + 1, end, next(group for group in match.groups() if group), text


def on_program_path(rel: str, line: int, kind: str) -> str:
    if kind in {"requires", "module", "imports", "endmodule", "syntax", "configuration", "context"}:
        return "DECLARATION/STRUCTURE"
    if rel == "verification.k":
        return "PROOF-LOCAL/PATH"
    if rel == "spec.k":
        return "ENTRY-CLAIM"
    used_ranges = {
        "reference-semantics/semantics/core.k": [
            (125, 127), (131, 154), (185, 210), (213, 215)
        ],
        "reference-semantics/semantics/operators.k": [(10, 20)],
        "reference-semantics/semantics/int.k": [
            (7, 7), (13, 16), (19, 27)
        ],
        "reference-semantics/semantics/controls.k": [(51, 54)],
        "reference-semantics/semantics/functions.k": [(63, 90)],
        "reference-semantics/semantics/call.k": [(18, 21), (69, 75)],
    }
    if any(lo <= line <= hi for lo, hi in used_ranges.get(rel, [])):
        return "FIXED-SUPPLIED/PATH"
    return "FIXED-SUPPLIED/UNREACHABLE"


def decision(classification: str, kind: str) -> str:
    if kind in {"requires", "module", "imports", "endmodule", "syntax", "configuration", "context"}:
        return "ACCEPT: declaration/configuration; no answer-producing equation"
    if classification == "PROOF-LOCAL/PATH":
        return "AUDIT: proof extension; justified individually in REVIEW.md"
    if classification == "ENTRY-CLAIM":
        return "AUDIT: theorem obligation; adequacy/non-vacuity checked in REVIEW.md"
    if classification == "FIXED-SUPPLIED/PATH":
        return "ACCEPT: fixed rule; checked against the used Python-int execution path"
    return (
        "NO PATH EFFECT: fixed supplied rule cannot match this program's reachable "
        "terms; no intended-domain false-conclusion witness"
    )


rows = []
for path in FILES:
    rel = (
        str(path.relative_to(SCRATCH))
        if path.is_relative_to(SCRATCH)
        else str(path)
    )
    for line, end, kind, text in statement_entries(path):
        classification = on_program_path(rel, line, kind)
        attrs = ",".join(sorted(set(ATTR.findall(text)))) or "-"
        rows.append(
            (rel, line, end, kind, attrs, classification, decision(classification, kind), text)
        )

print("# Exhaustive local K declaration and rule inventory")
print()
print(
    "Decision codes are theorem-relative. `FIXED-SUPPLIED/UNREACHABLE` means the "
    "rule is part of the byte-identical trusted baseline but cannot match any "
    "term/value reachable from this integer-only function. It is not asserted "
    "to model all of Python beyond that path."
)
print()
print(f"Inventory entries: {len(rows)}")
print()
print("| # | source | lines | kind | attributes | classification | decision | normalized declaration/rule |")
print("|---:|---|---:|---|---|---|---|---|")
for index, (rel, line, end, kind, attrs, classification, verdict, text) in enumerate(rows, 1):
    safe_text = text.replace("|", "&#124;").replace("`", "\\`")
    safe_verdict = verdict.replace("|", "&#124;")
    print(
        f"| {index} | `{rel}` | {line}-{end} | {kind} | `{attrs}` | "
        f"{classification} | {safe_verdict} | `{safe_text}` |"
    )

print()
print("## Counts")
print()
for kind in sorted({row[3] for row in rows}):
    print(f"- {kind}: {sum(row[3] == kind for row in rows)}")
for classification in sorted({row[5] for row in rows}):
    print(f"- {classification}: {sum(row[5] == classification for row in rows)}")
