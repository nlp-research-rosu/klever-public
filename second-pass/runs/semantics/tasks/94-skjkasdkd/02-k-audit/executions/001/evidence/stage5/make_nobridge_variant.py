#!/usr/bin/env python3
"""Remove the bounded #applyK bridge and retarget the spec to the variant."""

from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")
verification = (ROOT / "verification.k").read_text(encoding="utf-8")
specification = (ROOT / "spec.k").read_text(encoding="utf-8")

start_marker = (
    "  // Bounded entry-prefix summary.  It is the direct composition of MPY-CALL's\n"
)
end_marker = '  syntax Module ::= "solutionModule" [macro]\n'
start = verification.index(start_marker)
end = verification.index(end_marker)

variant = verification[:start] + verification[end:]
variant = variant.replace(
    "module VERIFICATION\n", "module VERIFICATION-NOBRIDGE\n", 1
)
(ROOT / "verification-nobridge.k").write_text(variant, encoding="utf-8")

variant_spec = specification.replace(
    'requires "verification.k"', 'requires "verification-nobridge.k"', 1
)
variant_spec = variant_spec.replace("module SPEC\n", "module SPEC-NOBRIDGE\n", 1)
variant_spec = variant_spec.replace(
    "imports VERIFICATION\n", "imports VERIFICATION-NOBRIDGE\n", 1
)
(ROOT / "spec-nobridge.k").write_text(variant_spec, encoding="utf-8")

print(ROOT / "verification-nobridge.k")
print(ROOT / "spec-nobridge.k")
