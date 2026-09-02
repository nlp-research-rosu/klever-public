#!/usr/bin/env python3
"""Mechanical token-level comparison of solution.mpy with solutionProgram's RHS."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def strip_space(text: str) -> str:
    return re.sub(r"\s+", "", text)


solution_text = (ROOT / "solution.mpy").read_text()
verification_text = (ROOT / "verification.k").read_text()
match = re.search(
    r"rule\s+solutionProgram\s*=>\s*(Module\(.*\))\s*endmodule\s*$",
    verification_text,
    flags=re.DOTALL,
)
if match is None:
    raise SystemExit("could not isolate solutionProgram rule RHS")

solution_normalized = strip_space(solution_text)
rhs_normalized = strip_space(match.group(1))

print(f"solution_normalized_sha256={hashlib.sha256(solution_normalized.encode()).hexdigest()}")
print(f"rhs_normalized_sha256={hashlib.sha256(rhs_normalized.encode()).hexdigest()}")
print(f"constructor_text_equal={solution_normalized == rhs_normalized}")
if solution_normalized != rhs_normalized:
    raise SystemExit(1)
