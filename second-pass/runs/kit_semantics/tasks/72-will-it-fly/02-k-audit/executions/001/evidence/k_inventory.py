#!/usr/bin/env python3
"""Emit a source-location inventory of every candidate and supplied K declaration."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOTS = [
    Path("/candidate/reference-semantics"),
    Path("/candidate"),
]
TOP_LEVEL_K = set(Path("/candidate").glob("*.k"))
FILES = sorted(Path("/candidate/reference-semantics").rglob("*.k")) + sorted(TOP_LEVEL_K)
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.md")

START = re.compile(r"^\s*(module|endmodule|configuration|syntax|context|rule|claim)\b")
ATTRIBUTES = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "strict",
    "seqstrict",
    "symbol",
    "no-evaluators",
    "preserves-definedness",
)


def without_line_comment(line: str) -> str:
    return line.split("//", 1)[0]


records: list[dict[str, str | int]] = []
for path in FILES:
    assert not path.is_symlink()
    lines = path.read_text().splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = START.match(without_line_comment(line))
        if match:
            starts.append((index, match.group(1)))

    for position, (index, kind) in enumerate(starts):
        if kind == "endmodule":
            continue
        next_index = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[index:next_index]:
            uncommented = without_line_comment(line).strip()
            if uncommented:
                block_lines.append(uncommented)
        text = " ".join(block_lines)
        flags = [attribute for attribute in ATTRIBUTES if re.search(rf"\b{re.escape(attribute)}\b", text)]
        if kind == "rule":
            if "simplification" in flags:
                classification = "simplification-rule"
            elif "<k>" in text or any(f"<{cell}>" in text for cell in (
                "env", "scopes", "heap", "heapLoc", "stack", "ret", "exc", "exit-code"
            )):
                classification = "operational-rule"
            else:
                classification = "function-or-equational-rule"
        elif kind == "syntax":
            classification = "syntax-declaration"
            if "no-evaluators" in flags:
                classification += "+opaque-symbol"
        elif kind == "claim":
            classification = "reachability-claim"
        else:
            classification = kind
        records.append(
            {
                "file": str(path),
                "line": index + 1,
                "kind": kind,
                "classification": classification,
                "attributes": ",".join(flags),
                "declaration": text,
            }
        )

with OUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=("file", "line", "kind", "classification", "attributes", "declaration"),
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(records)

by_file: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    by_file[str(record["file"])][str(record["classification"])] += 1

lines = [
    "# Exhaustive K declaration inventory summary",
    "",
    f"Inventoried files: {len(FILES)}",
    f"Inventoried declarations: {len(records)}",
    "",
    "| File | Syntax | Opaque syntax | Operational rules | Equational rules | Simplifications | Contexts | Claims |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]
for file_name in sorted(by_file):
    counts = by_file[file_name]
    lines.append(
        "| "
        + " | ".join(
            [
                file_name,
                str(counts["syntax-declaration"] + counts["syntax-declaration+opaque-symbol"]),
                str(counts["syntax-declaration+opaque-symbol"]),
                str(counts["operational-rule"]),
                str(counts["function-or-equational-rule"]),
                str(counts["simplification-rule"]),
                str(counts["context"]),
                str(counts["reachability-claim"]),
            ]
        )
        + " |"
    )

lines.extend(["", "## Global classification totals", ""])
totals = Counter(str(record["classification"]) for record in records)
for key, value in sorted(totals.items()):
    lines.append(f"- {key}: {value}")
SUMMARY.write_text("\n".join(lines) + "\n")

print(f"files={len(FILES)}")
print(f"declarations={len(records)}")
for key, value in sorted(totals.items()):
    print(f"{key}={value}")
print(f"inventory={OUT}")
print(f"summary={SUMMARY}")
