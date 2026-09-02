#!/usr/bin/env python3
"""Emit an exhaustive, line-addressed K declaration/rule inventory."""

from __future__ import annotations

import collections
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/161-solve/source")
PATHS = (
    sorted((ROOT / "reference-semantics").rglob("*.k"))
    + [ROOT / "verification.k", ROOT / "spec.k"]
)

START = re.compile(
    r"^\s*(configuration|syntax(?:\s+priorities|\s+associativity)?|"
    r"rule|claim|context|alias)\b"
)
STOP = re.compile(r"^\s*(module|endmodule|imports)\b")
SPECIAL = re.compile(
    r"\[(?:[^\]]*\b(?:function|total|functional|simplification|"
    r"priority|owise|anywhere|macro|macro-rec|symbol|no-evaluators)\b[^\]]*)\]"
)

grand = collections.Counter()

for path in PATHS:
    lines = path.read_text(encoding="utf-8").splitlines()
    records = []
    index = 0
    while index < len(lines):
        match = START.match(lines[index])
        if not match:
            index += 1
            continue
        kind = match.group(1).replace(" ", "_")
        start = index
        index += 1
        while index < len(lines):
            if START.match(lines[index]) or STOP.match(lines[index]):
                break
            if not lines[index].strip():
                index += 1
                break
            index += 1
        body = " ".join(part.strip() for part in lines[start:index] if part.strip())
        records.append((kind, start + 1, body))

    rel = path.relative_to(ROOT)
    counts = collections.Counter(kind for kind, _, _ in records)
    grand.update(counts)
    print(f"FILE {rel} records={len(records)} counts={dict(sorted(counts.items()))}")
    for kind, line, body in records:
        attrs = ",".join(SPECIAL.findall(body))
        suffix = f" ATTRS={attrs}" if attrs else ""
        print(f"  {line:04d} {kind}: {body}{suffix}")

print(f"TOTAL records={sum(grand.values())} counts={dict(sorted(grand.items()))}")
