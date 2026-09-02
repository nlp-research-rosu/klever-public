#!/usr/bin/env python3
"""Mechanically compare each claim's Module constructor to solution.mpy."""

from __future__ import annotations

from pathlib import Path


def normalize_outside_strings(text: str) -> str:
    result: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    if quoted:
        raise ValueError("unterminated string literal")
    return "".join(result)


def balanced_module_terms(text: str) -> list[str]:
    terms: list[str] = []
    cursor = 0
    while True:
        start = text.find("Module(", cursor)
        if start < 0:
            break
        depth = 0
        quoted = False
        escaped = False
        end = None
        for index in range(start, len(text)):
            char = text[index]
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char == "(":
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
    return terms


solution = Path(
    "/tmp/audit-work/83-review/candidate/solution.mpy"
).read_text(encoding="utf-8")
spec = Path(
    "/tmp/audit-work/83-review/candidate/spec.k"
).read_text(encoding="utf-8")

expected = normalize_outside_strings(solution)
terms = balanced_module_terms(spec)
matches = [normalize_outside_strings(term) == expected for term in terms]

print(f"SOLUTION_NORMALIZED_LENGTH: {len(expected)}")
print(f"CLAIM_MODULE_TERMS: {len(terms)}")
for index, match in enumerate(matches, 1):
    print(f"CLAIM_{index}_MODULE_EQUALS_SOLUTION_MPY: {match}")

if len(terms) != 2 or not all(matches):
    raise SystemExit(1)
