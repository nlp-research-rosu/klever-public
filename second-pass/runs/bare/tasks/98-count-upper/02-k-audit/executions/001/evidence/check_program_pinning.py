#!/usr/bin/env python3
"""Mechanically compare the claim's ground Program body with solution.mpy."""

from __future__ import annotations

import hashlib
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/98-count-upper-audit-20260726")


def extract_balanced(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    start = text.index("Module(", start)
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
    raise ValueError("unbalanced Module term")


def strip_unquoted_whitespace(text: str) -> str:
    result: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    return "".join(result)


def normalize_list_syntax(text: str) -> str:
    # The Stmts list production permits an omitted empty list in constructor
    # argument position.  verification.k spells the same term as `.Stmts`.
    return strip_unquoted_whitespace(text).replace(",)", ",.Stmts)")


def main() -> int:
    submitted = (SCRATCH / "solution.mpy").read_text(encoding="utf-8")
    verification = (SCRATCH / "verification.k").read_text(encoding="utf-8")
    claim_body = extract_balanced(verification, "rule countUpperProgram")

    submitted_normal = normalize_list_syntax(submitted)
    claim_normal = normalize_list_syntax(claim_body)
    equal = submitted_normal == claim_normal
    print(f"submitted_normal_sha256={hashlib.sha256(submitted_normal.encode()).hexdigest()}")
    print(f"claim_body_normal_sha256={hashlib.sha256(claim_normal.encode()).hexdigest()}")
    print(f"constructor_terms_equal={equal}")
    if not equal:
        print(f"SUBMITTED={submitted_normal}")
        print(f"CLAIM_BODY={claim_normal}")
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
