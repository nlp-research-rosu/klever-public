#!/usr/bin/env python3
"""Lexical, exhaustive declaration/rule inventory for all audited K sources."""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path


SOURCES = [
    Path("/tmp/audit-work/119-match-parens/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/119-match-parens/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/119-match-parens/verification.k"),
    Path("/tmp/audit-work/119-match-parens/spec.k"),
]
START = re.compile(r"^  (syntax|rule|claim|context|configuration)\b")
BOUNDARY = re.compile(r"^\s*(module|endmodule|imports)\b")


def squash(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines if line.strip())
    return re.sub(r"\s+", " ", text)


records: list[dict[str, object]] = []
for path in SOURCES:
    lines = path.read_text().splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    for position, index in enumerate(starts):
        next_index = starts[position + 1] if position + 1 < len(starts) else len(lines)
        for candidate in range(index + 1, next_index):
            if BOUNDARY.match(lines[candidate]):
                next_index = candidate
                break
        block = lines[index:next_index]
        kind = START.match(lines[index]).group(1)
        text = squash(block)
        code_only = " ".join(line.split("//", 1)[0] for line in block)
        attribute_text = " ".join(re.findall(r"\[([^\]]*)\]", code_only))
        attrs = []
        for attr in (
            "function",
            "total",
            "functional",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "symbol",
            "no-evaluators",
            "macro",
            "strict",
            "seqstrict",
            "hook",
            "circularity",
        ):
            if re.search(rf"\b{re.escape(attr)}\b", attribute_text):
                attrs.append(attr)
        category = kind
        if kind == "rule" and "simplification" in attrs:
            category = "simplification-rule"
        elif kind == "rule":
            category = "ordinary-rule"
        elif kind == "syntax" and "function" in attrs:
            category = "function-declaration"
        elif kind == "syntax":
            category = "syntax-declaration"
        elif kind == "claim":
            category = "reachability-claim"
        records.append(
            {
                "file": str(path.relative_to("/tmp/audit-work/119-match-parens")),
                "line": index + 1,
                "category": category,
                "attrs": ",".join(attrs) if attrs else "-",
                "text": text,
            }
        )

counts = Counter(str(record["category"]) for record in records)
file_counts: dict[str, Counter[str]] = defaultdict(Counter)
for record in records:
    file_counts[str(record["file"])][str(record["category"])] += 1

print(f"SOURCES={len(SOURCES)}")
print(f"RECORDS={len(records)}")
print(f"CATEGORY_COUNTS={dict(sorted(counts.items()))}")
print("FILE_COUNTS")
for name in sorted(file_counts):
    print(f"  {name}: {dict(sorted(file_counts[name].items()))}")
print("FULL_INVENTORY")
print("file:line | category | attributes | declaration/rule")
for record in records:
    print(
        f"{record['file']}:{record['line']} | {record['category']} | "
        f"{record['attrs']} | {record['text']}"
    )
