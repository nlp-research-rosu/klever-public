"""Independent differential test for HumanEval/63-fibfib.

The oracle is imported directly from the trusted canonical.py mount copy.  The
candidate implementation is imported from the isolated scratch copy.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


WORK = Path("/tmp/audit-work")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fibfib


canonical = load_function("trusted_canonical", WORK / "canonical.py")
generated = load_function("candidate_solution", WORK / "solution.py")

# n=0 is the empty/initial sequence boundary.  0, 1, 2 exercise each base
# branch; 3 is the first recursive/loop-recurrence boundary.  The documented
# examples are 1, 5, and 8.
fixed_inputs = [0, 1, 2, 3, 4, 5, 8, 10, 12, 15, 18, 20]
rng = random.Random(630063)
generated_inputs = [rng.randint(0, 20) for _ in range(16)]
inputs = fixed_inputs + generated_inputs

rows = []
mismatches = []
for n in inputs:
    expected = canonical(n)
    actual = generated(n)
    row = (n, expected, actual)
    rows.append(row)
    if expected != actual:
        mismatches.append(row)

print("contract_domain: nonnegative integers")
print(f"fixed_inputs: {fixed_inputs}")
print(f"seed: 630063")
print(f"generated_inputs: {generated_inputs}")
print("rows:")
for n, expected, actual in rows:
    print(f"  n={n:2d} canonical={expected} generated={actual}")
print(f"cases: {len(rows)}")
print(f"mismatches: {len(mismatches)}")
if mismatches:
    print(f"mismatch_rows: {mismatches}")
    raise SystemExit(1)
