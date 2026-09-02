#!/usr/bin/env python3
"""Emit an exhaustive declaration/rule ledger for the audited K sources."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/55-fib-audit/candidate-src")
sources = sorted((SCRATCH / "reference-semantics").rglob("*.k"))
sources += [SCRATCH / "verification.k", SCRATCH / "spec.k"]

start_re = re.compile(
    r"^\s*(configuration|syntax|rule|claim|context(?:\s+alias)?)\b"
)
attribute_names = (
    "function",
    "total",
    "functional",
    "simplification",
    "concrete",
    "owise",
    "priority",
    "symbol",
    "no-evaluators",
    "macro",
    "strict",
    "seqstrict",
    "circularity",
    "depends",
)


def declared_attributes(block: str) -> list[str]:
    bracket_text = " ".join(re.findall(r"\[[^\]]*\]", block, re.DOTALL))
    return [
        name
        for name in attribute_names
        if re.search(rf"(?<![A-Za-z0-9-]){re.escape(name)}(?![A-Za-z0-9-])", bracket_text)
    ]


totals: Counter[str] = Counter()
print("K SOURCE INVENTORY")
print(f"SOURCE_COUNT={len(sources)}")

for source in sources:
    rel = source.relative_to(SCRATCH)
    raw = source.read_bytes()
    lines = raw.decode().splitlines()
    print(
        f"\nFILE {rel} lines={len(lines)} "
        f"sha256={hashlib.sha256(raw).hexdigest()}"
    )
    starts = [i for i, line in enumerate(lines) if start_re.match(line)]
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:stop])
        match = start_re.match(lines[start])
        assert match is not None
        kind = match.group(1).replace(" ", "_")
        totals[kind] += 1
        attrs = declared_attributes(block)
        for attr in attrs:
            totals[f"attr:{attr}"] += 1
        headline = re.sub(r"\s+", " ", block).strip()
        if len(headline) > 360:
            headline = headline[:357] + "..."
        print(
            f"{rel}:{start + 1}: kind={kind} "
            f"attrs={','.join(attrs) if attrs else '-'} :: {headline}"
        )

print("\nTOTALS")
for key in sorted(totals):
    print(f"{key}={totals[key]}")

print("\nSPECIAL ATTRIBUTE OCCURRENCES")
special_re = re.compile(
    r"\b(function|total|functional|simplification|concrete|owise|priority|"
    r"symbol|no-evaluators|macro|strict|seqstrict|circularity|depends)\b"
)
for source in sources:
    rel = source.relative_to(SCRATCH)
    for number, line in enumerate(source.read_text().splitlines(), 1):
        uncommented = line.split("//", 1)[0]
        if "[" in uncommented and special_re.search(uncommented):
            print(f"{rel}:{number}: {line.strip()}")
