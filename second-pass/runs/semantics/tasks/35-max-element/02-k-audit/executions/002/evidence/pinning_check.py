#!/usr/bin/env python3
"""Mechanical comparison of translated program and proof constructor term."""

from __future__ import annotations

import re
from pathlib import Path

WORK = Path("/tmp/audit-work/work")
submitted = (WORK / "solution.mpy").read_text(encoding="utf-8")
verification = (WORK / "verification.k").read_text(encoding="utf-8")

match = re.search(
    r"rule\s+maxElementProgram\s*=>\s*(Module\(.*?\)\)\))\s*\n",
    verification,
    flags=re.DOTALL,
)
if match is None:
    raise SystemExit("could not extract maxElementProgram RHS")
claim_program = match.group(1)


def constructor_normalize(term: str) -> str:
    return re.sub(r"\s+", "", term)


print("SUBMITTED:")
print(submitted.rstrip())
print("CLAIM PROGRAM RHS:")
print(claim_program)
print(f"normalized_submitted={constructor_normalize(submitted)}")
print(f"normalized_claim={constructor_normalize(claim_program)}")
assert constructor_normalize(submitted) == constructor_normalize(claim_program)
print("MECHANICAL_CONSTRUCTOR_IDENTITY=PASS")
