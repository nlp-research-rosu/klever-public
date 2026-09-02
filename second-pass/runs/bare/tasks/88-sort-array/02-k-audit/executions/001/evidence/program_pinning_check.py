#!/usr/bin/env python3
"""Check that every entry claim embeds the regenerated submitted program."""

from __future__ import annotations

import re
from pathlib import Path


scratch = Path("/tmp/audit-work/88-sort-array")
spec_text = (scratch / "spec.k").read_text(encoding="utf-8")
program_text = (scratch / "regenerated-solution.mpy").read_text(encoding="utf-8")


def normalized(text: str) -> str:
    return re.sub(r"\s+", "", text)


def module_terms(text: str) -> list[str]:
    terms: list[str] = []
    cursor = 0
    while True:
        start = text.find("Module(", cursor)
        if start < 0:
            return terms
        depth = 0
        end = None
        for index in range(start, len(text)):
            char = text[index]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        if end is None:
            raise ValueError(f"unbalanced Module term at offset {start}")
        terms.append(text[start:end])
        cursor = end


embedded = module_terms(spec_text)
expected = normalized(program_text)
print(f"embedded_module_terms={len(embedded)}")
for index, term in enumerate(embedded):
    matches = normalized(term) == expected
    print(f"claim[{index}]_program_matches={str(matches).lower()}")
    if not matches:
        print(f"claim[{index}]={normalized(term)}")
        print(f"expected={expected}")

if len(embedded) != 4 or any(normalized(term) != expected for term in embedded):
    raise SystemExit(1)
