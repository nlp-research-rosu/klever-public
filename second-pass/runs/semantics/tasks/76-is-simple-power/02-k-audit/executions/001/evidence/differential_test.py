#!/usr/bin/env python3
"""Independent differential test for HumanEval 76.

The trusted canonical implementation is the oracle.  The tested implementation
is imported from the scratch copy of candidate solution.py.  The exhaustive
grid stays inside the canonical implementation's terminating integer domain:
n >= 1.  Additional n <= 0 cases are included only where x <= 1, for which the
canonical loop is not entered.
"""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/76-is-simple-power")


def load_function(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.is_simple_power


canonical = load_function("trusted_canonical", SCRATCH / "trusted/canonical.py")
generated = load_function(
    "generated_solution", SCRATCH / "candidate-source/solution.py"
)

documented = [(1, 4), (2, 2), (8, 2), (3, 2), (3, 1), (5, 3)]
branch_boundaries = [
    (-1, 1),
    (0, 1),
    (1, 1),
    (2, 1),
    (-1, 2),
    (0, 2),
    (1, 2),
    (2, 2),
    (3, 2),
    (4, 2),
    (8, 2),
    (9, 3),
    (10, 3),
    (16, 4),
    (64, 2),
]
terminating_nonpositive_bases = [
    (x, n) for x in range(-5, 2) for n in range(-5, 1)
]
exhaustive_grid = [(x, n) for x in range(-25, 1001) for n in range(1, 21)]

rng = random.Random(760076)
generated_sample = [
    (rng.randint(-100, 1_000_000), rng.randint(1, 100)) for _ in range(2000)
]
power_cases = []
for n in range(2, 31):
    value = 1
    for _exponent in range(9):
        power_cases.extend([(value, n), (value - 1, n), (value + 1, n)])
        value *= n

cases = []
seen = set()
for group in (
    documented,
    branch_boundaries,
    terminating_nonpositive_bases,
    exhaustive_grid,
    generated_sample,
    power_cases,
):
    for case in group:
        if case not in seen:
            seen.add(case)
            cases.append(case)

mismatches = []
for x, n in cases:
    expected = canonical(x, n)
    actual = generated(x, n)
    if actual != expected:
        mismatches.append((x, n, expected, actual))

print("oracle=/tmp/audit-work/76-is-simple-power/trusted/canonical.py")
print("subject=/tmp/audit-work/76-is-simple-power/candidate-source/solution.py")
print(f"documented_examples={documented}")
print(f"documented_results={[generated(x, n) for x, n in documented]}")
print(f"branch_boundary_cases={branch_boundaries}")
print(
    "scope=all x in [-25,1000] with n in [1,20], "
    "2000 deterministic generated cases with n>=1, powers and neighbors, "
    "plus terminating x<=1/n<=0 cases"
)
print(f"unique_case_count={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
    raise SystemExit(1)
