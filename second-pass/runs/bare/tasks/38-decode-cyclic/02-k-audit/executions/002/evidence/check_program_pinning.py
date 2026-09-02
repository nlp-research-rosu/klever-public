#!/usr/bin/env python3
"""Mechanically compare the claimed K constructor term with solution.mpy."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


SEMANTIC = Path("/candidate/semantic.k")
MPY = Path("/candidate/solution.mpy")


TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|=>|[A-Za-z_][A-Za-z0-9_-]*|[0-9]+|[(),]|\S'
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def rhs_between(source: str, rule_name: str, end_marker: str) -> str:
    marker = f"rule {rule_name} =>"
    start = source.index(marker) + len(marker)
    end = source.index(end_marker, start)
    return source[start:end].strip()


def count_subsequence(haystack: list[str], needle: list[str]) -> int:
    if not needle:
        return 0
    return sum(
        haystack[index : index + len(needle)] == needle
        for index in range(len(haystack) - len(needle) + 1)
    )


semantic = SEMANTIC.read_text(encoding="utf-8")
mpy = MPY.read_text(encoding="utf-8")

program_rhs = rhs_between(
    semantic, "solutionProgram", "\n\n  // Independent accumulator specification"
)
decode_body_rhs = rhs_between(
    semantic, "decodeBody", '\n\n  syntax Expr ::= "decodeTest"'
)
decode_test_rhs = rhs_between(
    semantic, "decodeTest", '\n\n  syntax Stmts ::= "decodeReturn"'
)
decode_return_rhs = rhs_between(semantic, "decodeReturn", "\nendmodule")

program_tokens = tokens(program_rhs)
mpy_tokens = tokens(mpy)
body_tokens = tokens(decode_body_rhs)
test_tokens = tokens(decode_test_rhs)
return_tokens = tokens(decode_return_rhs)

checks = {
    "solutionProgram token-identical to trusted-regenerated solution.mpy": (
        program_tokens == mpy_tokens
    ),
    "decodeBody is an exact unique subterm of solutionProgram": (
        count_subsequence(program_tokens, body_tokens) == 1
    ),
    "decodeTest is an exact unique subterm of solutionProgram": (
        count_subsequence(program_tokens, test_tokens) == 1
    ),
    "decodeReturn is an exact unique subterm of solutionProgram": (
        count_subsequence(program_tokens, return_tokens) == 1
    ),
}

print(f"SEMANTIC: {SEMANTIC}")
print(f"SUBMITTED_MPY: {MPY}")
print(f"PROGRAM_TOKEN_COUNT: {len(program_tokens)}")
print(f"MPY_TOKEN_COUNT: {len(mpy_tokens)}")
print(
    "PROGRAM_TOKEN_SHA256: "
    + hashlib.sha256("\0".join(program_tokens).encode()).hexdigest()
)
print(
    "MPY_TOKEN_SHA256: "
    + hashlib.sha256("\0".join(mpy_tokens).encode()).hexdigest()
)
print(f"decodeBody occurrence count: {count_subsequence(program_tokens, body_tokens)}")
print(f"decodeTest occurrence count: {count_subsequence(program_tokens, test_tokens)}")
print(
    f"decodeReturn occurrence count: "
    f"{count_subsequence(program_tokens, return_tokens)}"
)
for description, passed in checks.items():
    print(f"{'OK' if passed else 'FAIL'} {description}")

if program_tokens != mpy_tokens:
    for index, (left, right) in enumerate(zip(program_tokens, mpy_tokens)):
        if left != right:
            print(f"FIRST_TOKEN_MISMATCH: index={index} program={left!r} mpy={right!r}")
            break
    if len(program_tokens) != len(mpy_tokens):
        print(
            "TOKEN_LENGTH_MISMATCH: "
            f"program={len(program_tokens)} mpy={len(mpy_tokens)}"
        )

sys.exit(0 if all(checks.values()) else 1)
