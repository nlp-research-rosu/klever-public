#!/usr/bin/env python3
"""Inventory every top-level K declaration/rule in supplied and proof-local sources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/reconstruction/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/reconstruction/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/reconstruction/verification.k"),
    Path("/tmp/audit-work/reconstruction/spec.k"),
]
OUT = Path("/audit-output/evidence/rule-inventory.tsv")
SUMMARY = Path("/audit-output/evidence/rule-inventory-summary.txt")

START = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|syntax|rule|claim|"
    r"context|context alias|priority|endmodule)\b"
)
ITEM = re.compile(
    r"^\s*(requires|module|imports|configuration|syntax|rule|claim|"
    r"context alias|context|priority|endmodule)\b"
)

USED_TERMS = {
    "Module",
    "FuncDef",
    "Params",
    "Assign",
    "Name",
    "Str",
    "Int",
    "For",
    "If",
    "Call",
    "Attribute",
    "AugAssign",
    "Return",
    "str(",
    "IntSeq",
    "isupper",
    "isUpperC",
    "isLowerC",
    "ord",
    "applyBin",
    "closureVal",
    "builtinsScope",
    "#loop",
    "#for",
    "#endcall",
    "frame(",
    "<k>",
    "<env>",
    "<scopes>",
    "<scopeLoc>",
    "<stack>",
    "<ret>",
    "<exc>",
}


def source_items(path: Path):
    lines = path.read_text().splitlines()
    starts: list[int] = []
    for index, line in enumerate(lines):
        if ITEM.match(line):
            starts.append(index)
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        first = lines[start]
        match = ITEM.match(first)
        assert match
        kind = match.group(1)
        # Comments immediately before an item are useful context but are not an item.
        body = "\n".join(lines[start:end]).rstrip()
        yield start + 1, kind, body


rows: list[dict[str, str]] = []
module = ""
for path in ROOTS:
    for line, kind, text in source_items(path):
        flat = re.sub(r"\s+", " ", text).strip()
        code = "\n".join(re.sub(r"//.*$", "", part) for part in text.splitlines())
        code_flat = re.sub(r"\s+", " ", code).strip()
        if kind == "module":
            parts = code_flat.split()
            module = parts[1] if len(parts) > 1 else ""
        flags: list[str] = []
        for flag in [
            "function",
            "total",
            "functional",
            "simplification",
            "symbol",
            "macro",
            "macro-rec",
            "anywhere",
            "owise",
            "priority",
            "concrete",
            "trusted",
        ]:
            if re.search(rf"\b{re.escape(flag)}\b", code_flat):
                flags.append(flag)
        if kind == "rule":
            category = "ordinary-rule"
            if "simplification" in flags:
                category = "simplification-rule"
            elif "macro" in flags or "macro-rec" in flags:
                category = "macro-rule"
            elif "anywhere" in flags:
                category = "anywhere-rule"
        elif kind == "syntax":
            category = "syntax-declaration"
        else:
            category = kind
        relevant_terms = sorted(term for term in USED_TERMS if term in code)
        rows.append(
            {
                "source": str(path),
                "line": str(line),
                "module": module,
                "category": category,
                "flags": ",".join(flags),
                "used_term_hits": ",".join(relevant_terms),
                "code": code_flat,
                "text": flat,
            }
        )

with OUT.open("w", newline="") as stream:
    writer = csv.DictWriter(
        stream,
        fieldnames=[
            "source",
            "line",
            "module",
            "category",
            "flags",
            "used_term_hits",
            "code",
            "text",
        ],
        delimiter="\t",
    )
    writer.writeheader()
    writer.writerows(rows)

category_counts = Counter(row["category"] for row in rows)
flag_counts = Counter(
    flag for row in rows for flag in row["flags"].split(",") if flag
)
file_counts = Counter(row["source"] for row in rows)
with SUMMARY.open("w") as stream:
    stream.write(f"FILES: {len(ROOTS)}\n")
    stream.write(f"ITEMS: {len(rows)}\n")
    stream.write("CATEGORY_COUNTS:\n")
    for key, value in sorted(category_counts.items()):
        stream.write(f"  {key}: {value}\n")
    stream.write("FLAG_COUNTS:\n")
    for key, value in sorted(flag_counts.items()):
        stream.write(f"  {key}: {value}\n")
    stream.write("FILE_COUNTS:\n")
    for key, value in sorted(file_counts.items()):
        stream.write(f"  {key}: {value}\n")
    stream.write("PROGRAM-TERM-HIT ITEMS:\n")
    for row in rows:
        if row["used_term_hits"]:
            stream.write(
                f"  {row['source']}:{row['line']} [{row['category']}] "
                f"hits={row['used_term_hits']} :: {row['text']}\n"
            )

print(f"files={len(ROOTS)}")
print(f"items={len(rows)}")
print(f"inventory={OUT}")
print(f"summary={SUMMARY}")
