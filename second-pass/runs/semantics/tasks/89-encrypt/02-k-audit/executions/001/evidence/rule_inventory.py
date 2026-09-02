#!/usr/bin/env python3
"""Produce a deterministic declaration-by-declaration K source inventory."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


BASE = Path("/reference/reference-semantics")
SOURCES = [BASE / "semantics.k", *sorted((BASE / "semantics").glob("*.k"))]
SOURCES += [Path("/candidate/verification.k"), Path("/candidate/spec.k")]
START = re.compile(r"^\s*(configuration|syntax|rule|claim|context|alias)\b")
ATTR = re.compile(
    r"\b(function|total|functional|simplification|macro|concrete|owise|"
    r"priority|strict|seqstrict|symbol|no-evaluators)\b"
)


def relative(path: Path) -> str:
    if path.is_relative_to(BASE):
        return "reference-semantics/" + str(path.relative_to(BASE))
    return str(path)


def disposition(path: Path, line_no: int, kind: str) -> tuple[str, str]:
    if path == Path("/candidate/spec.k"):
        return (
            "entry/auxiliary claim",
            "audited dynamically and for pre/postcondition adequacy",
        )
    if path == Path("/candidate/verification.k"):
        if line_no in {9, 13, 14, 15, 23, 24}:
            return (
                "definitional summary",
                "truthful structural/math equation; disjoint coverage and descent checked",
            )
        if line_no in {28, 47, 55}:
            return (
                "source macro",
                "expanded AST checked textually against submitted solution.mpy",
            )
        if line_no == 66:
            return (
                "operational bridge",
                "loop execution summary; complete-context connection audited separately",
            )
        return (
            "proof-local syntax",
            "declaration attributes and result influence audited separately",
        )

    # The exact candidate tree was recursively byte-compared with this trusted
    # supplied baseline. It is the fixed semantics level, not a proof-local
    # extension. Relevance of the actually exercised subset is mapped in
    # REVIEW.md and 05_used_constructs.md.
    return (
        "fixed supplied semantics",
        "unchanged trusted baseline; used-path behavior reviewed, unused rule outside theorem path",
    )


rows = []
kind_counts: Counter[str] = Counter()
file_counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()

for source in SOURCES:
    lines = source.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, START.match(line))
        for index, line in enumerate(lines)
        if START.match(line)
    ]
    for position, (index, match) in enumerate(starts):
        assert match is not None
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        # Stop before a module boundary. Comments are retained only if they
        # occur inside a declaration block and are harmless in the synopsis.
        for offset, block_line in enumerate(block_lines[1:], start=1):
            if re.match(r"^\s*(?:end)?module\b", block_line):
                block_lines = block_lines[:offset]
                break
        flattened = " ".join(
            part.strip()
            for part in block_lines
            if part.strip() and not part.lstrip().startswith("//")
        )
        if len(flattened) > 300:
            flattened = flattened[:297] + "..."
        declaration_text = " ".join(
            part for part in block_lines if not part.lstrip().startswith("//")
        )
        attrs = sorted(set(ATTR.findall(declaration_text)))
        kind = match.group(1)
        role, decision = disposition(source, index + 1, kind)
        rows.append(
            (
                relative(source),
                index + 1,
                kind,
                ",".join(attrs) if attrs else "-",
                role,
                decision,
                flattened,
            )
        )
        kind_counts[kind] += 1
        file_counts[relative(source)] += 1
        attribute_counts.update(attrs)

print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Generated from the trusted supplied semantics tree plus the candidate's "
    "proof-local sources. Each row identifies the exact source line."
)
print()
print(f"Total inventoried declarations: {len(rows)}")
print()
print("## Counts by kind")
print()
for key in sorted(kind_counts):
    print(f"- {key}: {kind_counts[key]}")
print()
print("## Counts by source")
print()
for key in sorted(file_counts):
    print(f"- `{key}`: {file_counts[key]}")
print()
print("## Attributes observed")
print()
for key in sorted(attribute_counts):
    print(f"- {key}: {attribute_counts[key]}")
print()
print("## Rule-by-rule inventory")
print()
print("| Source | Line | Kind | Attributes | Role | Audit disposition | Synopsis |")
print("|---|---:|---|---|---|---|---|")
for source, line_no, kind, attrs, role, decision, synopsis in rows:
    synopsis = synopsis.replace("|", "\\|")
    decision = decision.replace("|", "\\|")
    print(
        f"| `{source}` | {line_no} | {kind} | {attrs} | {role} | "
        f"{decision} | `{synopsis}` |"
    )
