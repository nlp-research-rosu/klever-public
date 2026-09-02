#!/usr/bin/env python3
"""Independent differential test for HumanEval/8 sum_product."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_product


canonical = load_entry(
    Path("/tmp/audit-work/8-sum-product-audit-002/trusted/canonical.py"),
    "trusted_canonical",
)
candidate = load_entry(
    Path("/tmp/audit-work/8-sum-product-audit-002/work/solution.py"),
    "candidate_solution",
)

explicit_cases = [
    [],                         # empty-loop boundary and documented example
    [1, 2, 3, 4],               # documented example
    [0],                        # first/only iteration and zero product
    [1],
    [-1],
    [2],
    [-2],
    [0, 5],                     # first zero
    [5, 0],                     # later zero
    [-3, 4],                    # mixed signs
    [-3, -4],                   # even negative count
    [-(10**100), 10**100],      # arbitrary-precision integer boundary
    [10**200, 0, -(10**200)],
]

# Exhaust all lists of length 0..5 over a small signed alphabet. This covers
# zero versus nonzero loop execution, one versus many iterations, zero product,
# and odd/even negative counts at each feasible position.
exhaustive_cases = [
    list(values)
    for length in range(6)
    for values in itertools.product(range(-3, 4), repeat=length)
]

# Deterministic broader sample with large signed integers and longer lists.
rng = random.Random(0x8A11D17)
generated_cases = [
    [rng.randint(-(10**40), 10**40) for _ in range(rng.randint(0, 50))]
    for _ in range(2_000)
]

cases = explicit_cases + exhaustive_cases + generated_cases
mismatches = []
for index, values in enumerate(cases):
    expected = canonical(values)
    actual = candidate(values)
    if actual != expected:
        mismatches.append((index, values, expected, actual))
        if len(mismatches) >= 10:
            break

print(f"explicit_cases={len(explicit_cases)}")
print(f"exhaustive_cases={len(exhaustive_cases)}")
print(f"generated_cases={len(generated_cases)} seed=0x8A11D17")
print(f"total_cases={len(cases)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(repr(mismatch))

raise SystemExit(1 if mismatches else 0)
