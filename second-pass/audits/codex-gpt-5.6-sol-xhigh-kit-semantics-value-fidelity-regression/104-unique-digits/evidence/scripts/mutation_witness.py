#!/usr/bin/env python3
"""Show that the fresh K mutation's ground result is actually false."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


values = [15, 33, 1422, 1]
mutated_result = [1, 15]
canonical_result = load(
    Path("/reference/canonical.py"), "trusted_canonical_mutation"
).unique_digits(list(values))
candidate_result = load(
    Path("/tmp/audit-work/104-unique-digits/solution.py"),
    "candidate_solution_mutation",
).unique_digits(list(values))

print(f"input={values}")
print("formal_precondition=list of positive integers: true")
print(f"mutated_result={mutated_result}")
print(f"canonical_result={canonical_result}")
print(f"candidate_result={candidate_result}")
print(f"mutation_is_false={mutated_result != canonical_result == candidate_result}")

raise SystemExit(
    0 if mutated_result != canonical_result == candidate_result else 1
)
