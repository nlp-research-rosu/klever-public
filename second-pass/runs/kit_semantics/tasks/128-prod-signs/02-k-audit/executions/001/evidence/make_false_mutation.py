#!/usr/bin/env python3
"""Create a fresh auditor mutation: force every entry result to integer zero."""

from pathlib import Path


source = Path("/tmp/audit-work/128-prod-signs/spec.k").read_text()
mutated = source.replace("module SPEC\n", "module AUDITOR-FALSE-SPEC\n", 1)
needle = "=> prodSignsResult(INPUT)"
assert mutated.count(needle) == 1
mutated = mutated.replace(
    needle,
    "=> 0",
    1,
)

scratch = Path("/tmp/audit-work/128-prod-signs/auditor-false-spec.k")
evidence = Path("/audit-output/evidence/auditor-false-spec.k")
scratch.write_text(mutated)
evidence.write_text(mutated)

print(f"SCRATCH_MUTATION={scratch}")
print(f"PRESERVED_MUTATION={evidence}")
print("MUTATION=entry_postcondition_prodSignsResult_INPUT_to_zero")
print("SATISFYING_FALSE_WITNESS=[] EXPECTED=noneV MUTATED=0")
print("SATISFYING_FALSE_WITNESS=[1,2,2,-4] EXPECTED=-9 MUTATED=0")
