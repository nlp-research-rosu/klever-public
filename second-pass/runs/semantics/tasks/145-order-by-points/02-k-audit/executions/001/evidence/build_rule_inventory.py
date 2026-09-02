#!/usr/bin/env python3
"""Emit a source-linked inventory of every K declaration and rule."""

from __future__ import annotations

import re
from pathlib import Path


SOURCES = [
    Path("/reference/reference-semantics/semantics.k"),
    *sorted(Path("/reference/reference-semantics/semantics").glob("*.k")),
    Path("/candidate/verification.k"),
    Path("/candidate/spec.k"),
]

START = re.compile(
    r"^\s*(configuration|syntax|context(?:\s+alias)?|rule|claim)\b"
)
BOUNDARY = re.compile(
    r"^\s*(configuration|syntax|context(?:\s+alias)?|rule|claim|module|endmodule)\b"
)


def classify(block: str) -> str:
    head = START.match(block)
    kind = head.group(1) if head else "unknown"
    tags = [kind]
    for tag in (
        "function",
        "functional",
        "total",
        "macro",
        "macro-rec",
        "simplification",
        "concrete",
        "owise",
        "priority",
        "symbol",
        "no-evaluators",
        "strict",
        "seqstrict",
    ):
        if re.search(rf"\b{re.escape(tag)}\b", block):
            tags.append(tag)
    if kind == "syntax" and "symbol" in tags and "no-evaluators" in tags:
        tags.append("opaque")
    return ", ".join(tags)


total_entries = 0
kind_counts: dict[str, int] = {}

print("# Exhaustive K declaration and rule inventory")
print()
print("Sources are the trusted supplied semantics plus candidate proof sources.")
print()

for source in SOURCES:
    lines = source.read_text(encoding="utf-8").splitlines()
    entries: list[tuple[int, int, str]] = []
    index = 0
    while index < len(lines):
        if not START.match(lines[index]):
            index += 1
            continue
        start = index
        index += 1
        while index < len(lines) and not BOUNDARY.match(lines[index]):
            index += 1
        block = "\n".join(lines[start:index]).rstrip()
        entries.append((start + 1, index, block))

    print(f"## {source}")
    print()
    print(f"Entries: {len(entries)}")
    print()
    for ordinal, (first, last, block) in enumerate(entries, 1):
        category = classify(block)
        first_kind = category.split(",", 1)[0]
        kind_counts[first_kind] = kind_counts.get(first_kind, 0) + 1
        total_entries += 1
        print(f"### {ordinal}. lines {first}-{last}: {category}")
        print()
        print("```k")
        print(block)
        print("```")
        print()

print("# Totals")
print()
print(f"All entries: {total_entries}")
for kind in sorted(kind_counts):
    print(f"- {kind}: {kind_counts[kind]}")
