#!/usr/bin/env python3
"""Enumerate every local K declaration/rule/context in the audited sources."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path


START = re.compile(r"^  (configuration|syntax|context|rule|claim)\b")
END = re.compile(r"^(?:module\b|endmodule\b)")
ATTRIBUTE_PATTERNS = {
    "function": re.compile(r"\bfunction\b"),
    "total": re.compile(r"\btotal\b"),
    "functional": re.compile(r"\bfunctional\b"),
    "opaque/no-evaluators": re.compile(r"\bno-evaluators\b"),
    "symbol": re.compile(r"\bsymbol(?:\(|\b)"),
    "priority": re.compile(r"\bpriority\s*\("),
    "simplification": re.compile(r"\bsimplification\b"),
    "concrete": re.compile(r"\bconcrete\b"),
    "owise": re.compile(r"\bowise\b"),
    "macro": re.compile(r"\bmacro\b"),
    "strict/context": re.compile(r"\b(?:seqstrict|strict|context)\b"),
}


def records(path: Path):
    lines = path.read_text().splitlines()
    starts = []
    for index, line in enumerate(lines):
        if START.match(line):
            starts.append(index)
    for ordinal, start in enumerate(starts):
        stop = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(lines)
        for index in range(start + 1, stop):
            if END.match(lines[index]):
                stop = index
                break
        block = "\n".join(lines[start:stop]).rstrip()
        kind = START.match(lines[start]).group(1)
        yield start + 1, kind, block


paths = [Path(argument) for argument in sys.argv[1:]]
kind_counts = collections.Counter()
attribute_counts = collections.Counter()
file_counts = collections.Counter()
record_number = 0

all_records = []
for path in paths:
    for line, kind, block in records(path):
        record_number += 1
        kind_counts[kind] += 1
        file_counts[str(path)] += 1
        semantic_text = "\n".join(
            source_line
            for source_line in block.splitlines()
            if not source_line.lstrip().startswith("//")
        )
        attributes = [
            name for name, pattern in ATTRIBUTE_PATTERNS.items()
            if pattern.search(semantic_text)
        ]
        for attribute in attributes:
            attribute_counts[attribute] += 1
        if kind == "rule" and not any(
            attribute in attributes
            for attribute in ("priority", "simplification", "concrete", "owise")
        ):
            attributes.append("ordinary-rule")
            attribute_counts["ordinary-rule"] += 1
        all_records.append(
            (record_number, path, line, kind, attributes, block)
        )

print(f"TOTAL_RECORDS: {record_number}")
print("KIND_COUNTS:")
for key, value in sorted(kind_counts.items()):
    print(f"  {key}: {value}")
print("ATTRIBUTE_COUNTS (records may have multiple attributes):")
for key, value in sorted(attribute_counts.items()):
    print(f"  {key}: {value}")
print("FILE_COUNTS:")
for key, value in sorted(file_counts.items()):
    print(f"  {key}: {value}")
print("FULL_INVENTORY:")
for number, path, line, kind, attributes, block in all_records:
    label = ",".join(attributes) if attributes else "none"
    print(f"\nITEM {number:04d} {path}:{line} KIND={kind} CLASS={label}")
    print(block)
