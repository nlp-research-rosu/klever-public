#!/usr/bin/env python3
"""Create a K-level body mutation that the candidate bridge can preempt."""

from pathlib import Path


root = Path("/tmp/audit-work/39-prime-fib/src")
source = (root / "verification.k").read_text()

mutated = source
mutated = mutated.replace(
    "module PRIME-FIB-PROGRAM",
    "module AUDIT-BODY-MUT-PROGRAM",
    1,
)
mutated = mutated.replace(
    "module VERIFICATION",
    "module AUDIT-BODY-MUT-VERIFICATION",
    1,
)
mutated = mutated.replace(
    "imports PRIME-FIB-PROGRAM",
    "imports AUDIT-BODY-MUT-PROGRAM",
    1,
)

needle = '        Return(Name("b"))))'
replacement = '        Return(Name("a"))))'
if mutated.count(needle) != 1:
    raise AssertionError(f"expected one return-body target, got {mutated.count(needle)}")
mutated = mutated.replace(needle, replacement, 1)

destination = root / "audit-body-mut-verification.k"
destination.write_text(mutated)
print(f"WROTE {destination}")
print('BODY_MUTATION Return(Name("b")) -> Return(Name("a"))')
print("PROGRAM_TERM_CHANGED true")
