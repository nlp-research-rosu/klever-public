#!/usr/bin/env python3
"""Independent differential checks for HumanEval/83 on its positive-int domain."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.starts_one_ends


def brute_count(n: int) -> int:
    lower = 1 if n == 1 else 10 ** (n - 1)
    upper = 10**n
    return sum(
        1
        for value in range(lower, upper)
        if str(value).startswith("1") or str(value).endswith("1")
    )


trusted = load_entry(
    Path("/tmp/audit-work/83-review/trusted/canonical.py"),
    "trusted_canonical_83",
)
generated = load_entry(
    Path("/tmp/audit-work/83-review/candidate/solution.py"),
    "generated_solution_83",
)

# There are no examples in prompt.py.  The input is a scalar positive integer,
# so an "empty" value is not in the documented domain.  The list covers the
# minimum, both sides of the only branch boundary, small values, and a
# deterministic broader sample.
rng = random.Random(830083)
inputs = sorted(
    set([1, 2, 3, 4, 5, 9, 10, 20, 50, 100] + [rng.randint(1, 120) for _ in range(40)])
)

differential_mismatches: list[tuple[int, object, object]] = []
for n in inputs:
    expected = trusted(n)
    observed = generated(n)
    if observed != expected or type(observed) is not type(expected):
        differential_mismatches.append((n, expected, observed))

brute_inputs = [1, 2, 3, 4]
brute_mismatches: list[tuple[int, int, object, object]] = []
for n in brute_inputs:
    counted = brute_count(n)
    canonical_result = trusted(n)
    generated_result = generated(n)
    if counted != canonical_result or counted != generated_result:
        brute_mismatches.append(
            (n, counted, canonical_result, generated_result)
        )

print("DOCUMENTED_EXAMPLES: none")
print("EMPTY_CASE: not applicable; contract input is a positive integer")
print(f"DIFFERENTIAL_INPUTS ({len(inputs)}): {inputs}")
print(f"BRUTE_FORCE_INPUTS: {brute_inputs}")
print(
    "BOUNDARY_RESULTS: "
    + ", ".join(
        f"n={n}:canonical={trusted(n)},generated={generated(n)}"
        for n in [1, 2, 3, 10]
    )
)
print(f"DIFFERENTIAL_MISMATCHES: {len(differential_mismatches)}")
for mismatch in differential_mismatches:
    print(f"DIFFERENTIAL_MISMATCH: {mismatch}")
print(f"BRUTE_FORCE_MISMATCHES: {len(brute_mismatches)}")
for mismatch in brute_mismatches:
    print(f"BRUTE_FORCE_MISMATCH: {mismatch}")

if differential_mismatches or brute_mismatches:
    raise SystemExit(1)
