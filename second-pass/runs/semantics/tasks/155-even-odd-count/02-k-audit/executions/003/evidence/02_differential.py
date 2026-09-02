#!/usr/bin/env python3
"""Independent differential test for HumanEval 155.

The test does not import candidate proof equations.  It loads the trusted
canonical Python and the submitted generated Python directly from their
mounted source files.
"""

import importlib.util
import random
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.even_odd_count


canonical = load_function("trusted_canonical", Path("/reference/canonical.py"))
generated = load_function("candidate_solution", Path("/candidate/solution.py"))

documented = [-12, 123]
empty_or_boundary = [
    0,
    1,
    -1,
    2,
    -2,
    9,
    -9,
    10,
    -10,
    11,
    -11,
    99,
    -99,
    100,
    -100,
    101,
    -101,
    2**31 - 1,
    -(2**31),
    2**63 - 1,
    -(2**63),
]
branch_boundaries = list(range(-20, 21)) + [
    24680,
    -24680,
    13579,
    -13579,
    102030405,
    -102030405,
]
powers = []
for exponent in range(1, 101):
    power = 10**exponent
    powers.extend([power - 1, power, power + 1, -power + 1, -power, -power - 1])

rng = random.Random(155)
generated_inputs = [rng.randint(-(10**100), 10**100) for _ in range(2000)]
inputs = list(dict.fromkeys(documented + empty_or_boundary + branch_boundaries + powers + generated_inputs))

mismatches = []
for value in inputs:
    trusted_result = canonical(value)
    generated_result = generated(value)
    if trusted_result != generated_result:
        mismatches.append((value, trusted_result, generated_result))

print(f"documented={len(documented)}")
print(f"empty_or_boundary={len(empty_or_boundary)}")
print(f"branch_boundary={len(branch_boundaries)}")
print(f"power_boundaries={len(powers)}")
print(f"seed=155 generated={len(generated_inputs)} range=[-10**100,10**100]")
print(f"unique_total={len(inputs)} mismatches={len(mismatches)}")
if mismatches:
    print(f"first_mismatches={mismatches[:10]}")
    raise SystemExit(1)
