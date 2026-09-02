#!/usr/bin/env python3
"""Exhaustive source-level K declaration/rule inventory."""

from __future__ import annotations

import collections
import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/39-prime-fib-audit")
paths = sorted((ROOT / "reference-semantics").rglob("*.k"))
paths += [ROOT / "verification.k", ROOT / "spec.k"]

decl_re = re.compile(r"^\s*(configuration|syntax|context|rule|claim)\b")
attrs = (
    "function",
    "functional",
    "total",
    "opaque",
    "symbol",
    "no-evaluators",
    "priority",
    "simplification",
    "concrete",
    "macro",
    "macro-rec",
    "owise",
    "strict",
    "seqstrict",
)

grand = collections.Counter()
print("SOURCE FILES AND HASHES")
for path in paths:
    data = path.read_bytes()
    rel = path.relative_to(ROOT)
    print(f"{hashlib.sha256(data).hexdigest()}  {rel}")

print("\nPER-FILE COUNTS")
for path in paths:
    counts = collections.Counter()
    text = path.read_text()
    for raw in text.splitlines():
        code = raw.split("//", 1)[0]
        match = decl_re.match(code)
        if match:
            counts[match.group(1)] += 1
        for attr in attrs:
            counts[f"attr:{attr}"] += len(
                re.findall(rf"(?<![A-Za-z0-9_-]){re.escape(attr)}(?![A-Za-z0-9_-])", code)
            )
    grand.update(counts)
    rel = path.relative_to(ROOT)
    rendered = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"{rel}: {rendered}")

print("\nGRAND COUNTS")
print(" ".join(f"{key}={grand[key]}" for key in sorted(grand)))

print("\nEVERY DECLARATION / CONTEXT / RULE / CLAIM")
for path in paths:
    rel = path.relative_to(ROOT)
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        code = raw.split("//", 1)[0]
        match = decl_re.match(code)
        if match:
            print(f"{rel}:{lineno}:{match.group(1)}:{code.strip()}")

print("\nEVERY ATTRIBUTE-BEARING SOURCE LINE")
for path in paths:
    rel = path.relative_to(ROOT)
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        code = raw.split("//", 1)[0]
        if any(
            re.search(rf"(?<![A-Za-z0-9_-]){re.escape(attr)}(?![A-Za-z0-9_-])", code)
            for attr in attrs
        ):
            print(f"{rel}:{lineno}:{code.strip()}")
