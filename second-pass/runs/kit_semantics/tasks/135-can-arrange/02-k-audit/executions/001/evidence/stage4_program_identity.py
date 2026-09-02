"""Mechanical constructor-token comparison for the whole-program claim."""

from __future__ import annotations

import re
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/135-can-arrange")
TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'
    r"|=>|~>"
    r"|#[A-Za-z_][A-Za-z0-9_-]*"
    r"|\.[A-Za-z_][A-Za-z0-9_-]*"
    r"|[A-Za-z_][A-Za-z0-9_-]*"
    r"|-?[0-9]+"
    r"|[(),]"
)


def tokens(text: str):
    found = TOKEN.findall(text)
    return [token for token in found if token != ".Stmts"]


def balanced_constructor(text: str, constructor: str, start: int = 0):
    begin = text.index(constructor + "(", start)
    open_paren = begin + len(constructor)
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_paren, len(text)):
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
                return text[begin:index + 1]
    raise ValueError(f"unbalanced {constructor}")


program_text = (SCRATCH / "solution.mpy").read_text()
spec_text = (SCRATCH / "spec.k").read_text()

program_module = balanced_constructor(program_text, "Module")
load_position = spec_text.index("#loadAll(")
claim_module = balanced_constructor(spec_text, "Module", load_position)

program_tokens = tokens(program_module)
claim_tokens = tokens(claim_module)

print("program_constructor_tokens", len(program_tokens))
print("claim_constructor_tokens", len(claim_tokens))
print("constructor_token_identity", program_tokens == claim_tokens)

if program_tokens != claim_tokens:
    for index, (left, right) in enumerate(
        zip(program_tokens, claim_tokens, strict=False)
    ):
        if left != right:
            print("first_difference", index, left, right)
            break
    raise SystemExit(1)
