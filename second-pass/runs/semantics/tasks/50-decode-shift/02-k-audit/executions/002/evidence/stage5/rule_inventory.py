#!/usr/bin/env python3
"""Produce a complete declaration/rule inventory for every audited K source."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from pathlib import Path


ROOTS = [
    Path("/tmp/audit-work/fresh/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/fresh/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/fresh/verification.k"),
    Path("/tmp/audit-work/fresh/spec.k"),
]

START = re.compile(
    r'^\s*(requires\s+"|module\b|endmodule\b|imports\b|configuration\b'
    r"|context\b|syntax\b|rule\b|claim\b)"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(text: str) -> str:
    stripped = text.lstrip()
    for category in (
        "requires",
        "module",
        "endmodule",
        "imports",
        "configuration",
        "context",
        "syntax",
        "rule",
        "claim",
    ):
        if stripped.startswith(category):
            return category
    return "other"


counts: Counter[str] = Counter()
attribute_counts: Counter[str] = Counter()
print("# Exhaustive K declaration and rule inventory")
print()
print(
    "Each source was consumed in full. Multiline entries include every line through "
    "the next K declaration. File hashes make the reviewed source set exact."
)

for path in ROOTS:
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    print()
    print(f"## {path}")
    print(f"lines={len(lines)} sha256={sha256(path)}")
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        block = "\n".join(lines[start:stop]).rstrip()
        category = classify(lines[start])
        counts[category] += 1
        for attribute in (
            "function",
            "functional",
            "total",
            "macro",
            "simplification",
            "concrete",
            "symbol",
            "no-evaluators",
            "priority",
            "owise",
            "strict",
            "seqstrict",
            "hook",
        ):
            if re.search(rf"\b{re.escape(attribute)}\b", block):
                attribute_counts[attribute] += 1
        indented = "\n".join(f"    {line}" for line in block.splitlines())
        print()
        print(f"### {category} at line {start + 1}")
        print("```k")
        print(indented)
        print("```")

print()
print("## Counts")
print("categories=" + repr(dict(sorted(counts.items()))))
print("attributes=" + repr(dict(sorted(attribute_counts.items()))))
