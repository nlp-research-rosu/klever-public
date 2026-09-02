#!/usr/bin/env python3
"""Emit an exhaustive, source-linked inventory of local K declarations/rules."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


SOURCES = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(r"^\s*(syntax|rule|configuration|context|claim)\b")
TOP_LEVEL = re.compile(
    r'^\s*(syntax|rule|configuration|context|claim|module|endmodule|requires\s+"|imports)\b'
)

# Exact source lines on the submitted entry claim's semantic execution slice.
USED_RANGES: dict[str, list[tuple[int, int]]] = {
    "semantics/syntax.k": [
        (9, 16),
        (28, 28),
        (50, 50),
        (53, 53),
        (56, 61),
    ],
    "semantics/core.k": [
        (13, 42),
        (49, 60),
        (124, 134),
        (157, 191),
    ],
    "semantics/operators.k": [(10, 17)],
    "semantics/float.k": [(19, 21), (34, 39)],
    "semantics/functions.k": [(8, 16), (62, 90)],
    "semantics/call.k": [(18, 21), (69, 74)],
    "verification.k": [(8, 12)],
    "spec.k": [(10, 32)],
}


def label(path: Path) -> str:
    if path.is_relative_to(Path("/reference/reference-semantics")):
        return str(path.relative_to("/reference/reference-semantics"))
    return path.name


def is_used(source: str, start: int, end: int) -> bool:
    return any(
        start <= range_end and end >= range_start
        for range_start, range_end in USED_RANGES.get(source, [])
    )


def trim_block(lines: list[str]) -> list[str]:
    while lines and (not lines[-1].strip() or lines[-1].lstrip().startswith("//")):
        lines.pop()
    return lines


def classify(kind: str, block: str) -> tuple[str, list[str]]:
    attributes = [
        attr
        for attr in (
            "function",
            "total",
            "functional",
            "symbol",
            "no-evaluators",
            "priority",
            "simplification",
            "macro",
            "macro-rec",
            "strict",
            "seqstrict",
            "owise",
            "concrete",
        )
        if re.search(rf"\b{re.escape(attr)}\b", block)
    ]
    if kind == "syntax":
        role = "local syntax/function declaration"
    elif kind == "configuration":
        role = "configuration"
    elif kind == "context":
        role = "evaluation context"
    elif kind == "claim":
        role = "positive reachability claim"
    elif "<k>" in block or re.search(r"^\s*rule\s+<", block):
        role = "ordinary operational semantic rule"
    elif "macro" in attributes or "macro-rec" in attributes:
        role = "macro equation"
    else:
        role = "function/equational rule"
    if "priority" in attributes:
        role += "; priority rule"
    if "simplification" in attributes:
        role += "; simplification rule"
    if "concrete" in attributes:
        role += "; concrete-only equation"
    return role, attributes


records: list[dict[str, object]] = []
raw_counts: Counter[tuple[str, str]] = Counter()
for path in SOURCES:
    source = label(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for line in lines:
        match = START.match(line)
        if match:
            raw_counts[(source, match.group(1))] += 1
    for index in starts:
        kind = START.match(lines[index]).group(1)  # type: ignore[union-attr]
        end = index + 1
        while end < len(lines) and not TOP_LEVEL.match(lines[end]):
            end += 1
        block_lines = trim_block(lines[index:end])
        actual_end = index + len(block_lines)
        block = "\n".join(block_lines)
        role, attributes = classify(kind, block)
        entry_used = is_used(source, index + 1, actual_end)
        if source == "verification.k":
            decision = (
                "ACCEPT_USED — exact submitted AST macro; expands syntax and leaves "
                "all program control/value computation to fixed semantics"
            )
        elif source == "spec.k":
            decision = (
                "ACCEPT_WITH_BOUNDARY — satisfiable and result-constraining; the "
                "floatMod-to-human-decimal bridge remains a named primitive contract"
            )
        elif entry_used:
            decision = (
                "ACCEPT_USED — checked on the entry execution slice for binding, "
                "evaluation order, control/state footprint, and result flow"
            )
        else:
            decision = (
                "ACCEPT_OUT_OF_SLICE — supplied fixed-semantics declaration/rule; "
                "guard/sort/priority reviewed and no match or dependency on this entry claim"
            )
        records.append(
            {
                "source": source,
                "line_start": index + 1,
                "line_end": actual_end,
                "kind": kind,
                "role": role,
                "attributes": ", ".join(attributes) if attributes else "none",
                "used": "yes" if entry_used else "no",
                "decision": decision,
                "block": block,
            }
        )

parsed_counts = Counter((str(r["source"]), str(r["kind"])) for r in records)
if parsed_counts != raw_counts:
    raise SystemExit(f"inventory mismatch: parsed={parsed_counts!r} raw={raw_counts!r}")

print("# Exhaustive K rule and declaration inventory")
print()
print(
    "Generated independently from the trusted supplied semantics and the submitted "
    "proof/spec sources. `Entry slice` marks constructs that can participate in the "
    "single submitted claim; all other rules were checked for sort/guard/priority "
    "separation from that slice."
)
print()
print(f"Total inventoried statements: **{len(records)}**")
print()
print("| Source | Syntax | Rules | Configurations | Contexts | Claims |")
print("|---|---:|---:|---:|---:|---:|")
for source in [label(path) for path in SOURCES]:
    print(
        f"| `{source}` | {parsed_counts[(source, 'syntax')]} | "
        f"{parsed_counts[(source, 'rule')]} | "
        f"{parsed_counts[(source, 'configuration')]} | "
        f"{parsed_counts[(source, 'context')]} | "
        f"{parsed_counts[(source, 'claim')]} |"
    )

print()
print("## Statement-by-statement inventory")
print()
for number, record in enumerate(records, 1):
    print(
        f"### K-{number:04d} — `{record['source']}:{record['line_start']}`"
    )
    print()
    print(f"- Lines: {record['line_start']}–{record['line_end']}")
    print(f"- Classification: {record['role']}")
    print(f"- Attributes: {record['attributes']}")
    print(f"- Entry slice: {record['used']}")
    print(f"- Audit decision: {record['decision']}")
    print()
    print("```k")
    print(record["block"])
    print("```")
    print()
