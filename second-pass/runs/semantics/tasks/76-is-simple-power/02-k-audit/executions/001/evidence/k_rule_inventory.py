#!/usr/bin/env python3
"""Create a source-level inventory of K declarations, rules, and claims.

This is deliberately source-oriented: it inventories every top-level syntax
declaration and rule in the supplied semantics tree, then the candidate-local
verification/specification sources.  Multi-line items are rendered on one line
while retaining their exact source span.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/76-is-simple-power/candidate-source")
SEMANTICS = ROOT / "reference-semantics"

files = [SEMANTICS / "semantics.k", *sorted((SEMANTICS / "semantics").glob("*.k"))]
files.extend([ROOT / "verification.k", ROOT / "spec.k"])

start_re = re.compile(r"^\s*(configuration|syntax|rule|claim|context)\b")
boundary_re = re.compile(
    r"^\s*(?:requires\s+\"|module\b|endmodule\b|imports\b|"
    r"configuration\b|syntax\b|rule\b|claim\b|context\b)"
)

local_assessments = {
    ("verification.k", 11): (
        "VALID_DEFINITION: X=1 is the zero-exponent case and the program's "
        "first return; guard is disjoint."
    ),
    ("verification.k", 13): (
        "VALID_DEFINITION: X<1 is rejected by the program; guard is disjoint."
    ),
    ("verification.k", 15): (
        "VALID_PROGRAM_SUMMARY: for X>1,N<=1 the program's third guard returns "
        "false. This is not a universal mathematical characterization for "
        "negative bases; intent adequacy is assessed separately."
    ),
    ("verification.k", 17): (
        "VALID_DEFINITION: positive X and N enter the repeated-division "
        "summary; the guard completes the disjoint simplePower partition."
    ),
    ("verification.k", 20): (
        "VALID_RECURSIVE_EQUATION: when pyMod is zero, the concrete loop body "
        "updates x to X /Int N. On the entry domain X>1,N>1 it strictly descends."
    ),
    ("verification.k", 22): (
        "VALID_RECURSIVE_EQUATION: when pyMod is nonzero, the concrete loop "
        "exits and returns the Boolean X==1. Guard is complementary to line 20."
    ),
    ("verification.k", 28): "VALID_MACRO: exact solution.mpy condition AST.",
    ("verification.k", 32): "VALID_MACRO: exact solution.mpy assignment AST.",
    ("verification.k", 36): "VALID_MACRO: exact solution.mpy result AST.",
    ("verification.k", 40): "VALID_MACRO: exact solution.mpy while AST.",
    ("verification.k", 43): "VALID_MACRO: exact solution.mpy function body AST.",
    ("verification.k", 54): (
        "VALID_MACRO: exact solution.mpy module AST; independently checked by "
        "expanded-KORE identity."
    ),
}


def flatten(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


records: list[tuple[Path, int, int, str, str]] = []
for path in files:
    lines = path.read_text().splitlines()
    starts = [i for i, line in enumerate(lines) if start_re.match(line)]
    for position, start in enumerate(starts):
        limit = starts[position + 1] if position + 1 < len(starts) else len(lines)
        end = start + 1
        while end < limit and not boundary_re.match(lines[end]):
            end += 1
        text = flatten(lines[start:end])
        kind = start_re.match(lines[start]).group(1)  # type: ignore[union-attr]
        records.append((path, start + 1, end, kind, text))

print(
    "ID\tKIND\tSOURCE\tSPAN\tATTRIBUTES/CLASS\tASSESSMENT\tTEXT"
)
kind_counts: dict[str, int] = {}
for number, (path, start, end, kind, text) in enumerate(records, 1):
    kind_counts[kind] = kind_counts.get(kind, 0) + 1
    rel = path.relative_to(ROOT).as_posix()
    attrs = []
    for name in (
        "function",
        "total",
        "functional",
        "macro",
        "simplification",
        "symbol",
        "owise",
        "priority",
        "strict",
        "seqstrict",
        "hook",
    ):
        if re.search(rf"\b{re.escape(name)}\b", text):
            attrs.append(name)
    if kind == "rule" and not any(
        name in attrs for name in ("simplification", "owise", "priority")
    ):
        attrs.append("ordinary-rule")
    if rel.startswith("reference-semantics/"):
        assessment = (
            "ACCEPTED_SUPPLIED_BASELINE: byte-identical to the trusted mounted "
            "semantics; no candidate-local extension. Used-path fidelity is "
            "reviewed separately."
        )
    elif rel == "verification.k":
        assessment = local_assessments.get(
            ("verification.k", start),
            "DECLARATION: candidate-local item; paired rules are assessed by span.",
        )
    else:
        assessment = "CLAIM/DECLARATION: adequacy and closure assessed separately."
    print(
        f"K{number:04d}\t{kind}\t{rel}\t{start}-{end}\t"
        f"{','.join(attrs) or '-'}\t{assessment}\t{text}"
    )

print("\nSUMMARY")
print(f"files={len(files)}")
print(f"records={len(records)}")
for kind in sorted(kind_counts):
    print(f"{kind}={kind_counts[kind]}")
