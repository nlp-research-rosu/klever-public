#!/usr/bin/env python3
"""Mechanically compare the submitted MPY tree with verification.k's #solution RHS."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


mpy_path = Path("/tmp/audit-work/fresh/solution.mpy")
verification_path = Path("/tmp/audit-work/fresh/verification.k")


def balanced_module(text: str, start: int) -> str:
    depth = 0
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
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError("unbalanced Module(...) term")


def tokens(text: str) -> list[str]:
    values = re.findall(r'"(?:\\.|[^"\\])*"|\.Stmts|#[A-Za-z0-9_]+|[A-Za-z_][A-Za-z0-9_]*|-?[0-9]+|[(),]', text)
    # The transliterator prints an empty Stmts list as no token between
    # delimiters; verification.k spells the same K list unit explicitly.
    return [value for value in values if value != ".Stmts"]


mpy_text = mpy_path.read_text()
verification_text = verification_path.read_text()
rule_position = verification_text.index("rule #solution =>")
rhs_start = verification_text.index("Module(", rule_position)
rhs_text = balanced_module(verification_text, rhs_start)

mpy_tokens = tokens(mpy_text)
rhs_tokens = tokens(rhs_text)
same = mpy_tokens == rhs_tokens
print(f"solution_mpy_sha256={hashlib.sha256(mpy_path.read_bytes()).hexdigest()}")
print(f"verification_k_sha256={hashlib.sha256(verification_path.read_bytes()).hexdigest()}")
print(f"solution_token_count={len(mpy_tokens)}")
print(f"solution_rhs_token_count={len(rhs_tokens)}")
print(f"token_identical_modulo_empty_Stmts_spelling={same}")
if not same:
    for index, (left, right) in enumerate(zip(mpy_tokens, rhs_tokens)):
        if left != right:
            print(f"first_difference index={index} mpy={left!r} rhs={right!r}")
            break
    if len(mpy_tokens) != len(rhs_tokens):
        print(f"length_difference={len(mpy_tokens) - len(rhs_tokens)}")
raise SystemExit(0 if same else 1)
