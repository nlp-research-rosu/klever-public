#!/usr/bin/env python3
"""Mechanically enumerate all K declarations and rules in the audit scope."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path("/candidate/reference-semantics")
FILES = sorted(ROOT.rglob("*.k")) + [Path("/candidate/verification.k")]
START = re.compile(r"^\s*(configuration|syntax|context|claim|rule)\b")
BOUNDARY = re.compile(r"^\s*(?:configuration|syntax|context|claim|rule|module|endmodule)\b")
ATTRIBUTES = (
    "function",
    "functional",
    "total",
    "simplification",
    "priority",
    "macro",
    "macro-rec",
    "owise",
    "concrete",
    "symbol",
    "no-evaluators",
)


def normalized(block: list[str]) -> str:
    return " ".join(" ".join(block).split())


all_entries: list[tuple[Path, int, str, str, tuple[str, ...]]] = []
per_file: dict[Path, Counter[str]] = {}

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[tuple[int, str, str, tuple[str, ...]]] = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        end = index + 1
        while end < len(lines) and not BOUNDARY.match(lines[end]):
            end += 1
        source_block = lines[index:end]
        block = normalized(source_block)
        uncommented = normalized([line.split("//", 1)[0] for line in source_block])
        tags = tuple(attribute for attribute in ATTRIBUTES if attribute in uncommented)
        entries.append((index + 1, kind, block, tags))
        all_entries.append((path, index + 1, kind, block, tags))
        index = end

    counts = Counter(kind for _, kind, _, _ in entries)
    for _, _, _, tags in entries:
        counts.update(f"attr:{tag}" for tag in tags)
    per_file[path] = counts

print("# Exhaustive K declaration and rule inventory")
print()
print("Scope: exact candidate supplied-semantics tree plus candidate verification.k.")
print(f"Files: {len(FILES)}")
print(f"Inventory entries: {len(all_entries)}")
print()
print("## Per-file counts")
print()
print("| File | Configuration | Syntax | Context | Claim | Rule | Function | Total | "
      "Functional | Opaque/no-evaluators | Priority | Simplification | Macro | Owise | Concrete |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for path in FILES:
    counts = per_file[path]
    display = path.as_posix().replace("/candidate/", "")
    print(
        f"| `{display}` | {counts['configuration']} | {counts['syntax']} | "
        f"{counts['context']} | {counts['claim']} | {counts['rule']} | "
        f"{counts['attr:function']} | {counts['attr:total']} | "
        f"{counts['attr:functional']} | {counts['attr:no-evaluators']} | "
        f"{counts['attr:priority']} | {counts['attr:simplification']} | "
        f"{counts['attr:macro'] + counts['attr:macro-rec']} | "
        f"{counts['attr:owise']} | {counts['attr:concrete']} |"
    )

totals = Counter()
for counts in per_file.values():
    totals.update(counts)
print()
print("TOTALS " + " ".join(f"{key}={totals[key]}" for key in sorted(totals)))

print()
print("## Full entries")
for ordinal, (path, line, kind, block, tags) in enumerate(all_entries, 1):
    display = path.as_posix().replace("/candidate/", "")
    tag_text = ",".join(tags) if tags else "-"
    print(f"{ordinal:04d} {display}:{line} kind={kind} tags={tag_text}")
    print(f"    {block}")
