#!/usr/bin/env python3
"""Independent differential test for HumanEval 92 any_int.

The oracle is /reference/canonical.py.  The generated entry point is imported
from the clean scratch copy of candidate solution.py.  Test inputs are defined
here and also emitted as JSON for an exact, preserved corpus.
"""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load_module("trusted_canonical", Path("/reference/canonical.py"))
generated = load_module(
    "scratch_generated", Path("/tmp/audit-work/candidate-src/solution.py")
)

# Stated examples plus explicit witnesses for each equality, each failed type
# check, zero/negative/large integer behavior, and Python's bool-is-int edge.
named_cases = [
    ("example_x_plus_y", (5, 2, 7)),
    ("example_false", (3, 2, 2)),
    ("example_negative", (3, -2, 1)),
    ("example_non_integer", (3.6, -2.2, 2)),
    ("x_plus_z_equals_y", (5, 7, 2)),
    ("y_plus_z_equals_x", (7, 5, 2)),
    ("none_equal", (1, 1, 3)),
    ("all_zero", (0, 0, 0)),
    ("negative_true", (-5, 2, -3)),
    ("negative_false", (-5, 2, 3)),
    ("x_non_integer", (1.0, 2, 3)),
    ("y_non_integer", (1, 2.0, 3)),
    ("z_non_integer", (1, 2, 3.0)),
    ("nan", (math.nan, 0, 0)),
    ("positive_infinity", (math.inf, 0, 0)),
    ("bool_is_python_int", (True, 1, 2)),
    ("large_integer", (10**100, -(10**100), 0)),
]

# Exhaustive small cross-product. It covers all sign transitions, every
# equality orientation, all failed-equality regions, and non-integer positions.
grid_values = list(range(-5, 6)) + [-2.5, 0.0, 3.5, False, True]
grid_cases = [
    (f"grid_{index}", (x, y, z))
    for index, (x, y, z) in enumerate(
        (x, y, z)
        for x in grid_values
        for y in grid_values
        for z in grid_values
    )
]

# Deterministic broader integer sample, including arbitrary-precision values.
rng = random.Random(920092)
random_cases = []
for index in range(2000):
    if index < 100:
        x = rng.randrange(-(10**80), 10**80)
        y = rng.randrange(-(10**80), 10**80)
    else:
        x = rng.randrange(-10**9, 10**9)
        y = rng.randrange(-10**9, 10**9)
    selector = index % 5
    if selector == 0:
        triple = (x, y, x + y)
    elif selector == 1:
        triple = (x, x + y, y)
    elif selector == 2:
        triple = (x + y, x, y)
    elif selector == 3:
        triple = (x, y, x + y + 1)
    else:
        triple = (x, y, rng.randrange(-10**9, 10**9))
    random_cases.append((f"random_{index}", triple))

all_cases = named_cases + grid_cases + random_cases
corpus_path = Path("/audit-output/evidence/differential_inputs.json")
corpus_path.write_text(
    json.dumps(
        [{"label": label, "args": args} for label, args in all_cases],
        allow_nan=True,
        indent=2,
    )
    + "\n",
    encoding="utf-8",
)

mismatches = []
for label, args in all_cases:
    try:
        expected = ("return", canonical.any_int(*args))
    except BaseException as err:  # record behavior, including exceptional behavior
        expected = ("raise", type(err).__name__, str(err))
    try:
        actual = ("return", generated.any_int(*args))
    except BaseException as err:
        actual = ("raise", type(err).__name__, str(err))
    if expected != actual:
        mismatches.append(
            {"label": label, "args": args, "canonical": expected, "generated": actual}
        )

print(f"named_cases={len(named_cases)}")
print(f"grid_values={grid_values!r}")
print(f"grid_cases={len(grid_cases)}")
print("random_seed=920092")
print(f"random_cases={len(random_cases)}")
print(f"total_cases={len(all_cases)}")
print(f"corpus={corpus_path}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches[:20]:
    print(json.dumps(mismatch, allow_nan=True, sort_keys=True))

sys.exit(1 if mismatches else 0)
