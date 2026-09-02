#!/usr/bin/env python3
"""Independent CPython differential test for HumanEval/36."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from random import Random


def load_entry(module_name: str, path: Path):
    spec = spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.fizz_buzz


canonical = load_entry("trusted_canonical", Path("/reference/canonical.py"))
generated = load_entry(
    "scratch_generated", Path("/tmp/audit-work/36-fizz-buzz/solution.py")
)

# Documented examples and the empty/nonpositive boundary.
documented = [50, 78, 79]
empty_and_boundaries = [-10_000, -1, 0, 1, 2]

# Values immediately before/at/after loop inclusion boundaries for multiples
# of 11, 13, and their LCM, plus the first qualifying values containing 7.
branch_seeds = [11, 13, 22, 26, 77, 117, 143, 176, 177, 187, 273, 377, 770, 777]
branch_boundaries = sorted(
    {
        value + delta
        for value in branch_seeds
        for delta in (-2, -1, 0, 1, 2)
        if value + delta >= 0
    }
)

# Broad deterministic coverage plus reproducible generated representatives.
rng = Random(20260729)
generated_inputs = [rng.randint(-2_000, 20_000) for _ in range(2_000)]
representative = list(range(-100, 2_001)) + [
    5_000,
    10_000,
    20_000,
    50_000,
    100_000,
]

inputs = sorted(
    set(documented + empty_and_boundaries + branch_boundaries + representative + generated_inputs)
)
mismatches = []
for value in inputs:
    expected = canonical(value)
    actual = generated(value)
    if type(actual) is not type(expected) or actual != expected:
        mismatches.append((value, expected, actual, type(expected).__name__, type(actual).__name__))

print(f"documented={documented}")
print(f"empty_and_boundaries={empty_and_boundaries}")
print(f"branch_boundaries={branch_boundaries}")
print("random_seed=20260729 random_draws=2000 range=[-2000,20000]")
print(f"total_unique_inputs={len(inputs)} mismatches={len(mismatches)}")
print(f"sample_results={[(n, generated(n)) for n in [-1, 0, 1, 50, 77, 78, 79, 117, 118, 143, 144, 777]]}")
if mismatches:
    print(f"first_mismatches={mismatches[:20]}")
    raise SystemExit(1)
