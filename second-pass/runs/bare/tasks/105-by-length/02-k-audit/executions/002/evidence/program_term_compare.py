#!/usr/bin/env python3
"""Mechanically compare solution.mpy with verification.k's #solutionProgram RHS."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")


def extract_balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    began = False
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
            began = True
        elif char == ")":
            depth -= 1
            if began and depth == 0:
                return text[start : index + 1]
    raise ValueError("unterminated #solutionProgram constructor term")


def strip_layout(text: str) -> str:
    output = []
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
    return "".join(output)


def main() -> int:
    verification = (SCRATCH / "verification.k").read_text()
    marker = "rule #solutionProgram =>"
    marker_at = verification.index(marker) + len(marker)
    term_at = verification.index("Module(", marker_at)
    claim_term = extract_balanced_term(verification, term_at)
    submitted_term = (SCRATCH / "solution.mpy").read_text()

    normalized_claim = strip_layout(claim_term)
    normalized_submitted = strip_layout(submitted_term)
    claim_hash = hashlib.sha256(normalized_claim.encode()).hexdigest()
    submitted_hash = hashlib.sha256(normalized_submitted.encode()).hexdigest()
    equal = normalized_claim == normalized_submitted

    print("comparison=constructor term with layout-only normalization")
    print(f"claim_term_sha256={claim_hash}")
    print(f"submitted_term_sha256={submitted_hash}")
    print(f"equal={equal}")
    print(f"RESULT={'PASS' if equal else 'FAIL'}")
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
