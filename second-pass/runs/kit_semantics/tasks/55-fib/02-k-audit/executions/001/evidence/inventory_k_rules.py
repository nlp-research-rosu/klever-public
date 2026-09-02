#!/usr/bin/env python3
"""Produce an exhaustive, line-addressed inventory of all local K declarations."""

from __future__ import annotations

import collections
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path("/tmp/audit-work/fib-audit")
SOURCES = sorted((ROOT / "reference-semantics").rglob("*.k")) + [
    ROOT / "verification.k",
    ROOT / "spec.k",
]
START = re.compile(
    r'^\s*(context\s+alias|configuration|endmodule|requires(?=\s+")|imports|'
    r"module|syntax|context|rule|claim)\b"
)


@dataclass
class Entry:
    path: Path
    line: int
    kind: str
    text: str
    categories: tuple[str, ...]


def categories(kind: str, text: str) -> tuple[str, ...]:
    found = []
    code = "\n".join(line.split("//", 1)[0] for line in text.splitlines())
    lowered = code.lower()
    attributes = " ".join(re.findall(r"\[([^\]]*)\]", lowered))
    for name in (
        "function",
        "functional",
        "total",
        "macro",
        "simplification",
        "priority",
        "owise",
        "concrete",
        "symbol",
        "hook",
        "strict",
        "seqstrict",
        "assoc",
        "comm",
        "unit",
    ):
        if re.search(rf"\b{re.escape(name)}\b", attributes):
            found.append(name)
    if "no-evaluators" in attributes or re.search(r"\bopaque\b", attributes):
        found.append("opaque")
    if kind == "rule":
        if "simplification" in found:
            found.append("simplification-rule")
        elif "macro" in found:
            found.append("macro-rule")
        else:
            found.append("ordinary-semantic-rule")
    return tuple(found)


entries = []
for source in SOURCES:
    lines = source.read_text(encoding="utf-8").splitlines()
    starts = []
    for index, line in enumerate(lines):
        match = START.match(line)
        if match:
            starts.append((index, match.group(1).replace(" ", "-")))
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        text = "\n".join(lines[index:end]).rstrip()
        entries.append(
            Entry(
                path=source,
                line=index + 1,
                kind=kind,
                text=text,
                categories=categories(kind, text),
            )
        )

kind_counts = collections.Counter(entry.kind for entry in entries)
category_counts = collections.Counter(
    category for entry in entries for category in entry.categories
)

print("# Exhaustive K declaration and rule inventory")
print()
print("Generated from the clean scratch source copies. Each listed block is")
print("addressed by source file and starting line; no compiled rules are used.")
print()
print("## Summary")
print()
print(f"- Source files: {len(SOURCES)}")
print(f"- Inventoried declaration blocks: {len(entries)}")
for kind, count in sorted(kind_counts.items()):
    print(f"- `{kind}`: {count}")
for category, count in sorted(category_counts.items()):
    print(f"- category `{category}`: {count}")

for source in SOURCES:
    relative = source.relative_to(ROOT)
    print()
    print(f"## `{relative}`")
    for entry in entries:
        if entry.path != source:
            continue
        category_text = ", ".join(entry.categories) if entry.categories else "-"
        print()
        print(
            f"### `{relative}:{entry.line}` — {entry.kind}; "
            f"categories: {category_text}"
        )
        print()
        print("```k")
        print(entry.text)
        print("```")
