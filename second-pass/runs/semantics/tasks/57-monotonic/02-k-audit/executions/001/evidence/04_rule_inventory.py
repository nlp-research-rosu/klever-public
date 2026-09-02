#!/usr/bin/env python3
"""Enumerate every local K declaration/rule in the audited source tree."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

WORK = Path("/tmp/audit-work/57-monotonic")
OUT = Path("/audit-output/evidence/04_rule_inventory.tsv")
source_paths = [
    WORK / "reference-semantics" / "semantics.k",
    *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]

start_re = re.compile(r"^\s*(configuration|syntax|rule|context|claim)\b")
attribute_re = re.compile(r"\[([^\]]+)\]")


def disposition(relative: str, line: int, kind: str, text: str) -> tuple[str, str]:
    if relative == "verification.k":
        if line == 55:
            return (
                "proof-local result abstraction",
                "REJECT: [total] has uncovered ground list-pair cases",
            )
        if line == 57:
            return (
                "proof-local operational bridge",
                "REJECT: replaces fixed list equality on a broader domain",
            )
        if line in (62, 66):
            return (
                "proof-local simplification axiom",
                "REJECT-AS-CONNECTION: no bridge-free theorem; ground specialization fails",
            )
        if 8 <= line <= 36:
            return (
                "proof-local definitional program constant",
                "ACCEPT: byte/AST identity checked independently",
            )
        if 40 <= line <= 50 or 74 <= line <= 76:
            return (
                "proof-local mathematical definition",
                "ACCEPT on values with modeled <=/>= comparisons",
            )
        return ("proof-local declaration", "REVIEWED")
    if relative == "spec.k":
        return ("target reachability claim", "TARGET: dynamic closure is not soundness")
    if relative.endswith("semantics/sort.k") and (
        "sortVS" in text or "sortKeyVS" in text
    ):
        return (
            "fixed supplied trusted sort boundary",
            "CONDITIONAL TRUST: opaque symbolic value with concrete ground rules",
        )
    if relative.endswith("semantics/concrete.k"):
        return (
            "fixed supplied concrete-only rule",
            "ACCEPTED BASELINE; excluded from Haskell proof import",
        )
    if relative.startswith("reference-semantics/"):
        return (
            "fixed supplied semantics",
            "ACCEPTED BASELINE; integrity exact, no intended-path false witness found",
        )
    return ("unclassified", "REVIEWED")


rows: list[dict[str, str | int]] = []
for path in source_paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [
        (index, match.group(1))
        for index, line in enumerate(lines)
        if (match := start_re.match(line))
    ]
    for position, (index, kind) in enumerate(starts):
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = lines[index:next_index]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        text = " ".join(line.strip() for line in block_lines)
        text = re.sub(r"\s+", " ", text)
        attributes = ";".join(attribute_re.findall(text))
        relative = str(path.relative_to(WORK))
        category, decision = disposition(relative, index + 1, kind, text)
        rows.append(
            {
                "id": len(rows) + 1,
                "path": relative,
                "line": index + 1,
                "kind": kind,
                "attributes": attributes,
                "category": category,
                "decision": decision,
                "declaration_or_rule": text,
            }
        )

with OUT.open("w", encoding="utf-8", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "id",
            "path",
            "line",
            "kind",
            "attributes",
            "category",
            "decision",
            "declaration_or_rule",
        ],
        dialect="excel-tab",
    )
    writer.writeheader()
    writer.writerows(rows)

counts = Counter(str(row["kind"]) for row in rows)
categories = Counter(str(row["category"]) for row in rows)
print(f"sources={len(source_paths)}")
print(f"inventory_rows={len(rows)}")
for key in sorted(counts):
    print(f"kind_{key}={counts[key]}")
for key in sorted(categories):
    print(f"category_{key}={categories[key]}")
print(f"output={OUT}")
