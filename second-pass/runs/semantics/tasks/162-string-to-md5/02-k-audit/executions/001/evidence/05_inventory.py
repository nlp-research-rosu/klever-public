#!/usr/bin/env python3
"""Exhaustive declaration/rule index for the audited K source corpus."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
import re

ROOT = Path("/tmp/audit-work/proof-162")
files = sorted((ROOT / "reference-semantics").rglob("*.k"))
files += [ROOT / "verification.k", ROOT / "spec.k"]

entry = re.compile(
    r"^\s*(configuration|syntax|context|rule|claim)\b"
)
attributes = (
    "function",
    "total",
    "functional",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "macro",
    "macro-rec",
    "owise",
    "concrete",
)

grand = Counter()
print("# Exhaustive K source inventory")
for path in files:
    data = path.read_bytes()
    text = data.decode()
    relative = path.relative_to(ROOT)
    local = Counter()
    starts = []
    for number, line in enumerate(text.splitlines(), 1):
        match = entry.match(line)
        if match:
            kind = match.group(1)
            local[kind] += 1
            starts.append((number, kind, line.strip()))
        code = line.split("//", 1)[0]
        for attribute in attributes:
            if re.search(rf"\b{re.escape(attribute)}\b", code):
                local[f"attr:{attribute}"] += 1
    grand.update(local)
    counts = " ".join(f"{key}={local[key]}" for key in sorted(local))
    print(
        f"\n## {relative} sha256={sha256(data).hexdigest()} "
        f"lines={len(text.splitlines())} {counts}"
    )
    for number, kind, line in starts:
        print(f"{relative}:{number}\t{kind}\t{line}")

print("\n# Grand totals")
for key in sorted(grand):
    print(f"{key}\t{grand[key]}")
