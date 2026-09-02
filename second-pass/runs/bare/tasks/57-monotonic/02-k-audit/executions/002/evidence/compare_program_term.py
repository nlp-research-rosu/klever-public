#!/usr/bin/env python3
"""Mechanical constructor/token comparison of solution.mpy and proof constant."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


MPY = Path("/tmp/audit-work/57-monotonic/solution.regenerated.mpy")
VERIFICATION = Path("/tmp/audit-work/57-monotonic/verification.k")

TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"|#[A-Za-z_][A-Za-z0-9_-]*|'
    r"[A-Za-z_][A-Za-z0-9_-]*|-?[0-9]+|[(),]"
)


def balanced_constructor(text: str, marker: str) -> str:
    marker_offset = text.index(marker) + len(marker)
    start = text.index("Module", marker_offset)
    open_paren = text.index("(", start)
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
                return text[start : index + 1]
    raise ValueError("unbalanced constructor after solutionProgram rule")


def tokens(text: str) -> list[str]:
    result = TOKEN.findall(text)
    residue = TOKEN.sub("", text)
    if residue.strip():
        raise ValueError(f"unparsed non-whitespace residue: {residue!r}")
    return result


def digest(values: list[str]) -> str:
    return hashlib.sha256("\0".join(values).encode()).hexdigest()


def main() -> int:
    mpy_text = MPY.read_text()
    proof_text = balanced_constructor(
        VERIFICATION.read_text(), "rule solutionProgram =>"
    )
    mpy_tokens = tokens(mpy_text)
    proof_tokens = tokens(proof_text)
    equal = mpy_tokens == proof_tokens
    print(f"translated_program={MPY}")
    print(f"proof_program_source={VERIFICATION}")
    print(f"translated_token_count={len(mpy_tokens)}")
    print(f"proof_rhs_token_count={len(proof_tokens)}")
    print(f"translated_token_sha256={digest(mpy_tokens)}")
    print(f"proof_rhs_token_sha256={digest(proof_tokens)}")
    print(f"constructor_token_identity={equal}")
    if not equal:
        for index, (left, right) in enumerate(
            zip(mpy_tokens, proof_tokens, strict=False)
        ):
            if left != right:
                print(f"first_difference_index={index} translated={left!r} proof={right!r}")
                break
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
