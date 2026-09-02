#!/usr/bin/env python3
"""Independent result differential for HumanEval 70.

Oracle: /reference/canonical.py.
Generated entry point: /tmp/audit-work/recon/solution.py.
Each implementation receives its own list copy because the canonical function
destructively removes elements while the generated implementation does not.
"""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.strange_sort_list


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry("generated_solution", Path("/tmp/audit-work/recon/solution.py"))

documented = [
    [],
    [1, 2, 3, 4],
    [5, 5, 5, 5],
]

# Explicitly hits loop false/true, both parity branches, even/odd lengths,
# ordering patterns, duplicates, negatives, and large Python integers.
boundaries = [
    [0],
    [2, 1],
    [2, 1, 3],
    [4, 1, 3, 2],
    [4, 1, 4, 1, 2],
    [-1, -2, -3, -4, -5, -6],
    [3, -1, 3, 2, 0],
    [10**100, 0, -(10**100), 7, 7],
]

rng = random.Random(70070)
random_cases = [
    [rng.randint(-10**6, 10**6) for _ in range(rng.randint(0, 30))]
    for _ in range(2_000)
]

checked = 0
mismatches: list[tuple[list[int], list[int], list[int]]] = []


def check(case: list[int]) -> None:
    global checked
    expected = canonical(list(case))
    actual = generated(list(case))
    checked += 1
    if expected != actual:
        mismatches.append((case, expected, actual))


for case in documented:
    check(case)
for case in boundaries:
    check(case)

# Exhaustive finite sample: every list of lengths 0..6 over {-2,-1,0,1,2}.
for length in range(7):
    for values in itertools.product(range(-2, 3), repeat=length):
        check(list(values))

for case in random_cases:
    check(case)

print("oracle=/reference/canonical.py:strange_sort_list")
print("generated=/tmp/audit-work/recon/solution.py:strange_sort_list")
print("documented_cases=3")
print("explicit_boundary_cases=8")
print("exhaustive_domain=lengths 0..6, values -2..2")
print("exhaustive_cases=19531")
print("deterministic_random_seed=70070")
print("random_cases=2000, lengths 0..30, values -1000000..1000000")
print(f"total_checked={checked}")
print(f"mismatch_count={len(mismatches)}")
for case, expected, actual in mismatches[:20]:
    print(f"MISMATCH input={case!r} canonical={expected!r} generated={actual!r}")

for case in documented + boundaries:
    print(
        f"WITNESS input={case!r} "
        f"canonical={canonical(list(case))!r} generated={generated(list(case))!r}"
    )

raise SystemExit(1 if mismatches else 0)
