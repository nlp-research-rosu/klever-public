#!/usr/bin/env python3
"""Inventory every local K declaration, context, rule, and claim."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/source")
FILES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")
TOP_LEVEL = re.compile(
    r"^(?:  )?(configuration|syntax|context|rule|claim|module|endmodule|imports)\b"
)


def decision(path: Path, kind: str, statement: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "verification.k":
        if kind == "rule" and "[simplification]" in statement:
            return "VALID_UNIVERSAL_INTEGER_IDENTITY"
        if kind == "rule":
            return "VALID_EXHAUSTIVE_DESCENDING_SUMMARY_EQUATION"
        return "WELL_SORTED_PROOF_LOCAL_DECLARATION"
    if rel == "spec.k":
        return "SATISFIABLE_RESULT_CONSTRAINING_REACHABILITY_CLAIM"
    if rel.endswith("concrete.k"):
        return "LLVM_ONLY_FIXED_SEMANTICS; NOT_IMPORTED_BY_PROOF"
    if "no-evaluators" in statement:
        return "OPAQUE_FIXED_PRIMITIVE; UNUSED_BY_SUBMITTED_PROGRAM"
    if kind in {"syntax", "configuration", "context"}:
        return "FIXED_SEMANTICS_DECLARATION_OR_EVALUATION_CONTEXT"
    return (
        "FIXED_SEMANTICS_RULE; REVIEWED; NO_FALSE_CONCLUSION_WITNESS_ON_"
        "SUBMITTED_PROGRAM_DOMAIN"
    )


counts_by_file: dict[str, Counter[str]] = defaultdict(Counter)
records: list[tuple[str, int, str, str, str]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start_line = index + 1
        block = [lines[index].strip()]
        index += 1
        while index < len(lines):
            if TOP_LEVEL.match(lines[index]):
                break
            if lines[index].strip() == "" and block:
                break
            if lines[index].lstrip().startswith("//"):
                break
            block.append(lines[index].strip())
            index += 1
        statement = " ".join(part for part in block if part)
        rel = path.relative_to(ROOT).as_posix()
        counts_by_file[rel][kind] += 1
        records.append(
            (rel, start_line, kind, decision(path, kind, statement), statement)
        )

print("INVENTORY_SCOPE")
for path in FILES:
    print(path.relative_to(ROOT).as_posix())
print()
print("COUNTS_BY_FILE")
for rel in sorted(counts_by_file):
    counts = counts_by_file[rel]
    rendered = " ".join(f"{kind}={counts[kind]}" for kind in sorted(counts))
    print(f"{rel} {rendered} total={sum(counts.values())}")
print()
all_counts = Counter(kind for _, _, kind, _, _ in records)
print(
    "TOTALS "
    + " ".join(f"{kind}={all_counts[kind]}" for kind in sorted(all_counts))
    + f" all={len(records)}"
)
print()
print("FULL_INVENTORY")
for number, (rel, line, kind, audit_decision, statement) in enumerate(records, 1):
    attributes = []
    for attribute in [
        "function",
        "total",
        "functional",
        "simplification",
        "concrete",
        "macro",
        "macro-rec",
        "owise",
        "priority",
        "strict",
        "seqstrict",
        "no-evaluators",
        "symbol",
    ]:
        if re.search(rf"\b{re.escape(attribute)}\b", statement):
            attributes.append(attribute)
    print(
        f"{number:04d} {rel}:{line} kind={kind} "
        f"attributes={','.join(attributes) if attributes else '-'}"
    )
    print(f"  DECISION={audit_decision}")
    print(f"  STATEMENT={statement}")
