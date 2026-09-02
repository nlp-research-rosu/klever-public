#!/usr/bin/env python3
"""Lexical inventory and task-slice classification for all audited K sources."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction.tZYoqF")
SEMANTICS = ROOT / "reference-semantics"
FILES = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
FILES += [ROOT / "verification.k", ROOT / "spec.k"]

# Inclusive source ranges containing declarations/rules reached by the positive
# task proof or by the concrete task executions. Syntax declarations are also
# separately mapped in REVIEW.md at the constructor level.
USED_RANGES = {
    "semantics/core.k": [
        (13, 60), (68, 70), (117, 127), (130, 181), (183, 225)
    ],
    "semantics/functions.k": [(8, 11), (62, 91)],
    "semantics/call.k": [(15, 75)],
    "semantics/controls.k": [(8, 31), (46, 60), (65, 103)],
    "semantics/operators.k": [(10, 18)],
    "semantics/int.k": [(9, 13), (22, 27)],
    "semantics/list.k": [(12, 20), (52, 55)],
    "semantics/subscript.k": [(6, 41)],
    "semantics/builtins.k": [(17, 26)],
    "semantics/sort.k": [(14, 24), (34, 42)],
    "verification.k": [(6, 34)],
    "spec.k": [(6, 114)],
}

START = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|alias|syntax\s+priorities)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|alias|module|endmodule|"
    r"syntax\s+priorities)\b"
)


def relative(path: Path) -> str:
    if path == ROOT / "verification.k" or path == ROOT / "spec.k":
        return path.name
    return path.relative_to(SEMANTICS).as_posix()


def in_used_range(name: str, line: int) -> bool:
    return any(lo <= line <= hi for lo, hi in USED_RANGES.get(name, []))


def kind_and_attributes(text: str) -> tuple[str, str]:
    first = text.lstrip().split(None, 1)[0]
    recognized = re.compile(
        r"^(?:function|functional|total|concrete|owise|simplification|"
        r"no-evaluators|macro|macro-rec|token|bracket|cell|maincell|exit|"
        r"strict(?:\([^)]*\))?|seqstrict(?:\([^)]*\))?|"
        r"priority\([^)]*\)|symbol\([^)]*\))$"
    )
    attrs = []
    for bracket in re.findall(r"\[([^\[\]]+)\]", text, re.S):
        tokens = [token.strip() for token in bracket.split(",")]
        selected = [token for token in tokens if recognized.match(token)]
        if selected:
            attrs.extend(selected)
    attr_text = "; ".join(attrs)
    if first == "rule":
        if "simplification" in attr_text:
            kind = "simplification-rule"
        elif "priority(" in attr_text:
            kind = "priority-rule"
        elif "concrete" in attr_text:
            kind = "concrete-rule"
        else:
            kind = "ordinary-rule"
    elif first == "syntax":
        if "function" in attr_text or "functional" in attr_text:
            kind = "function-declaration"
        else:
            kind = "syntax-declaration"
    else:
        kind = first
    return kind, attr_text or "-"


def assessment(name: str, line: int, text: str, kind: str) -> str:
    if name == "verification.k":
        if line in (7, 8, 9):
            return "VALID_DEFINITIONAL_ALLINTS"
        if 14 <= line <= 26:
            return "VALID_DEFINITIONAL_STRANGEACC"
        if 31 <= line <= 33:
            return "VALID_MAP_DELETE_SIMPLIFICATION"
    if name == "spec.k":
        return (
            "POSITIVE_LOOP_CONNECTION_CLAIM"
            if line < 58
            else "POSITIVE_ENTRY_CLAIM"
        )
    if "sortVS(ValSeq)" in text and "syntax" in text:
        return "USED_TRUSTED_OPAQUE_SORT_PRIMITIVE"
    if "valSeqAt(ValSeq, Int)" in text and "syntax" in text:
        return "USED_TOTAL_UNDERSPECIFIED_OOB_INBOUNDS_ON_ENTRY_PATH"
    if in_used_range(name, line):
        return "USED_FIXED_RULE_REVIEWED"
    if kind in {"syntax-declaration", "function-declaration"}:
        return "FIXED_DECLARATION_UNUSED_BY_TASK"
    return "FIXED_RULE_UNUSED_BY_TASK"


print("# Exhaustive K sentence inventory")
print()
print(
    "Every outer `configuration`, `syntax`, `context`, `rule`, `claim`, and "
    "`alias` sentence in the mounted supplied tree, `verification.k`, and "
    "`spec.k` is listed below. Continuation lines belong to the preceding row."
)
print()
print("| Source | Lines | Kind | Attributes | Assessment | Normalized sentence |")
print("|---|---:|---|---|---|---|")

totals: dict[str, int] = {}
for path in FILES:
    text = path.read_text()
    lines = text.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    name = relative(path)
    for position, start in enumerate(starts):
        end = len(lines)
        for candidate in range(start + 1, len(lines)):
            if BOUNDARY.match(lines[candidate]):
                end = candidate
                break
        sentence = "\n".join(lines[start:end]).strip()
        kind, attrs = kind_and_attributes(sentence)
        verdict = assessment(name, start + 1, sentence, kind)
        normalized = " ".join(sentence.split()).replace("|", "\\|")
        attrs = attrs.replace("|", "\\|")
        print(
            f"| `{name}` | {start + 1}-{end} | {kind} | `{attrs}` | "
            f"{verdict} | `{normalized}` |"
        )
        totals[kind] = totals.get(kind, 0) + 1

print()
print("## Counts")
print()
for kind in sorted(totals):
    print(f"- {kind}: {totals[kind]}")
print(f"- total: {sum(totals.values())}")
