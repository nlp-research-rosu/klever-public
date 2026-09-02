#!/usr/bin/env python3
"""Create an executed-body sensitivity mutant without changing the claims."""

from pathlib import Path


work = Path("/tmp/audit-work/103-rounded-avg")
verification = (work / "verification.k").read_text(encoding="utf-8")
old_increment = 'BinOp("+", Name("average"), Int(1)))'
new_increment = 'BinOp("+", Name("average"), Int(2)))'
if verification.count(old_increment) != 1:
    raise RuntimeError("expected exactly one average increment")
verification = verification.replace(
    "module ROUNDED-AVG-VERIFICATION",
    "module ROUNDED-AVG-VERIFICATION-BODY-MUTANT",
    1,
).replace(old_increment, new_increment, 1)
(work / "verification-body-mutant.k").write_text(verification, encoding="utf-8")

spec = (work / "spec.k").read_text(encoding="utf-8")
spec = spec.replace(
    'requires "verification.k"',
    'requires "verification-body-mutant.k"',
    1,
).replace(
    "module ROUNDED-AVG-SPEC",
    "module ROUNDED-AVG-SPEC-BODY-MUTANT",
    1,
).replace(
    "imports ROUNDED-AVG-VERIFICATION",
    "imports ROUNDED-AVG-VERIFICATION-BODY-MUTANT",
    1,
)
(work / "spec-body-mutant.k").write_text(spec, encoding="utf-8")
print("changed executed body: average + 1 -> average + 2")
print("claims unchanged:", spec.count("claim") == 4)
