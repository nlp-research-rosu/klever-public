#!/usr/bin/env python3
"""Lexical inventory of every local K declaration in the audited sources."""

from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
OUT = Path("/audit-output/evidence/05-rule-inventory.tsv")

START = re.compile(
    r"^(requires(?=\s+\")|\s*(?:module|endmodule|imports|configuration|context|"
    r"syntax(?:\s+priority|\s+associativity)?|rule|claim))\b"
)
ATTRIBUTES = [
    "function",
    "total",
    "functional",
    "macro",
    "simplification",
    "concrete",
    "symbolic",
    "priority",
    "owise",
    "strict",
    "seqstrict",
    "heat",
    "cool",
]


def normalized(lines: list[str]) -> str:
    pieces: list[str] = []
    for line in lines:
        code = line.split("//", 1)[0].strip()
        if code:
            pieces.append(code)
    return " ".join(pieces)


records: list[dict[str, str | int]] = []
for path in SOURCES:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    module = ""
    for pos, start in enumerate(starts):
        end = starts[pos + 1] if pos + 1 < len(starts) else len(lines)
        first = lines[start].strip()
        kind_match = START.match(lines[start])
        assert kind_match
        kind = kind_match.group(1).strip().split()[0]
        statement = normalized(lines[start:end])
        if kind == "module":
            parts = first.split()
            module = parts[1] if len(parts) > 1 else ""
        current_module = module
        if kind == "endmodule":
            current_module = module
        attrs = ",".join(attr for attr in ATTRIBUTES if re.search(rf"\b{attr}\b", statement))
        records.append(
            {
                "file": path.relative_to(ROOT).as_posix(),
                "line": start + 1,
                "module": current_module,
                "kind": kind,
                "attributes": attrs,
                "statement": statement,
            }
        )
        if kind == "endmodule":
            module = ""

with OUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=["file", "line", "module", "kind", "attributes", "statement"],
        delimiter="\t",
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(records)

kind_counts = Counter(str(record["kind"]) for record in records)
file_counts: dict[str, Counter[str]] = defaultdict(Counter)
attribute_counts = Counter()
for record in records:
    file_counts[str(record["file"])][str(record["kind"])] += 1
    for attribute in str(record["attributes"]).split(","):
        if attribute:
            attribute_counts[attribute] += 1

print(f"source_file_count={len(SOURCES)}")
print(f"inventory_record_count={len(records)}")
print(f"kind_counts={dict(sorted(kind_counts.items()))}")
print(f"attribute_counts={dict(sorted(attribute_counts.items()))}")
for file, counts in sorted(file_counts.items()):
    print(f"file={file} counts={dict(sorted(counts.items()))}")
print(f"inventory_path={OUT}")
