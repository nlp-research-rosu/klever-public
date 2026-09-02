#!/usr/bin/env python3
import importlib.util
import itertools
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def load_function(module_name: str, path: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_function("trusted_canonical", "/reference/canonical.py")
generated = load_function("generated_solution", "/candidate/solution.py")

documented = [
    [1, 2, 3],
    [],
    [-1, -5, 2, -1, -5],
]

# Prefix lengths 0..14 place a final element at every relevant index around
# 0, 3, 4, 6, 8, 9, and 12, including the 12-divisible precedence case.
branch_boundaries = [
    [(-1 if index % 2 else index) for index in range(length)]
    for length in range(15)
]

# Exhaust all small lists through length 6.
exhaustive = [
    list(values)
    for length in range(7)
    for values in itertools.product([-5, -1, 0, 1, 2], repeat=length)
]

rng = random.Random(142)
generated_cases = [
    [rng.randint(-1000, 1000) for _ in range(rng.randint(0, 40))]
    for _ in range(500)
]
generated_cases.extend([
    [10**40, -(10**40), 0, 2, -3, 7, -11, 13, -17, 19, -23, 29, -31],
    [1] * 100,
])

normal_cases = documented + branch_boundaries + exhaustive + generated_cases
mismatches = []
for ordinal, case in enumerate(normal_cases):
    expected = canonical(case.copy())
    actual = generated(case.copy())
    if actual != expected:
        mismatches.append((ordinal, case, expected, actual))

print(f"documented_cases={len(documented)}")
print(f"branch_boundary_cases={len(branch_boundaries)}")
print(f"exhaustive_small_cases={len(exhaustive)}")
print(f"representative_generated_cases={len(generated_cases)}")
print(f"normal_total={len(normal_cases)}")
print(f"normal_mismatches={len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:10]:
        print(f"NORMAL_MISMATCH={mismatch!r}")

# Probe the actual CPython recursion boundary separately because the candidate
# is recursive whereas the trusted canonical implementation is iterative.
resource_case = list(range(1500))
resource_expected = canonical(resource_case.copy())
try:
    resource_actual = generated(resource_case.copy())
    resource_outcome = f"value={resource_actual}"
    resource_match = resource_actual == resource_expected
except Exception as error:
    resource_outcome = f"{type(error).__name__}: {error}"
    resource_match = False

print("resource_case_length=1500")
print(f"resource_canonical=value={resource_expected}")
print(f"resource_generated={resource_outcome}")
print(f"resource_match={resource_match}")

if mismatches:
    raise SystemExit(1)
