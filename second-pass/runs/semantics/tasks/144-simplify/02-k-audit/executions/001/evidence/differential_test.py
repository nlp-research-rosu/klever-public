#!/usr/bin/env python3
"""Independent differential test for HumanEval 144 (simplify).

The exhaustive grid is all (A, B, C, D) in [1, 12]^4.  The generated sample
uses the fixed seed 144 and 500 four-tuples in [1, 10^12]^4.  Explicit
large-number cases probe the trusted canonical implementation's float-based
division boundary separately from the ordinary shared range.
"""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(module_path: Path, module_name: str) -> Callable[[str, str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.simplify


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical_144")
generated = load_entry(Path("/candidate/solution.py"), "candidate_solution_144")


def capture(fn: Callable[[str, str], bool], x: str, n: str) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": fn(x, n)}
    except Exception as err:  # Deliberately compare invalid-input behavior too.
        return {"kind": "raise", "type": type(err).__name__, "message": str(err)}


def record(label: str, x: str, n: str) -> bool:
    trusted = capture(canonical, x, n)
    candidate = capture(generated, x, n)
    equal = trusted == candidate
    print(
        json.dumps(
            {
                "label": label,
                "x": x,
                "n": n,
                "canonical": trusted,
                "candidate": candidate,
                "equal": equal,
            },
            sort_keys=True,
        )
    )
    return equal


explicit_cases = [
    ("documented-1", "1/5", "5/1"),
    ("documented-2", "1/6", "2/1"),
    ("documented-3", "7/10", "10/2"),
    ("true-unit-boundary", "1/1", "1/1"),
    ("false-remainder-one", "1/2", "1/1"),
    ("true-exact-boundary", "2/3", "3/2"),
    ("candidate-extra-example", "12/35", "70/24"),
    ("leading-zero-valid-numerals", "00012/00035", "00070/00024"),
    ("empty-invalid", "", ""),
    ("zero-numerator-outside-positive-domain", "0/7", "3/5"),
    ("zero-denominator-excluded", "1/0", "2/3"),
    (
        "float-rounding-witness-valid-positive",
        "18014398509481985/2",
        "1/1",
    ),
    ("float-overflow-witness-valid-positive", f"{10**400}/1", "1/1"),
]

explicit_mismatches = 0
for case in explicit_cases:
    if not record(*case):
        explicit_mismatches += 1

small_mismatches = []
small_total = 0
for a, b, c, d in itertools.product(range(1, 13), repeat=4):
    small_total += 1
    x = f"{a}/{b}"
    n = f"{c}/{d}"
    left = capture(canonical, x, n)
    right = capture(generated, x, n)
    if left != right:
        small_mismatches.append((a, b, c, d, left, right))

rng = random.Random(144)
random_mismatches = []
random_total = 500
for _ in range(random_total):
    a, b, c, d = (rng.randint(1, 10**12) for _ in range(4))
    x = f"{a}/{b}"
    n = f"{c}/{d}"
    left = capture(canonical, x, n)
    right = capture(generated, x, n)
    if left != right:
        random_mismatches.append((a, b, c, d, left, right))

print(
    json.dumps(
        {
            "summary": {
                "explicit_total": len(explicit_cases),
                "explicit_mismatches": explicit_mismatches,
                "small_grid_domain": "A,B,C,D in integers 1..12 inclusive",
                "small_grid_total": small_total,
                "small_grid_mismatches": len(small_mismatches),
                "small_grid_first_five": small_mismatches[:5],
                "random_seed": 144,
                "random_domain": "500 four-tuples, each component in 1..10^12",
                "random_total": random_total,
                "random_mismatches": len(random_mismatches),
                "random_first_five": random_mismatches[:5],
            }
        },
        sort_keys=True,
    )
)
