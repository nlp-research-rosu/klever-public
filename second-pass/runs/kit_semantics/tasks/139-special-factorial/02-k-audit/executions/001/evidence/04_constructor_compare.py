#!/usr/bin/env python3
"""Mechanical constructor-level pinning check for the entry claim."""

import pathlib
import re
import sys


def squash(text: str) -> str:
    return re.sub(r"\s+", "", text)


mpy = squash(pathlib.Path("/tmp/audit-work/reconstruction/solution.mpy").read_text())
spec = squash(pathlib.Path("/tmp/audit-work/reconstruction/spec.k").read_text())

loaded_program = "#loadAll(" + mpy + ")"
call = 'Call(Name("special_factorial"),(N:Int,.Exprs))'
checks = {
    "exact_translated_module_loaded": loaded_program in spec,
    "exact_entry_binding_called": call in spec,
    "positive_unbounded_int_precondition": "requiresN>=Int1" in spec,
    "result_constrained_by_recurrence": "=>productAfter(1,N,1,1)" in spec,
}

print(f"normalized_solution_mpy={mpy}")
print(f"exact_loaded_program_occurrences={spec.count(loaded_program)}")
for name, result in checks.items():
    print(f"{name}={result}")

sys.exit(0 if all(checks.values()) and spec.count(loaded_program) == 1 else 1)
