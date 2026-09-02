#!/usr/bin/env python3
"""Mechanically compare submitted solution.mpy with solutionProgram's K RHS."""

from __future__ import annotations

import hashlib
from pathlib import Path


WORK = Path("/tmp/audit-work/candidate-fresh")


def strip_k_whitespace_outside_strings(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for character in text:
        if in_string:
            output.append(character)
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
        elif character == '"':
            in_string = True
            output.append(character)
        elif not character.isspace():
            output.append(character)
    if in_string:
        raise ValueError("unterminated K string")
    return "".join(output)


verification = (WORK / "verification.k").read_text(encoding="utf-8")
marker = "rule solutionProgram =>"
if verification.count(marker) != 1:
    raise SystemExit(f"expected exactly one {marker!r}")
rhs_and_tail = verification.split(marker, 1)[1]
if rhs_and_tail.count("endmodule") != 1:
    raise SystemExit("unexpected verification.k tail")
rhs = rhs_and_tail.rsplit("endmodule", 1)[0]
submitted = (WORK / "solution.mpy").read_text(encoding="utf-8")

normalized_rhs = strip_k_whitespace_outside_strings(rhs)
normalized_submitted = strip_k_whitespace_outside_strings(submitted)
print(f"submitted_normalized_bytes={len(normalized_submitted.encode())}")
print(f"claim_rhs_normalized_bytes={len(normalized_rhs.encode())}")
print(f"submitted_sha256={hashlib.sha256(normalized_submitted.encode()).hexdigest()}")
print(f"claim_rhs_sha256={hashlib.sha256(normalized_rhs.encode()).hexdigest()}")
print(f"constructor_terms_equal={normalized_submitted == normalized_rhs}")
raise SystemExit(0 if normalized_submitted == normalized_rhs else 1)
