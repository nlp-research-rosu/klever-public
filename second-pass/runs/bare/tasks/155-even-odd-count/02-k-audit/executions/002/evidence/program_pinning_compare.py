#!/usr/bin/env python3
"""Check that the pinning claim's RHS is the submitted .mpy constructor text."""

from __future__ import annotations

import re
from pathlib import Path


root = Path("/tmp/audit-work/155-even-odd-count-audit/reconstruction")
claim_path = root / "spec-program-pinning.k"
program_path = Path("/tmp/audit-work/155-even-odd-count-audit/source/solution.mpy")
rhs_path = root / "pinning-rhs.mpy"


def erase_layout(text: str) -> str:
    return re.sub(r"\s+", "", text)


def normalize_empty_statements(text: str) -> str:
    # The translator prints an empty List{Stmt,""} as no characters, whereas
    # a K claim must spell the same list unit explicitly as .Stmts.
    return erase_layout(text).replace(".Stmts", "")


print(f"claim_file={claim_path}")
print(f"submitted_program={program_path}")
print(f"explicit_claim_rhs={rhs_path}")
claim = claim_path.read_text()
match = re.search(
    r"claim\s+solutionProgram\(\)\s*=>\s*(Module\(.*\))\s*endmodule",
    claim,
    re.DOTALL,
)
assert match, "could not extract pinning-claim RHS"
claim_rhs = match.group(1)
rhs = rhs_path.read_text()
program = program_path.read_text()
claim_matches_rhs = erase_layout(claim_rhs) == erase_layout(rhs)
constructor_identity = normalize_empty_statements(rhs) == normalize_empty_statements(program)
print(f"claim_rhs_matches_explicit_rhs={claim_matches_rhs}")
print("normalization=erase layout and equate explicit .Stmts with blank Stmts list")
print(f"constructor_identity_after_empty_list_normalization={constructor_identity}")
if not claim_matches_rhs or not constructor_identity:
    raise SystemExit(1)
