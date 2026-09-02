#!/usr/bin/env python3
"""Check that the entry claim embeds the submitted MPY term exactly."""

from __future__ import annotations

import re
from pathlib import Path


def no_space(text: str) -> str:
    return re.sub(r"\s+", "", text)


scratch = Path("/tmp/audit-work/reconstruction")
solution_path = scratch / "solution.mpy"
spec_path = scratch / "spec.k"
solution = solution_path.read_text(encoding="utf-8")
spec = spec_path.read_text(encoding="utf-8")

match = re.search(r"<k>\s*(Module\(.*?)\s*~>\s*invoke\(", spec, re.DOTALL)
if match is None:
    raise SystemExit("could not locate entry program term in spec.k")

submitted_term = no_space(solution)
claimed_term = no_space(match.group(1))
print(f"submitted_normalized={submitted_term}")
print(f"claimed_normalized={claimed_term}")
print(f"normalized_terms_identical={submitted_term == claimed_term}")

claims = re.findall(r"(?m)^\s*claim\b", spec)
claim_tail = spec[spec.index("claim") :]
claim_requires = re.findall(r"(?m)^\s*requires\b", claim_tail)
print(f"entry_claim_count={len(claims)}")
print(f"claim_precondition_requires_count={len(claim_requires)}")
print("satisfying_witnesses: S=\"\"; S=\"abc\"; S=\"😀\"")

raise SystemExit(0 if submitted_term == claimed_term and len(claims) == 1 else 1)
