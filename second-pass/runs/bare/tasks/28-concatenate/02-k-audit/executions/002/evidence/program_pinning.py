#!/usr/bin/env python3
"""Mechanical constructor-token comparison between solution.mpy and the entry claim."""

from __future__ import annotations

import re
from pathlib import Path


TOKEN = re.compile(
    r'''
    "(?:\\.|[^"\\])*"       # quoted K string
    |[A-Za-z_][A-Za-z0-9_-]*  # identifier
    |[(),]                     # constructor punctuation
    ''',
    re.VERBOSE,
)


def without_line_comments(text: str) -> str:
    return re.sub(r"//[^\n]*", "", text)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(without_line_comments(text))


def extract_constructor_argument(all_tokens: list[str], constructor: str) -> list[str]:
    start = all_tokens.index(constructor)
    if all_tokens[start + 1] != "(":
        raise AssertionError(f"{constructor} is not followed by '('")
    depth = 0
    for index in range(start + 1, len(all_tokens)):
        token = all_tokens[index]
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
            if depth == 0:
                return all_tokens[start + 2 : index]
    raise AssertionError(f"unterminated {constructor} argument")


mpy_tokens = tokens(Path("/candidate/solution.mpy").read_text())
spec_tokens = tokens(Path("/candidate/spec.k").read_text())
claim_program_tokens = extract_constructor_argument(spec_tokens, "load")

print(f"solution_token_count={len(mpy_tokens)}")
print(f"claim_load_argument_token_count={len(claim_program_tokens)}")
print(f"constructor_tokens_equal={mpy_tokens == claim_program_tokens}")
print("solution_tokens=" + " ".join(mpy_tokens))
print("claim_load_argument_tokens=" + " ".join(claim_program_tokens))

invoke_start = spec_tokens.index("invoke")
invoke_window = spec_tokens[invoke_start : invoke_start + 9]
print("claim_invocation_prefix=" + " ".join(invoke_window))
binding_and_body_present = (
    "FuncDef" in claim_program_tokens
    and '"concatenate"' in claim_program_tokens
    and '"strings"' in claim_program_tokens
)
print(
    "function_binding_and_body_present="
    f"{binding_and_body_present}"
)

raise SystemExit(0 if mpy_tokens == claim_program_tokens else 1)
