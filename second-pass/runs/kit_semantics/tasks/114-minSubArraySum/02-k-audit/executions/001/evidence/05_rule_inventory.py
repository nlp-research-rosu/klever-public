#!/usr/bin/env python3
"""Enumerate every declaration/rule in supplied and proof-local K sources."""

from __future__ import annotations

import collections
import re
from pathlib import Path


WORK = Path("/tmp/audit-work/114-minSubArraySum")
FILES = [
    WORK / "reference-semantics" / "semantics.k",
    *sorted((WORK / "reference-semantics" / "semantics").glob("*.k")),
    WORK / "verification.k",
    WORK / "spec.k",
]

start_pattern = re.compile(
    r'^\s*(?P<kind>module|imports|configuration|syntax|rule|context|claim)\b'
    r'|^(?P<file_requires>requires)\s+"'
)
attribute_pattern = re.compile(
    r"\b(function|total|functional|simplification|owise|concrete|macro-rec|macro|"
    r"no-evaluators|symbol|strict|seqstrict)\b|priority\([^)]*\)"
)

kind_counts: collections.Counter[str] = collections.Counter()
attribute_counts: collections.Counter[str] = collections.Counter()
file_counts: collections.Counter[str] = collections.Counter()
records: list[tuple[str, int, str, list[str], str]] = []

for path in FILES:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_pattern.match(line)
    ]
    for position, start in enumerate(starts):
        next_start = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block_lines = lines[start:next_start]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
            or block_lines[-1].strip() == "endmodule"
        ):
            block_lines.pop()
        first = block_lines[0]
        match = start_pattern.match(first)
        assert match is not None
        kind = match.group("kind") or match.group("file_requires")
        normalized = " ".join(
            part.strip()
            for part in block_lines
            if part.strip() and not part.lstrip().startswith("//")
        )
        attributes = sorted(set(attribute_pattern.findall(normalized)))
        # findall has an alternative; normalize priority separately.
        attributes = [item for item in attributes if item]
        attributes.extend(sorted(set(re.findall(r"priority\([^)]*\)", normalized))))
        if kind == "rule":
            attributes.append("operational" if "<k>" in normalized else "equational")
            if "[simplification]" not in normalized:
                attributes.append("ordinary-rule")
        if kind == "syntax" and (
            "symbol" in normalized or "no-evaluators" in normalized
        ):
            attributes.append("opaque-or-backend-symbol")
        attributes = sorted(set(attributes))
        relative = path.relative_to(WORK).as_posix()
        kind_counts[kind] += 1
        file_counts[relative] += 1
        attribute_counts.update(attributes)
        records.append((relative, start + 1, kind, attributes, normalized))

print("INVENTORY_FILES:", len(FILES))
print("INVENTORY_RECORDS:", len(records))
print("KIND_COUNTS:", dict(sorted(kind_counts.items())))
print("ATTRIBUTE_COUNTS:", dict(sorted(attribute_counts.items())))
print("FILE_COUNTS:")
for path, count in sorted(file_counts.items()):
    print(f"  {count:4d} {path}")
print("RECORDS:")
for path, line, kind, attributes, normalized in records:
    print(
        f"{path}:{line}\t{kind}\t"
        f"attrs={','.join(attributes) if attributes else '-'}\t{normalized}"
    )
