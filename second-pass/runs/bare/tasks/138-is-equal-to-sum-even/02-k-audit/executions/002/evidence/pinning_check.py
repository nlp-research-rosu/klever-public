#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and claim programs."""

from __future__ import annotations

import re
from pathlib import Path


def remove_layout(text: str) -> str:
    result = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            result.append(char)
        elif not char.isspace():
            result.append(char)
    return "".join(result)


def main() -> int:
    scratch = Path("/tmp/audit-work/138-audit/scratch")
    program = scratch.joinpath("solution.mpy").read_text()
    spec = scratch.joinpath("spec.k").read_text()
    terms = re.findall(
        r"<k>\s*(Module\(.*?\))\s*=>\s*\.K\s*</k>",
        spec,
        flags=re.DOTALL,
    )
    assert len(terms) == 5, f"expected five program-executing claims, found {len(terms)}"
    normalized_program = remove_layout(program)
    comparisons = [remove_layout(term) == normalized_program for term in terms]
    print("translated_program_normalized:", normalized_program)
    print("program_claim_count:", len(terms))
    print("constructor_level_equalities:", comparisons)
    print("all_program_claims_pin_solution_mpy:", all(comparisons))
    return 0 if all(comparisons) else 1


if __name__ == "__main__":
    raise SystemExit(main())
