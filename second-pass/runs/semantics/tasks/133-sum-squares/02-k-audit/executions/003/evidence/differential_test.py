#!/usr/bin/env python3
"""Independent differential test for HumanEval 133."""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path


def load(path: str, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("/reference/canonical.py", "trusted_canonical_133")
generated = load("/tmp/audit-work/candidate/solution.py", "generated_solution_133")

documented = [
    ([1, 2, 3], 14),
    ([1, 4, 9], 98),
    ([1, 3, 5, 7], 84),
    ([1.4, 4.2, 0], 29),
    ([-2.4, 1, 1], 6),
]

boundaries = [
    [],
    [0],
    [-0.0],
    [0.000000001],
    [-0.000000001],
    [0.999999999],
    [1.0],
    [1.000000001],
    [-0.999999999],
    [-1.0],
    [-1.000000001],
    [-1.999999999],
    [-2.0],
    [-2.000000001],
    [10**30],
    [-(10**30)],
    [-2.4, 0, 1.4, 4.2],
    list(range(-25, 26)),
]

rng = random.Random(133_2026)
generated_inputs: list[list[int | float]] = []
for _ in range(1000):
    values: list[int | float] = []
    for _ in range(rng.randrange(0, 25)):
        if rng.randrange(3) == 0:
            values.append(rng.randrange(-10_000, 10_001))
        else:
            numerator = rng.randrange(-1_000_000, 1_000_001)
            denominator = rng.choice((10, 100, 1000, 10_000))
            values.append(numerator / denominator)
    generated_inputs.append(values)

cases = [case for case, _ in documented] + boundaries + generated_inputs
mismatches: list[tuple[list[int | float], object, object]] = []

for case, expected in documented:
    can = canonical.sum_squares(list(case))
    got = generated.sum_squares(list(case))
    if can != expected or got != expected:
        mismatches.append((case, can, got))

for case in boundaries + generated_inputs:
    try:
        can: object = canonical.sum_squares(list(case))
    except Exception as err:  # compare exception types as observable behavior
        can = ("EXCEPTION", type(err).__name__, str(err))
    try:
        got: object = generated.sum_squares(list(case))
    except Exception as err:
        got = ("EXCEPTION", type(err).__name__, str(err))
    if can != got:
        mismatches.append((case, can, got))

print("oracle=/reference/canonical.py:sum_squares")
print("candidate=/tmp/audit-work/candidate/solution.py:sum_squares")
print(f"documented_examples={len(documented)}")
print(f"hand_boundary_cases={len(boundaries)}")
print(f"seed=1332026 generated_cases={len(generated_inputs)}")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(f"MISMATCH {mismatch!r}")

for witness in ([], [1.4, 4.2, 0], [-2.4, 1, 1], [2.0001, -2.0001]):
    print(
        "WITNESS "
        f"input={witness!r} "
        f"canonical={canonical.sum_squares(list(witness))!r} "
        f"candidate={generated.sum_squares(list(witness))!r}"
    )

if mismatches:
    raise SystemExit(1)
