#!/usr/bin/env python3
"""Create the fresh false-postcondition mutation used for stage 6."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/43-pairs-sum-to-zero")
source = (ROOT / "candidate/spec.k").read_text()
source = source.replace(
    'requires "verification.k"',
    'requires "candidate/verification.k"',
    1,
)
source = source.replace("module SPEC", "module SPEC-VACUITY", 1)
needle = "pyBool(hasZeroPair(L))"
assert source.count(needle) == 1
source = source.replace(needle, "pyBool(notBool hasZeroPair(L))", 1)

scratch_path = ROOT / "06-spec-vacuity.k"
evidence_path = Path("/audit-output/evidence/06-spec-vacuity.k")
scratch_path.write_text(source)
evidence_path.write_text(source)
print(f"wrote {scratch_path}")
print(f"wrote {evidence_path}")
print(
    "witness: L=.ISeq satisfies the original precondition; the actual program "
    "returns false, hasZeroPair(.ISeq)=false, and the mutated RHS demands true"
)
