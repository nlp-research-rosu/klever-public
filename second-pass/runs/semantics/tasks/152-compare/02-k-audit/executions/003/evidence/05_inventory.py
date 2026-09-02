#!/usr/bin/env python3
"""Line-addressed inventory of K declarations, rules, claims, and attributes."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/152-compare/candidate")
files = sorted((ROOT / "reference-semantics").rglob("*.k"))
files.extend(
    [
        ROOT / "verification.k",
        ROOT / "spec.k",
        ROOT / "operational-spec.k",
        ROOT / "mutation-spec.k",
    ]
)

directive = re.compile(
    r"^\s*(requires|module|imports|configuration|syntax|context|rule|claim)\b"
)
attribute_words = (
    "function",
    "functional",
    "total",
    "macro",
    "macro-rec",
    "no-evaluators",
    "concrete",
    "priority",
    "owise",
    "strict",
    "seqstrict",
)

grand_counts: collections.Counter[str] = collections.Counter()
print("K_RULE_INVENTORY")
for path in files:
    relative = path.relative_to(ROOT).as_posix()
    counts: collections.Counter[str] = collections.Counter()
    entries: list[tuple[int, str, str]] = []
    with path.open("r", encoding="utf-8") as stream:
        for line_number, raw_line in enumerate(stream, 1):
            line = raw_line.rstrip()
            match = directive.match(line)
            if match:
                kind = match.group(1)
                counts[kind] += 1
                grand_counts[kind] += 1
                entries.append((line_number, kind, line.strip()))
            if any(f"[{word}" in line or f", {word}" in line for word in attribute_words):
                for word in attribute_words:
                    if re.search(rf"\b{re.escape(word)}\b", line):
                        counts[f"attr:{word}"] += 1
                        grand_counts[f"attr:{word}"] += 1
    print(f"FILE {relative}")
    print(f"COUNTS {dict(sorted(counts.items()))}")
    for line_number, kind, text in entries:
        print(f"  {line_number:04d} {kind:13s} {text}")

print(f"GRAND_COUNTS {dict(sorted(grand_counts.items()))}")
