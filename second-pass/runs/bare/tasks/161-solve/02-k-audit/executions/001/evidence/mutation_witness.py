#!/usr/bin/env python3
"""Ground witness for the deliberately false always-reverse mutation."""

from __future__ import annotations

import importlib.util


spec = importlib.util.spec_from_file_location(
    "generated_solution_mutation", "/tmp/audit-work/candidate-src/solution.py"
)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot import generated solution")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

value = "ab"
actual = module.solve(value)
mutated_postcondition = value[::-1]
print(f"input={value!r}")
print(f"satisfying_PString=97 :: 98 :: .PString")
print(f"submitted_program_result={actual!r}")
print(f"mutated_required_result={mutated_postcondition!r}")
print(f"mutation_is_false={actual != mutated_postcondition}")
raise SystemExit(0 if actual != mutated_postcondition else 1)
