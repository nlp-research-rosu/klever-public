#!/usr/bin/env python3
"""Mechanically compare the program inside program-correct with solution.mpy."""

from __future__ import annotations

import hashlib
import pathlib
import re


SPEC = pathlib.Path("/tmp/audit-work/candidate/spec.k")
MPY = pathlib.Path("/tmp/audit-work/candidate/solution.mpy")
REGENERATED = pathlib.Path(
    "/tmp/audit-work/candidate/solution.regenerated.mpy"
)


def boot_argument(text: str) -> str:
    marker = "#boot("
    start = text.index(marker, text.index("claim [program-correct]:")) + len(marker)
    depth = 1
    in_string = False
    escaped = False
    index = start
    while index < len(text):
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
        index += 1
    raise ValueError("unterminated #boot argument")


def tokens(text: str):
    token_re = re.compile(
        r'"(?:\\.|[^"\\])*"'
        r"|[.]?[A-Za-z_#?][A-Za-z0-9_#?\\-]*"
        r"|-?[0-9]+|[(),]"
    )
    matched = token_re.findall(text)
    residue = token_re.sub("", text)
    if residue.strip():
        raise ValueError(f"unparsed residue: {residue!r}")
    return matched


spec_program = boot_argument(SPEC.read_text(encoding="utf-8"))
submitted = MPY.read_text(encoding="utf-8")
regenerated = REGENERATED.read_text(encoding="utf-8")

spec_tokens = tokens(spec_program)
submitted_tokens = tokens(submitted)
regenerated_tokens = tokens(regenerated)
spec_normalized = [token for token in spec_tokens if token != ".Stmts"]
submitted_normalized = [token for token in submitted_tokens if token != ".Stmts"]
regenerated_normalized = [token for token in regenerated_tokens if token != ".Stmts"]

print("SPEC_BOOT_TOKEN_COUNT=", len(spec_tokens))
print("SUBMITTED_MPY_TOKEN_COUNT=", len(submitted_tokens))
print("REGENERATED_MPY_TOKEN_COUNT=", len(regenerated_tokens))
print("SPEC_EXPLICIT_EMPTY_STMTS=", spec_tokens.count(".Stmts"))
print("SUBMITTED_EXPLICIT_EMPTY_STMTS=", submitted_tokens.count(".Stmts"))
print(
    "SPEC_NORMALIZED_TERM_SHA256=",
    hashlib.sha256("\n".join(spec_normalized).encode()).hexdigest(),
)
print(
    "SUBMITTED_NORMALIZED_TERM_SHA256=",
    hashlib.sha256("\n".join(submitted_normalized).encode()).hexdigest(),
)
print(
    "SPEC_EQUALS_SUBMITTED_K_TERM=",
    spec_normalized == submitted_normalized,
)
print(
    "SUBMITTED_EQUALS_REGENERATED_K_TERM=",
    submitted_normalized == regenerated_normalized,
)
assert spec_normalized == submitted_normalized == regenerated_normalized
