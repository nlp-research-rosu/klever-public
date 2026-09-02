#!/usr/bin/env python3
"""Mechanically compare the translated program and the claim's executed term."""

from __future__ import annotations

from pathlib import Path


def strip_layout(text: str) -> str:
    output: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        else:
            if char == '"':
                quoted = True
                output.append(char)
            elif not char.isspace():
                output.append(char)
    if quoted:
        raise ValueError("unterminated string")
    return "".join(output)


solution = Path("/tmp/audit-work/candidate/solution.mpy").read_text()
spec = Path("/tmp/audit-work/candidate/spec.k").read_text()
k_start = spec.index("<k>") + len("<k>")
rewrite = spec.index("=> done", k_start)
claim_program = spec[k_start:rewrite]
solution_normalized = strip_layout(solution)
claim_normalized = strip_layout(claim_program)
print(f"solution_normalized_bytes={len(solution_normalized)}")
print(f"claim_normalized_bytes={len(claim_normalized)}")
print(f"constructor_terms_equal={solution_normalized == claim_normalized}")
if solution_normalized != claim_normalized:
    print("solution_term=" + solution_normalized)
    print("claim_term=" + claim_normalized)
    raise SystemExit(1)
