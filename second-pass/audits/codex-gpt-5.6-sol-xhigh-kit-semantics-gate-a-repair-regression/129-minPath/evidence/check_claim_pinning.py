#!/usr/bin/env python3
"""Compare the submitted MPY function term with the function embedded in spec.k."""

from __future__ import annotations

import hashlib
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/129-minPath")


def balanced_term(text: str, marker: str) -> str:
    start = text.index(marker)
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
    raise ValueError(f"unterminated term beginning at {marker!r}")


def normalize_units_and_space(term: str) -> str:
    # The translator prints empty K list arguments by omission; spec.k sometimes
    # spells the same K units explicitly.
    term = term.replace(".Stmts", "").replace(".Exprs", "")
    result: list[str] = []
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


submitted_text = (SCRATCH / "solution.mpy").read_text()
spec_text = (SCRATCH / "spec.k").read_text()
submitted = normalize_units_and_space(balanced_term(submitted_text, 'FuncDef("minPath"'))
embedded = normalize_units_and_space(balanced_term(spec_text, 'FuncDef("minPath"'))

print(f"submitted_normalized_length={len(submitted)}")
print(f"embedded_normalized_length={len(embedded)}")
print(f"submitted_sha256={hashlib.sha256(submitted.encode()).hexdigest()}")
print(f"embedded_sha256={hashlib.sha256(embedded.encode()).hexdigest()}")
print(f"FUNCTION_TERM_IDENTICAL_MODULO_EXPLICIT_UNITS={submitted == embedded}")

if submitted != embedded:
    differing = next(
        (
            index
            for index, (left, right) in enumerate(zip(submitted, embedded))
            if left != right
        ),
        min(len(submitted), len(embedded)),
    )
    print(f"first_difference_index={differing}")
    print(f"submitted_context={submitted[max(0, differing - 100):differing + 100]}")
    print(f"embedded_context={embedded[max(0, differing - 100):differing + 100]}")
    raise SystemExit(1)
