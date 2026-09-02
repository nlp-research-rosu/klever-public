#!/usr/bin/env python3
"""Check that the entry claim's source term is the submitted .mpy term."""

from __future__ import annotations

import re
from pathlib import Path


solution_text = Path("/candidate/solution.mpy").read_text(encoding="utf-8")
spec_text = Path("/candidate/spec.k").read_text(encoding="utf-8")

k_cell = re.search(r"<k>(.*?)</k>", spec_text, flags=re.DOTALL)
if k_cell is None:
    raise SystemExit("spec.k has no <k> cell")

claim_lhs, separator, claim_rhs = k_cell.group(1).partition("=>")
if not separator:
    raise SystemExit("spec.k <k> cell has no rewrite")


def ignore_layout(text: str) -> str:
    return re.sub(r"\s+", "", text)


lhs_matches_submitted = ignore_layout(claim_lhs) == ignore_layout(solution_text)
print(f"submitted_mpy_normalized={ignore_layout(solution_text)}")
print(f"claim_lhs_normalized={ignore_layout(claim_lhs)}")
print(f"claim_rhs_normalized={ignore_layout(claim_rhs)}")
print(f"claim_lhs_matches_submitted={lhs_matches_submitted}")
raise SystemExit(0 if lhs_matches_submitted else 1)
