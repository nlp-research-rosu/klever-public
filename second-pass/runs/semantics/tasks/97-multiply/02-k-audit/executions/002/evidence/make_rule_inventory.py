#!/usr/bin/env python3
"""Emit a line-addressable inventory of all submitted K declarations."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOT = Path("/tmp/audit-work/97-multiply")
files = sorted((ROOT / "reference-semantics").rglob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

start_re = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
attribute_names = (
    "function",
    "functional",
    "total",
    "simplification",
    "concrete",
    "priority",
    "owise",
    "macro",
    "macro-rec",
    "symbol",
    "no-evaluators",
)

grand = Counter()
attribute_counts = Counter()
inventory: list[tuple[str, int, str, str, str]] = []

for path in files:
    text = path.read_text(encoding="utf-8")
    relative = path.relative_to(ROOT).as_posix()
    digest = hashlib.sha256(text.encode()).hexdigest()
    lines = text.splitlines()
    starts: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        match = start_re.match(line)
        if match:
            starts.append((index, match.group(1)))
    print(
        f"FILE {relative} sha256={digest} "
        f"declarations={len(starts)}"
    )
    for position, (index, kind) in enumerate(starts):
        end = starts[position + 1][0] if position + 1 < len(starts) else len(lines)
        block_lines = []
        for line in lines[index:end]:
            stripped = line.strip()
            if not stripped or stripped.startswith("//"):
                continue
            block_lines.append(stripped)
        block = " ".join(block_lines)
        block = re.sub(r"\s+", " ", block)
        bracket_text = " ".join(re.findall(r"\[([^\]]*)\]", block))
        attributes = [
            name for name in attribute_names
            if re.search(rf"\b{re.escape(name)}\b", bracket_text)
        ]
        for attribute in attributes:
            attribute_counts[attribute] += 1
        grand[kind] += 1
        inventory.append(
            (relative, index + 1, kind, ",".join(attributes) or "-", block)
        )

print("SUMMARY")
for kind in ("configuration", "syntax", "context", "rule", "claim"):
    print(f"{kind}={grand[kind]}")
for attribute in attribute_names:
    print(f"attribute_{attribute}={attribute_counts[attribute]}")
print("INVENTORY")
for relative, line, kind, attributes, block in inventory:
    print(f"{relative}:{line} | {kind} | {attributes} | {block}")
