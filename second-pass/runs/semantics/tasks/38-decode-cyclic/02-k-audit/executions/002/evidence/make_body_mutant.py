#!/usr/bin/env python3
"""Create a body-sensitivity mutant that changes the executed decode term."""

from pathlib import Path


scratch = Path("/tmp/audit-work/38-decode-cyclic")
verification = (scratch / "verification.k").read_text(encoding="utf-8")
old = 'Subscript(Name("s"), Int(2))'
new = 'Subscript(Name("s"), Int(1))'
if verification.count(old) != 1:
    raise RuntimeError(f"expected exactly one body mutation site, got {verification.count(old)}")
verification = verification.replace(
    "module VERIFICATION\n", "module VERIFICATION-BODY-MUTANT\n", 1
).replace(old, new, 1)
(scratch / "verification-body-mutant.k").write_text(verification, encoding="utf-8")

spec = (scratch / "spec.k").read_text(encoding="utf-8")
spec = (
    spec.replace(
        'requires "verification.k"',
        'requires "verification-body-mutant.k"',
        1,
    )
    .replace("module SPEC\n", "module SPEC-BODY-MUTANT\n", 1)
    .replace("imports VERIFICATION\n", "imports VERIFICATION-BODY-MUTANT\n", 1)
)
(scratch / "spec-body-mutant.k").write_text(spec, encoding="utf-8")
print(f"mutation={old} -> {new}")
print('false_witness="bca": submitted result "abc", mutant result "cbc"')
