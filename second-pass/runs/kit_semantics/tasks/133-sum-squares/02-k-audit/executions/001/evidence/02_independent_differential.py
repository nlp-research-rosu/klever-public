#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval/133."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: str, module_name: str) -> Callable[[list[Any]], int]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.sum_squares


canonical = load_entry("/reference/canonical.py", "trusted_canonical_133")
generated = load_entry(
    "/tmp/audit-work/reconstruction/solution.py", "generated_solution_133"
)

examples: list[tuple[list[int | float], int]] = [
    ([1, 2, 3], 14),
    ([1, 4, 9], 98),
    ([1, 3, 5, 7], 84),
    ([1.4, 4.2, 0], 29),
    ([-2.4, 1, 1], 6),
]
for values, expected in examples:
    assert canonical(values) == expected
    assert generated(values) == expected

cases: list[list[Any]] = [
    [],
    [0],
    [0.0],
    [-0.0],
    [1],
    [-1],
    [10**100, -(10**100)],
    [float.fromhex("0x0.0000000000001p-1022")],
    [-float.fromhex("0x0.0000000000001p-1022")],
    [float.fromhex("0x1.fffffffffffffp+1023")],
    [math.nan],
    [math.inf],
    [-math.inf],
    ["not-a-number"],
]
cases.extend(values for values, _ in examples)

# Each integer ceiling discontinuity gets just-below, exact, and just-above
# singleton witnesses. This covers both sides of the only numeric branch
# boundary used by math.ceil, including negative and zero boundaries.
for integer in [-100, -3, -2, -1, 0, 1, 2, 3, 100]:
    point = float(integer)
    cases.extend(
        [
            [math.nextafter(point, -math.inf)],
            [point],
            [math.nextafter(point, math.inf)],
            [
                math.nextafter(point, -math.inf),
                point,
                math.nextafter(point, math.inf),
            ],
        ]
    )

# Deterministic representative generated lists exercise the empty/non-empty
# loop boundary, many lengths, mixed Int/Float elements, and repeated values.
rng = random.Random(133_2026_07_29)
pool: list[int | float] = list(range(-50, 51))
pool.extend(numerator / 16.0 for numerator in range(-800, 801))
for integer in range(-12, 13):
    point = float(integer)
    pool.append(math.nextafter(point, -math.inf))
    pool.append(math.nextafter(point, math.inf))
for _ in range(3000):
    length = rng.randrange(0, 65)
    cases.append([rng.choice(pool) for _ in range(length)])


def outcome(function: Callable[[list[Any]], int], values: list[Any]) -> tuple:
    try:
        result = function(values)
        return ("return", type(result).__name__, result)
    except Exception as err:  # compare CPython-observable exceptional behavior
        return ("raise", type(err).__name__, str(err))


mismatches: list[dict[str, Any]] = []
returns = 0
raises = 0
for index, values in enumerate(cases):
    trusted = outcome(canonical, values)
    candidate = outcome(generated, values)
    if trusted[0] == "return":
        returns += 1
    else:
        raises += 1
    if trusted != candidate:
        mismatches.append(
            {
                "index": index,
                "input": repr(values),
                "trusted": repr(trusted),
                "candidate": repr(candidate),
            }
        )

input_manifest = "\n".join(repr(values) for values in cases).encode()
print(f"documented_examples={len(examples)} all_expected=true")
print(f"cases={len(cases)} returns={returns} raises={raises}")
print(f"input_manifest_sha256={hashlib.sha256(input_manifest).hexdigest()}")
print(f"mismatches={len(mismatches)}")
if mismatches:
    print(json.dumps(mismatches[:10], indent=2, sort_keys=True))
    raise SystemExit(1)
