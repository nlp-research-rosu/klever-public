#!/usr/bin/env python3
"""Emit an exhaustive, line-numbered inventory of local K declarations."""

from __future__ import annotations

import re
from pathlib import Path


FILES = [
    Path("/tmp/audit-work/candidate/semantic.k"),
    Path("/tmp/audit-work/candidate/verification.k"),
    Path("/tmp/audit-work/candidate/spec.k"),
]
START = re.compile(
    r"^\s*(requires|module|imports|syntax|configuration|rule|claim|endmodule)\b"
)
ATTRIBUTE = re.compile(
    r"\[(?:[^\]]*\b(?:function|total|functional|simplification|concrete|owise|priority)\b[^\]]*)\]"
)


for path in FILES:
    lines = path.read_text().splitlines()
    print(f"===== {path.name} =====")
    starts = [index for index, line in enumerate(lines) if START.match(line)]
    rule_number = 0
    claim_number = 0
    syntax_number = 0
    for position, index in enumerate(starts):
        keyword = START.match(lines[index]).group(1)
        if keyword not in {"syntax", "configuration", "rule", "claim"}:
            print(f"META L{index + 1}: {lines[index].strip()}")
            continue
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        while end > index + 1 and not lines[end - 1].strip():
            end -= 1
        if keyword == "rule":
            rule_number += 1
            identifier = f"R{rule_number:02d}"
        elif keyword == "claim":
            claim_number += 1
            identifier = f"C{claim_number:02d}"
        elif keyword == "syntax":
            syntax_number += 1
            identifier = f"S{syntax_number:02d}"
        else:
            identifier = "CONFIG"
        print(f"{identifier} L{index + 1}-L{end}:")
        for line_number in range(index, end):
            print(f"  {line_number + 1:03d} {lines[line_number]}")
    attributes = [
        (number, match.group(0))
        for number, line in enumerate(lines, 1)
        for match in ATTRIBUTE.finditer(line)
    ]
    print(f"ATTRIBUTE_OCCURRENCES={attributes}")
    print(f"SYNTAX_COUNT={syntax_number}")
    print(f"RULE_COUNT={rule_number}")
    print(f"CLAIM_COUNT={claim_number}")
