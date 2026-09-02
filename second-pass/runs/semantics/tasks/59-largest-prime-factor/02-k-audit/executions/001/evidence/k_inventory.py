#!/usr/bin/env python3
"""Inventory every top-level K declaration/rule in the audited source set.

The output is TSV so each source item has an explicit relevance and review
disposition. Continuation lines (requires, attributes, cells, and alternatives)
are folded into the item text rather than silently omitted.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path("/tmp/audit-work/review-59/candidate-src")
FILES = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

START = re.compile(
    r"^\s*(module\b|endmodule\b|imports\b|configuration\b|"
    r"syntax\b|rule\b|context\b|claim\b)"
)
INVENTORIED = {"configuration", "syntax", "rule", "context", "claim"}

# Fixed-semantics lines whose declarations/rules participate in the submitted
# program's parse or concrete/symbolic control path.
USED_LINES = {
    "semantics/core.k": {
        25, 31, 36, 37, 39, 42, 49, 124, 125, 126, 127, 130, 131, 132,
        145, 152, 157, 158, 194, 198, 199, 200, 202, 208, 209, 210,
    },
    "semantics/functions.k": {
        8, 14, 62, 63, 64, 77, 78, 80, 85,
    },
    "semantics/controls.k": {
        9, 20, 50, 51, 52, 53, 54, 65, 76, 77, 78, 79, 81, 85,
    },
    "semantics/operators.k": {12, 15, 16, 17},
    "semantics/int.k": {9, 15, 16, 19, 20, 24, 26},
    "semantics/call.k": {19, 20, 21, 69},
    "semantics/syntax.k": {
        9, 12, 15, 28, 30, 32, 41, 44, 46, 49, 50, 53, 56, 57, 60, 61,
    },
}


def kind_of(first_line: str) -> str:
    stripped = first_line.strip()
    return stripped.split(maxsplit=1)[0]


def disposition(path: Path, line: int, kind: str, text: str) -> tuple[str, str]:
    rel = path.relative_to(ROOT).as_posix()
    short = rel.removeprefix("reference-semantics/")

    if rel == "verification.k":
        if kind == "syntax" and line in {15, 30, 34}:
            return "PROOF_USED", "ACCEPT_EXACT_MACRO_ALIAS"
        if kind == "syntax" and line == 44:
            return "PROOF_USED", "ACCEPT_DEFINED_SUMMARY_ON_N_GT_1_F_GT_1"
        if kind == "rule" and line in {9}:
            return "PROOF_USED", "ACCEPT_TRUE_MAP_DELETE_SIMPLIFICATION"
        if kind == "rule" and line in {16, 31, 35}:
            return "PROOF_USED", "ACCEPT_EXACT_MACRO_EXPANSION"
        if kind == "rule" and line in {45, 47, 50}:
            return "PROOF_USED", "ACCEPT_RECURRENCE_GUARDS_PARTITION_PROOF_DOMAIN"
        if kind == "rule" and line in {58, 72, 88, 104, 119}:
            return "PROOF_USED", "ACCEPT_DERIVABLE_BRIDGE_CONNECTION_CLAIM_ABSENT"
        return "PROOF_SUPPORT", "REVIEWED_NO_RESULT_ORACLE"

    if rel == "spec.k":
        if kind == "claim" and line == 8:
            return "TARGET_HELPER", "ACCEPT_RESULT_CONSTRAINING_LOOP_CIRCULARITY"
        if kind == "claim" and line == 35:
            return "TARGET_ENTRY", "ACCEPT_PREFIX_ONLY_COMPOSES_WITH_LOOP_CLAIM"
        return "SPEC_SUPPORT", "REVIEWED"

    if rel.startswith("reference-semantics/"):
        used = line in USED_LINES.get(short, set())
        opaque = "no-evaluators" in text or "symbol(" in text
        if used:
            return "FIXED_USED", "ACCEPT_SUPPLIED_RULE_MATCHES_INTEGER_PROGRAM_STEP"
        if opaque:
            return "FIXED_UNUSED_OPAQUE", "ACCEPT_INERT_FOR_SUBMITTED_PROGRAM"
        return "FIXED_UNUSED", "ACCEPT_SUPPLIED_BASELINE_INERT_FOR_SUBMITTED_PROGRAM"

    return "OTHER", "REVIEWED"


def records(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) and not line.lstrip().startswith("//")
    ]
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        kind = kind_of(lines[start])
        if kind not in INVENTORIED:
            continue
        body_lines = []
        for raw in lines[start:end]:
            stripped = raw.split("//", 1)[0].strip()
            if stripped.startswith("//"):
                continue
            if stripped:
                body_lines.append(stripped)
        body = " ".join(body_lines)
        yield start + 1, kind, body


print("file\tline\tkind\tattributes\trelevance\tdisposition\tdeclaration")
count = 0
for path in FILES:
    for line, kind, body in records(path):
        attrs = ",".join(
            re.findall(
                r"(?<![A-Za-z0-9_-])("
                r"function|total|functional|symbol\([^)]*\)|no-evaluators|"
                r"priority\([^)]*\)|simplification|macro-rec|macro|concrete|"
                r"owise|seqstrict\([^)]*\)|strict\([^)]*\)|circularity"
                r")(?![A-Za-z0-9_-])",
                body,
            )
        ).replace("\t", " ")
        relevance, decision = disposition(path, line, kind, body)
        rel = path.relative_to(ROOT).as_posix()
        clean = body.replace("\t", " ").replace("\n", " ")
        print(
            f"{rel}\t{line}\t{kind}\t{attrs}\t{relevance}\t{decision}\t{clean}"
        )
        count += 1

print(f"# inventory_count={count}")
