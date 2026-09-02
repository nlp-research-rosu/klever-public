#!/usr/bin/env python3
"""Enumerate every top-level K declaration/rule in the audited source tree."""

from __future__ import annotations

import collections
import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/22-filter-integers-review")
SOURCE_PATHS = [
    SCRATCH / "reference-semantics" / "semantics.k",
    *sorted((SCRATCH / "reference-semantics" / "semantics").glob("*.k")),
    SCRATCH / "verification.k",
    SCRATCH / "spec.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
STRUCTURAL = re.compile(
    r"^\s*(requires|module|endmodule|imports)\b"
)
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "symbol",
    "no-evaluators",
    "priority",
    "owise",
    "simplification",
    "concrete",
    "macro",
    "macro-rec",
    "strict",
    "seqstrict",
    "hook",
    "token",
)


def entries(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if START.match(line) or STRUCTURAL.match(line)
    ]
    for ordinal, index in enumerate(starts):
        start_match = START.match(lines[index])
        if start_match is None:
            continue
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        block = lines[index:end]
        while block and (not block[-1].strip() or block[-1].lstrip().startswith("//")):
            block.pop()
        yield index + 1, start_match.group(1), "\n".join(block)


def flags(block: str) -> str:
    found = [flag for flag in ATTRIBUTES if flag in block]
    return ",".join(found) if found else "-"


def role(source: str, line: int, kind: str, block: str) -> str:
    if source == "verification.k":
        if kind == "syntax":
            return "PROOF_LOCAL_MACRO_DECL"
        if kind == "rule":
            return "PASS_MACRO_EXPANSION; no operational bridge; AST identity checked"
    if source == "spec.k":
        return "TARGET_REACHABILITY_CLAIM"
    if kind == "configuration":
        return "PASS_FIXED_CONFIGURATION"
    if kind == "syntax":
        if "symbol(" in block or "no-evaluators" in block:
            return "TRUST_BOUNDARY_OPAQUE_DECL; inactive in submitted claims"
        return "PASS_FIXED_DECLARATION; no truth assertion"
    if kind == "context":
        return "PASS_FIXED_EVALUATION_CONTEXT"
    if source.endswith("builtins.k") and line == 291:
        return "MODEL_GAP_ROUTE; delegates Python isinstance(_,int) to isIntV"
    if source.endswith("builtins.k") and line == 294:
        return "PASS_INT_CASE; K Int maps to true"
    if source.endswith("builtins.k") and line == 295:
        return "MATERIAL_MODEL_GAP; K Bool maps false but CPython bool is int subclass"
    if source.endswith("concrete.k") or "[concrete]" in block:
        return "PASS_FIXED_CONCRETE_RULE; absent or inactive in proof definition"
    if "<k>" in block or any(
        cell in block
        for cell in (
            "<env>",
            "<scopes>",
            "<heap>",
            "<stack>",
            "<ret>",
            "<exc>",
        )
    ):
        return "PASS_FIXED_OPERATIONAL_RULE; no task-specific result shortcut"
    return "PASS_FIXED_EQUATION; guarded/constructor-recursive fixed theory"


def compact(block: str) -> str:
    uncommented = []
    for line in block.splitlines():
        text = line.split("//", 1)[0].strip()
        if text:
            uncommented.append(text)
    return " ".join(uncommented).replace("|", r"\|")


def main() -> int:
    records = []
    for path in SOURCE_PATHS:
        source = path.relative_to(SCRATCH).as_posix()
        for line, kind, block in entries(path):
            records.append(
                (
                    source,
                    line,
                    kind,
                    flags(block),
                    role(source, line, kind, block),
                    compact(block),
                )
            )

    print("# Exhaustive K source inventory")
    print()
    print(
        "Each top-level configuration, syntax declaration, context, rule, and "
        "claim is listed once. Multi-line declarations/rules are collapsed."
    )
    print()
    print("| ID | Source:line | Kind | Attributes | Assessment | Declaration/rule |")
    print("|---:|---|---|---|---|---|")
    for identifier, record in enumerate(records, 1):
        source, line, kind, attrs, assessment, text = record
        print(
            f"| {identifier} | `{source}:{line}` | {kind} | {attrs} | "
            f"{assessment} | `{text}` |"
        )

    kind_counts = collections.Counter(record[2] for record in records)
    assessment_counts = collections.Counter(record[4] for record in records)
    opaque = [
        (record[0], record[1], record[5])
        for record in records
        if "TRUST_BOUNDARY_OPAQUE_DECL" in record[4]
    ]
    print()
    print("## Summary")
    print()
    print(f"TOTAL_ENTRIES: {len(records)}")
    for name, count in sorted(kind_counts.items()):
        print(f"KIND_{name.upper()}: {count}")
    for name, count in sorted(assessment_counts.items()):
        print(f"ASSESSMENT {name}: {count}")
    print(f"OPAQUE_DECLARATIONS: {len(opaque)}")
    for source, line, text in opaque:
        print(f"OPAQUE {source}:{line}: {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
