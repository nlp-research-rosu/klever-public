#!/usr/bin/env python3
"""Enumerate every K declaration and rule in the supplied audit sources."""

from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from pathlib import Path


WORK = Path("/tmp/audit-work")
FILES = sorted((WORK / "reference-semantics").rglob("*.k")) + [
    WORK / "verification.k",
    WORK / "spec-original.k",
]
START = re.compile(
    r"^\s*(configuration|syntax|rule|context|claim|alias)\b"
)
BOUNDARY = re.compile(
    r"(?:^\s*(configuration|syntax|rule|context|claim|alias|"
    r"module|endmodule|imports)\b)|(?:^requires\s+\")"
)
MODULE = re.compile(r"^\s*module\s+(\S+)")
IMPORT = re.compile(r"^\s*imports\s+(\S+)")


def normalize(lines: list[str]) -> str:
    return " ".join(part.strip() for part in lines if part.strip())


records: list[tuple[str, int, int, str, str, str, str]] = []
modules: dict[str, str] = {}
imports: dict[str, list[str]] = defaultdict(list)

for path in FILES:
    rel = path.relative_to(WORK).as_posix()
    lines = path.read_text().splitlines()
    for line in lines:
        if match := MODULE.match(line):
            modules[rel] = match.group(1)
        if match := IMPORT.match(line):
            imports[rel].append(match.group(1))
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1)
        start = index
        index += 1
        while index < len(lines):
            if BOUNDARY.match(lines[index]):
                break
            index += 1
        block_lines = lines[start:index]
        block = normalize(block_lines)
        attrs: list[str] = []
        for marker in (
            "function",
            "functional",
            "total",
            "simplification",
            "priority",
            "owise",
            "concrete",
            "symbol",
            "no-evaluators",
            "strict",
            "seqstrict",
        ):
            if re.search(rf"\b{re.escape(marker)}\b", block):
                attrs.append(marker)
        block_hash = hashlib.sha256(block.encode()).hexdigest()[:12]
        records.append(
            (rel, start + 1, index, kind, ",".join(attrs) or "-", block_hash, block)
        )

print("K SOURCE MODULES AND IMPORTS")
for path in FILES:
    rel = path.relative_to(WORK).as_posix()
    print(
        f"MODULE\t{rel}\t{modules.get(rel, '-')}\t"
        f"imports={','.join(imports.get(rel, [])) or '-'}"
    )

print("\nCOUNTS BY FILE AND KIND")
file_counts: dict[str, Counter[str]] = defaultdict(Counter)
attribute_counts: Counter[str] = Counter()
for rel, _start, _end, kind, attrs, _block_hash, _block in records:
    file_counts[rel][kind] += 1
    for attr in attrs.split(","):
        if attr != "-":
            attribute_counts[attr] += 1
for rel in sorted(file_counts):
    values = " ".join(
        f"{kind}={count}" for kind, count in sorted(file_counts[rel].items())
    )
    print(f"COUNT\t{rel}\t{values}\ttotal={sum(file_counts[rel].values())}")
print(f"TOTAL_RECORDS\t{len(records)}")
print(
    "ATTRIBUTE_COUNTS\t"
    + " ".join(f"{name}={count}" for name, count in sorted(attribute_counts.items()))
)

print("\nEXHAUSTIVE INVENTORY")
print("ID\tFILE\tLINES\tKIND\tATTRIBUTES\tSHA256_12\tNORMALIZED_DECLARATION")
for number, (rel, start, end, kind, attrs, block_hash, block) in enumerate(records, 1):
    print(
        f"K{number:04d}\t{rel}\t{start}-{end}\t{kind}\t{attrs}\t"
        f"{block_hash}\t{block}"
    )
