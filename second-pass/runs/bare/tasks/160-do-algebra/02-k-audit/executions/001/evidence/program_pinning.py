#!/usr/bin/env python3
"""Check that proof spellings contain exactly the trusted-translated program term."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def extract_constructor(text: str, constructor: str) -> str:
    start = text.index(constructor + "(")
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unterminated {constructor} constructor")


def normalize(term: str) -> str:
    result = []
    quoted = False
    escaped = False
    for character in term:
        if quoted:
            result.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
        elif character == '"':
            quoted = True
            result.append(character)
        elif not character.isspace():
            result.append(character)
    return "".join(result)


solution = normalize((ROOT / "regenerated-solution.mpy").read_text(encoding="utf-8"))
spec = normalize(
    extract_constructor((ROOT / "spec.k").read_text(encoding="utf-8"), "Module")
)
verification = normalize(
    extract_constructor(
        (ROOT / "verification.k").read_text(encoding="utf-8"), "Module"
    )
)

for name, term in [
    ("trusted_regenerated_solution", solution),
    ("entry_claim_program", spec),
    ("solutionProgram_helper", verification),
]:
    print(f"{name}_sha256={hashlib.sha256(term.encode()).hexdigest()}")
    print(f"{name}_length={len(term)}")

print(f"entry_claim_exact_match={spec == solution}")
print(f"solutionProgram_exact_match={verification == solution}")
raise SystemExit(0 if spec == solution and verification == solution else 1)
