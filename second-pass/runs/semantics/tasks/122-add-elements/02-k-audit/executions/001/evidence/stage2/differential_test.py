#!/usr/bin/env python3
"""Differential audit of the trusted canonical and submitted Python entry points."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[int], int], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.add_elements


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(Path("/tmp/audit-work/src/solution.py"), "submitted_solution")

cases: list[tuple[str, list[int], int]] = [
    ("documented-example", [111, 21, 3, 4000, 5, 6, 7, 8, 9], 4),
    ("outside-domain-empty", [], 0),
    ("k-lower-bound", [99, 100], 1),
    ("k-upper-bound", [99, 100], 2),
    ("length-upper-k-lower", list(range(100)), 1),
    ("length-upper-k-upper", list(range(100)), 100),
    (
        "all-branch-boundaries",
        [-101, -100, -99, -10, -9, -1, 0, 1, 9, 10, 99, 100, 101],
        13,
    ),
    ("suffix-excluded", [-99, 10, 20], 1),
    ("singleton-zero", [0], 1),
]

# Exhaustive singleton sweep around both string-length and abs-value boundaries.
for value in range(-150, 151):
    cases.append((f"singleton-{value}", [value], 1))

# Deterministic representative generation over the documented domain:
# integer arrays, 1 <= length <= 100, 1 <= k <= length.
rng = random.Random(122)
interesting_values = [
    -10000,
    -101,
    -100,
    -99,
    -10,
    -9,
    -1,
    0,
    1,
    9,
    10,
    99,
    100,
    101,
    10000,
]
for index in range(200):
    length = rng.randint(1, 100)
    arr = [
        rng.choice(interesting_values)
        if rng.random() < 0.7
        else rng.randint(-10000, 10000)
        for _ in range(length)
    ]
    k = rng.choice([1, length, rng.randint(1, length)])
    cases.append((f"generated-{index}", arr, k))

print("ORACLES:")
print("  trusted=/reference/canonical.py:add_elements")
print("  submitted=/tmp/audit-work/src/solution.py:add_elements")
print("INPUT_SCOPE:")
print("  documented example; empty outside-domain case; k and len boundaries;")
print("  all decision boundaries; every singleton integer -150..150;")
print("  200 deterministic generated in-domain arrays (seed=122).")
print(f"CASE_COUNT: {len(cases)}")

mismatches: list[dict[str, object]] = []
errors: list[dict[str, object]] = []
for label, arr, k in cases:
    try:
        expected = canonical(arr, k)
        actual = generated(arr, k)
    except Exception as error:  # Preserve unexpected execution failures as evidence.
        errors.append(
            {
                "label": label,
                "arr": arr,
                "k": k,
                "error": f"{type(error).__name__}: {error}",
            }
        )
        continue
    if expected != actual:
        mismatches.append(
            {
                "label": label,
                "arr": arr,
                "k": k,
                "canonical": expected,
                "submitted": actual,
            }
        )

print(f"ERROR_COUNT: {len(errors)}")
print(f"MISMATCH_COUNT: {len(mismatches)}")
print("ERRORS_JSON:")
print(json.dumps(errors, sort_keys=True))
print("MISMATCHES_JSON:")
print(json.dumps(mismatches, sort_keys=True))

# The differential command should fail on any semantic divergence.
raise SystemExit(1 if errors or mismatches else 0)
