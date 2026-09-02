#!/usr/bin/env python3
"""Independent differential audit for HumanEval problem 159."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load_eat(module_name: str, source: Path):
    spec = importlib.util.spec_from_file_location(module_name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.eat


canonical_eat = load_eat("trusted_canonical_159", Path("/reference/canonical.py"))
candidate_eat = load_eat("candidate_solution_159", Path("/candidate/solution.py"))

documented = [
    ((5, 6, 10), [11, 4]),
    ((4, 8, 9), [12, 1]),
    ((1, 10, 10), [11, 0]),
    ((2, 11, 5), [7, 0]),
]

inputs: set[tuple[int, int, int]] = {case for case, _ in documented}

# Empty, extrema, and mixed extrema.
inputs.update(
    {
        (0, 0, 0),
        (1000, 0, 0),
        (0, 1000, 0),
        (0, 0, 1000),
        (1000, 1000, 1000),
        (1000, 1000, 0),
        (1000, 0, 1000),
        (0, 1, 1000),
        (0, 1000, 1),
    }
)

# Both sides of the only branch and the equality boundary, at domain edges.
for number in (0, 1, 999, 1000):
    for remaining in (0, 1, 2, 500, 999, 1000):
        for need in (remaining - 1, remaining, remaining + 1):
            if 0 <= need <= 1000:
                inputs.add((number, need, remaining))

# Exhaustive small cube.
for number in range(21):
    for need in range(21):
        for remaining in range(21):
            inputs.add((number, need, remaining))

# Deterministic broad sample over the complete documented integer cube.
rng = random.Random(159)
for _ in range(20_000):
    inputs.add(
        (
            rng.randrange(1001),
            rng.randrange(1001),
            rng.randrange(1001),
        )
    )

mismatches: list[tuple[tuple[int, int, int], object, object, object]] = []
for case in sorted(inputs):
    canonical_result = canonical_eat(*case)
    candidate_result = candidate_eat(*case)
    consumed = min(case[1], case[2])
    independent_formula = [case[0] + consumed, case[2] - consumed]
    if canonical_result != candidate_result or candidate_result != independent_formula:
        mismatches.append(
            (case, canonical_result, candidate_result, independent_formula)
        )

for case, expected in documented:
    actual = candidate_eat(*case)
    if actual != expected:
        mismatches.append((case, canonical_eat(*case), actual, expected))

print("DOMAIN: integer triples 0..1000 inclusive")
print("DOCUMENTED_EXAMPLES: 4")
print("BOUNDARY_STRATEGY: empty/extrema plus need=remaining-1,remaining,remaining+1")
print("EXHAUSTIVE_SUBCUBE: 0..20 inclusive on all three arguments")
print("PRNG_SEED: 159")
print("PRNG_DRAWS: 20000")
print(f"UNIQUE_CASES: {len(inputs)}")
print(f"MISMATCHES: {len(mismatches)}")
if mismatches:
    for mismatch in mismatches[:20]:
        print("MISMATCH:", mismatch)
    raise SystemExit(1)
