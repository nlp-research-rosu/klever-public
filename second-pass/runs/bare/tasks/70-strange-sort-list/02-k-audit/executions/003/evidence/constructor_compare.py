#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and solutionProgram."""

from __future__ import annotations

import re
from pathlib import Path


mpy = Path("/tmp/audit-work/candidate-src/solution.mpy").read_text()
verification = Path("/tmp/audit-work/candidate-src/verification.k").read_text()

match = re.search(
    r"rule\s+solutionProgram\s*=>\s*(Module\(.*\))\s*"
    r"// Independent contract function:",
    verification,
    flags=re.DOTALL,
)
assert match is not None
program_term = match.group(1)


def normalize(text: str) -> str:
    # K treats omitted empty statement lists and translator whitespace as
    # semantically inert. Make the two explicit empty branches match.
    text = re.sub(r"\s+", "", text)
    text = text.replace(",.Stmts)", ",)")
    return text


normalized_mpy = normalize(mpy)
normalized_term = normalize(program_term)
print(f"normalized_solution_mpy={normalized_mpy}")
print(f"normalized_solutionProgram={normalized_term}")
print(f"byte_lengths={len(normalized_mpy)},{len(normalized_term)}")
assert normalized_mpy == normalized_term
print("CONSTRUCTOR COMPARISON PASS")
