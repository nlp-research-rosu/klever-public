#!/usr/bin/env python3
"""Mechanical token comparison of solution.mpy's function body and the claim body."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_.][A-Za-z0-9_.-]*|-?[0-9]+|[(),]')


def tokens(path: str) -> list[str]:
    return TOKEN.findall(Path(path).read_text())


mpy = tokens("solution.mpy")
expected_prefix = [
    "Module", "(", "FuncDef", "(", '"get_max_triples"', ",",
    "Params", "(", '"n"', ")", ",",
]
if mpy[: len(expected_prefix)] != expected_prefix:
    raise AssertionError(f"unexpected solution.mpy prefix: {mpy[:len(expected_prefix)]}")
if mpy[-2:] != [")", ")"]:
    raise AssertionError(f"unexpected solution.mpy suffix: {mpy[-5:]}")
mpy_body = mpy[len(expected_prefix) : -2]

verification_text = Path("verification.k").read_text()
match = re.search(
    r"rule\s+getMaxTriplesBody\s*=>\s*(.*?)\s*\.Stmts",
    verification_text,
    flags=re.DOTALL,
)
if match is None:
    raise AssertionError("getMaxTriplesBody rule not found")
verification_body = TOKEN.findall(match.group(1))

print(f"solution_body_tokens={len(mpy_body)}")
print(f"verification_body_tokens={len(verification_body)}")
print(f"token_sequences_equal={mpy_body == verification_body}")
if mpy_body != verification_body:
    for index, (left, right) in enumerate(zip(mpy_body, verification_body)):
        if left != right:
            print(f"first_difference_index={index} solution={left!r} verification={right!r}")
            break
    print(f"solution_tail={mpy_body[-20:]}")
    print(f"verification_tail={verification_body[-20:]}")
    raise SystemExit(1)
