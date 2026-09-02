#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and #callAdd."""

from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path("/tmp/audit-work/53-add-clean")


def normalize_k(text: str) -> str:
    """Drop whitespace outside quoted strings without changing tokens."""
    output: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    assert not in_string
    return "".join(output)


def balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index]
    raise AssertionError(f"unbalanced marker: {marker}")


solution_term = normalize_k((ROOT / "solution.mpy").read_text())
verification = (ROOT / "verification.k").read_text()
loaded_term = normalize_k(balanced_argument(verification, "#loadAll("))
verification_normalized = normalize_k(verification)
spec_normalized = normalize_k((ROOT / "spec.k").read_text())

print(f"solution_term={solution_term}")
print(f"loaded_term={loaded_term}")
print(f"constructor_term_equal={solution_term == loaded_term}")
print(f"solution_term_sha256={hashlib.sha256(solution_term.encode()).hexdigest()}")
print(f"loaded_term_sha256={hashlib.sha256(loaded_term.encode()).hexdigest()}")

expected_call = '~>Call(Name("add"),Int(X),Int(Y))'
expected_entry = "<k>#callAdd(X:Int,Y:Int)=>X+IntY</k>"
print(f"actual_call_present={expected_call in verification_normalized}")
print(f"result_constraining_entry_present={expected_entry in spec_normalized}")

assert solution_term == loaded_term
assert expected_call in verification_normalized
assert expected_entry in spec_normalized
print("TERM_PINNING_CHECK=PASS")
