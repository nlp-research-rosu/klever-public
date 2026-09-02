#!/usr/bin/env python3
"""Enumerate every local K declaration, rule, context, and claim under audit."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
paths = [
    ROOT / "reference-semantics" / "semantics.k",
    *sorted((ROOT / "reference-semantics" / "semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_re = re.compile(
    r"^\s*(module|endmodule|imports|requires|configuration|syntax|context|rule|claim|alias)\b"
)
entry_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim|alias)\b")

counts: dict[str, int] = {}
attribute_counts = {
    "function": 0,
    "functional": 0,
    "total": 0,
    "symbol": 0,
    "no-evaluators": 0,
    "priority": 0,
    "simplification": 0,
    "concrete": 0,
    "owise": 0,
    "macro": 0,
    "macro-rec": 0,
}
entries: list[tuple[str, int, str, str]] = []

for path in paths:
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        match = entry_re.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines) and not start_re.match(lines[index]):
            index += 1
        text = " ".join(
            line.strip()
            for line in lines[start:index]
            if line.strip() and not line.lstrip().startswith("//")
        )
        rel = path.relative_to(ROOT).as_posix()
        entries.append((rel, start + 1, kind, text))
        counts[kind] = counts.get(kind, 0) + 1
        for attr in attribute_counts:
            if re.search(rf"\b{re.escape(attr)}\b", text):
                attribute_counts[attr] += 1

print(f"source_file_count={len(paths)}")
print(f"entry_count={len(entries)}")
print(f"kind_counts={counts}")
print(f"attribute_entry_counts={attribute_counts}")
print()
print("ID\tLOCATION\tKIND\tATTRIBUTES\tDECLARATION_OR_RULE")
for number, (rel, line, kind, text) in enumerate(entries, 1):
    attrs = [
        name
        for name in attribute_counts
        if re.search(rf"\b{re.escape(name)}\b", text)
    ]
    print(
        f"K{number:04d}\t{rel}:{line}\t{kind}\t"
        f"{','.join(attrs) if attrs else '-'}\t{text}"
    )
