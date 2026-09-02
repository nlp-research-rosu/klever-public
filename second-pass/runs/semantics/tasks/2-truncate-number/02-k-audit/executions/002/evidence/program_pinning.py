#!/usr/bin/env python3
"""Mechanical constructor-level pinning checks for the submitted program."""

from __future__ import annotations

import re
from pathlib import Path


work = Path("/tmp/audit-work/truncate2-reconstruction")
submitted = (work / "solution.mpy").read_text()
regenerated = (work / "regenerated-solution.mpy").read_text()
verification = (work / "verification.k").read_text()
spec = (work / "spec.k").read_text()


def strip_comments_and_space(text: str) -> str:
    text = re.sub(r"//[^\n]*", "", text)
    return re.sub(r"\s+", "", text)


macro_match = re.search(
    r"rule\s+solutionProgram\s*=>\s*(Module\s*\(.*\))\s*endmodule",
    verification,
    re.DOTALL,
)
if macro_match is None:
    raise SystemExit("solutionProgram macro RHS not found")

macro_rhs = macro_match.group(1)
normalized_submitted = strip_comments_and_space(submitted)
normalized_macro = strip_comments_and_space(macro_rhs)

checks = {
    "trusted_regeneration_byte_identity": submitted.encode() == regenerated.encode(),
    "macro_rhs_constructor_identity": normalized_submitted == normalized_macro,
    "claim_loads_solutionProgram": "#loadAll(solutionProgram)" in spec,
    "claim_calls_submitted_binding": (
        'Call(Name("truncate_number"), (Float(N:Float), .Exprs))' in spec
    ),
    "claim_constrains_return": "=> floatMod(N, 1.0) </k>" in spec,
    "destination_closure_body_matches": (
        'Return(BinOp("%", Name("number"), Float(1.0))) .Stmts' in spec
    ),
}

for name, passed in checks.items():
    print(f"{name}={passed}")
print(f"submitted_normalized={normalized_submitted}")
print(f"macro_rhs_normalized={normalized_macro}")

if not all(checks.values()):
    raise SystemExit(1)
