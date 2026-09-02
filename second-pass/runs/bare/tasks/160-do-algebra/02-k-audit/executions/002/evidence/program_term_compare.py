#!/usr/bin/env python3
"""Mechanical constructor-token comparison of solution.mpy and entry claim."""

from __future__ import annotations

import re
from pathlib import Path


work = Path("/tmp/audit-work/160-do-algebra/candidate")


def balanced_constructor(text: str, marker: str) -> str:
    start = text.index(marker)
    depth = 0
    quoted = False
    escaped = False
    opened = False
    for position in range(start, len(text)):
        char = text[position]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
            opened = True
        elif char == ")":
            depth -= 1
            if opened and depth == 0:
                return text[start : position + 1]
    raise ValueError(f"unbalanced constructor after {marker!r}")


token_pattern = re.compile(
    r'"(?:\\.|[^"\\])*"|[A-Za-z][A-Za-z0-9-]*|-?[0-9]+|[(),]'
)


def tokens(text: str):
    return token_pattern.findall(text)


solution = balanced_constructor((work / "solution.mpy").read_text(), "Module(")
spec = balanced_constructor((work / "spec.k").read_text(), "Module(")
verification = balanced_constructor(
    (work / "verification.k").read_text(), "Module("
)

solution_tokens = tokens(solution)
spec_tokens = tokens(spec)
verification_tokens = tokens(verification)

print(f"solution_token_count={len(solution_tokens)}")
print(f"entry_claim_token_count={len(spec_tokens)}")
print(f"solutionProgram_token_count={len(verification_tokens)}")
print(f"entry_claim_constructor_equal={solution_tokens == spec_tokens}")
print(f"solutionProgram_constructor_equal={solution_tokens == verification_tokens}")

if solution_tokens != spec_tokens or solution_tokens != verification_tokens:
    for name, other in (("entry", spec_tokens), ("solutionProgram", verification_tokens)):
        for index, (left, right) in enumerate(zip(solution_tokens, other)):
            if left != right:
                print(f"first_{name}_difference={index}:{left!r}!={right!r}")
                break
    raise SystemExit(1)
