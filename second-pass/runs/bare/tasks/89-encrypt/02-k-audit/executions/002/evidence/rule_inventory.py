#!/usr/bin/env python3
"""Emit a bounded, exhaustive inventory of local K declarations and rules."""

from __future__ import annotations

import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/candidate-src/semantic.k"),
    Path("/tmp/audit-work/candidate-src/verification.k"),
    Path("/tmp/audit-work/candidate-src/spec.k"),
]
START = re.compile(
    r"^(module |endmodule|  imports |  syntax |  configuration|  rule |  claim )"
)


for path in FILES:
    lines = path.read_text().splitlines()
    items = []
    current_start = None
    current_lines = []
    for number, line in enumerate(lines, 1):
        if START.match(line):
            if current_lines:
                items.append((current_start, current_lines))
            current_start = number
            current_lines = [line]
        elif current_lines:
            current_lines.append(line)
    if current_lines:
        items.append((current_start, current_lines))

    syntax_count = sum(block[0].lstrip().startswith("syntax ") for _, block in items)
    rule_count = sum(block[0].lstrip().startswith("rule ") for _, block in items)
    claim_count = sum(block[0].lstrip().startswith("claim ") for _, block in items)
    config_count = sum(
        block[0].lstrip().startswith("configuration") for _, block in items
    )
    print(
        f"FILE {path.name} syntax={syntax_count} rules={rule_count} "
        f"claims={claim_count} configurations={config_count}"
    )
    for index, (start, block) in enumerate(items, 1):
        compact = " ".join(part.strip() for part in block if part.strip())
        compact = re.sub(r"\s+", " ", compact)
        print(f"ITEM {path.name}:{start} {compact}")

mpy = Path("/tmp/audit-work/candidate-src/solution.mpy").read_text()
constructors = sorted(set(re.findall(r"\b[A-Z][A-Za-z0-9]*\s*\(", mpy)))
constructors = [value.rstrip().rstrip("(").rstrip() for value in constructors]
operators = sorted(set(re.findall(r'^\s*"([+%=-]+)",?\s*$', mpy, re.MULTILINE)))
print(f"PROGRAM_CONSTRUCTORS {constructors}")
print(f"PROGRAM_OPERATOR_TOKENS {operators}")
