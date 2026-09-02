#!/usr/bin/env python3
"""Exhaustive declaration-block inventory for all audited K source."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/52-below-threshold")
files = [
    ROOT / "reference-semantics/semantics.k",
    *sorted((ROOT / "reference-semantics/semantics").glob("*.k")),
    ROOT / "verification.k",
    ROOT / "spec.k",
]

start_re = re.compile(r"^  (configuration|context|syntax|rule|claim|alias)\b")
module_re = re.compile(r"^(requires|module|endmodule)\b")
attr_names = (
    "function",
    "total",
    "functional",
    "macro",
    "macro-rec",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "symbol",
    "no-evaluators",
    "strict",
    "seqstrict",
)

overall: Counter[str] = Counter()
attributes: Counter[str] = Counter()
blocks: list[tuple[Path, int, int, str, str]] = []

for path in files:
    lines = path.read_text().splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if start_re.match(line) or module_re.match(line)
    ]
    starts.append(len(lines))
    for position, start in enumerate(starts[:-1]):
        first = lines[start]
        module_match = module_re.match(first)
        declaration_match = start_re.match(first)
        kind = module_match.group(1) if module_match else declaration_match.group(1)
        end = starts[position + 1]
        block_lines = lines[start:end]
        while block_lines and (
            not block_lines[-1].strip()
            or block_lines[-1].lstrip().startswith("//")
        ):
            block_lines.pop()
        block = "\n".join(block_lines)
        overall[kind] += 1
        for attr in attr_names:
            if re.search(rf"\b{re.escape(attr)}\b", block):
                attributes[attr] += 1
        blocks.append((path, start + 1, start + len(block_lines), kind, block))

print("FILES=", len(files))
print("DECLARATION_BLOCKS=", len(blocks))
print("KIND_COUNTS=", dict(sorted(overall.items())))
print("ATTRIBUTE_BLOCK_COUNTS=", dict(sorted(attributes.items())))
for path, start, end, kind, block in blocks:
    relative = path.relative_to(ROOT)
    flattened = " ".join(part.strip() for part in block.splitlines())
    block_hash = hashlib.sha256(block.encode()).hexdigest()
    print(
        f"{relative}:{start}-{end}\t{kind}\tsha256={block_hash}\t{flattened}"
    )
