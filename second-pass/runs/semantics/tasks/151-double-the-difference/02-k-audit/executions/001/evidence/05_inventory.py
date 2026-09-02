#!/usr/bin/env python3
"""Produce a complete, source-indexed K declaration/rule inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
FILES = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r"^(requires|module|endmodule)\b"
    r"|^ {2}(imports|configuration|context|syntax|rule|claim|macro|alias)\b"
)
ATTRIBUTE = re.compile(r"\[([^\]]+)\]")


def classify(kind: str, block: str) -> tuple[str, str]:
    attrs = ",".join(ATTRIBUTE.findall(block)).replace("\n", " ")
    if kind == "rule":
        if "simplification" in attrs:
            category = "simplification-rule"
        elif "priority" in attrs:
            category = "priority-rule"
        elif "<" in block and ">" in block:
            category = "operational-rule"
        else:
            category = "equational-rule"
    elif kind == "syntax":
        if "function" in attrs or "functional" in attrs:
            category = "function-syntax"
        else:
            category = "syntax"
    else:
        category = kind
    return category, attrs


entries = []
for path in FILES:
    lines = path.read_text().splitlines()
    starts = [(index, START.match(line)) for index, line in enumerate(lines)]
    starts = [(index, match) for index, match in starts if match]
    for pos, (index, match) in enumerate(starts):
        next_index = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        block = "\n".join(lines[index:next_index]).rstrip()
        kind = match.group(1) or match.group(2)
        category, attrs = classify(kind, block)
        rel = str(path.relative_to(ROOT))
        entries.append(
            {
                "file": rel,
                "line": index + 1,
                "kind": kind,
                "category": category,
                "attributes": attrs,
                "block": block,
            }
        )

counts = collections.Counter(entry["category"] for entry in entries)
file_counts = collections.Counter(entry["file"] for entry in entries)
rule_counts = collections.Counter(
    entry["file"] for entry in entries if entry["kind"] in {"rule", "claim"}
)

print("# Exhaustive K source inventory")
print()
print("Generated from every mounted supplied-semantics K source plus candidate")
print("`verification.k` and `spec.k`. Each item preserves its complete source")
print("block through the next top-level K declaration.")
print()
print("## Summary")
print()
print(f"- Files: {len(FILES)}")
print(f"- Top-level inventory entries: {len(entries)}")
for category, count in sorted(counts.items()):
    print(f"- `{category}`: {count}")
print()
print("| File | Entries | Rules/claims |")
print("|---|---:|---:|")
for file in sorted(file_counts):
    print(f"| `{file}` | {file_counts[file]} | {rule_counts[file]} |")
print()
print("## Entries")
print()
for number, entry in enumerate(entries, 1):
    attrs = entry["attributes"] or "none"
    print(
        f"### I{number:04d} — `{entry['file']}:{entry['line']}` "
        f"({entry['category']}; attributes: `{attrs}`)"
    )
    print()
    print("```k")
    print(entry["block"])
    print("```")
    print()
