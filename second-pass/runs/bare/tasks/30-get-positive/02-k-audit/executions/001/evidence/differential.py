#!/usr/bin/env python3
"""Independent canonical-vs-candidate differential test for get_positive."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path) -> Callable[[list], list]:
    spec = importlib.util.spec_from_file_location(f"mod_{path.stem}_{id(path)}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_positive


canonical = load_function(Path("/reference/canonical.py"))
generated = load_function(Path("/tmp/audit-work/30-get-positive/solution.py"))

documented_and_boundaries: list[tuple[str, list[Any]]] = [
    ("prompt-example-1", [-1, 2, -4, 5, 6]),
    ("prompt-example-2", [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10]),
    ("empty", []),
    ("zero-only", [0]),
    ("negative-only", [-1, -2, -10**100]),
    ("positive-only", [1, 2, 10**100]),
    ("three-way-branch-boundary", [-1, 0, 1]),
    ("duplicates-and-order", [2, -1, 2, 0, 3, 2]),
    ("float-boundaries", [-math.inf, -0.0, 0.0, 1e-300, math.inf]),
    ("bool-numeric-subclass", [False, True, -1, 1]),
]

rng = random.Random(20260723)
generated_cases: list[list[Any]] = []
for _ in range(120):
    length = rng.randint(0, 35)
    values: list[Any] = []
    for _ in range(length):
        if rng.randrange(5) == 0:
            values.append(rng.choice([-1.5, -0.0, 0.0, 0.25, 2.5]))
        else:
            values.append(rng.randint(-1000, 1000))
    generated_cases.append(values)

all_cases = documented_and_boundaries + [
    (f"generated-{index:03d}", values)
    for index, values in enumerate(generated_cases)
]

mismatches = []
serialized_inputs = []
for label, values in all_cases:
    expected = canonical(list(values))
    actual = generated(list(values))
    serialized_inputs.append((label, repr(values)))
    if expected != actual:
        mismatches.append((label, values, expected, actual))
    if label in {name for name, _ in documented_and_boundaries}:
        print(
            f"CASE {label} input={values!r} canonical={expected!r} "
            f"candidate={actual!r} match={expected == actual}"
        )

scope_blob = json.dumps(serialized_inputs, separators=(",", ":")).encode()
print(
    "SUMMARY "
    f"cases={len(all_cases)} documented_boundary={len(documented_and_boundaries)} "
    f"generated={len(generated_cases)} mismatches={len(mismatches)} "
    f"input_scope_sha256={hashlib.sha256(scope_blob).hexdigest()} "
    "generator_seed=20260723 generated_lengths=0..35 "
    "generated_values=int[-1000,1000] plus {-1.5,-0.0,0.0,0.25,2.5}"
)
for mismatch in mismatches:
    print(f"MISMATCH {mismatch!r}")
raise SystemExit(1 if mismatches else 0)
