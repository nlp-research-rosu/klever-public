#!/usr/bin/env python3
"""Independent differential test for HumanEval/35.

Oracle: /reference/canonical.py
Generated program: /candidate/solution.py
Seeded generated inputs are printed in full for reproducibility.
"""

from __future__ import annotations

import importlib.util
import math
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: str) -> Callable[[list], Any]:
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.max_element


canonical = load_function("/reference/canonical.py")
generated = load_function("/candidate/solution.py")


def run(fn: Callable[[list], Any], values: list[Any]) -> dict[str, Any]:
    try:
        result = fn(values)
        identity_indices = [i for i, value in enumerate(values) if value is result]
        return {
            "kind": "return",
            "type": type(result).__name__,
            "repr": repr(result),
            "identity_indices": identity_indices,
        }
    except Exception as err:  # The exception class is observable at the boundary.
        return {"kind": "raise", "type": type(err).__name__}


def equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if left["kind"] != right["kind"] or left["type"] != right["type"]:
        return False
    if left["kind"] == "raise":
        return True
    # repr preserves signed zero and infinities. For NaN, identity selection
    # identifies which list element was returned.
    return (
        left["repr"] == right["repr"]
        and left["identity_indices"] == right["identity_indices"]
    )


cases: list[tuple[str, list[Any], str]] = [
    ("prompt-1", [1, 2, 3], "intended"),
    (
        "prompt-2",
        [5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10],
        "intended",
    ),
    ("empty", [], "invalid-empty"),
    ("singleton-negative", [-4], "intended"),
    ("replace-branch", [1, 2], "intended"),
    ("keep-branch", [2, 1], "intended"),
    ("tie-first", [2, 2, 1], "intended"),
    ("booleans", [False, True, False], "intended"),
    ("mixed-numeric", [1, 2.5, True, -4], "intended"),
    (
        "int-float-2pow53",
        [9007199254740993, 9007199254740992.0],
        "intended",
    ),
    ("positive-infinity", [1.0, float("inf"), 2.0], "intended"),
    ("negative-infinity", [float("-inf"), -2.0], "intended"),
    ("nan-head", [float("nan"), 1.0], "intended"),
    ("nan-tail", [1.0, float("nan")], "intended"),
    ("signed-zero-negative-first", [-0.0, 0.0], "intended"),
    ("signed-zero-positive-first", [0.0, -0.0], "intended"),
    ("ascii-strings", ["ant", "zebra", "yak"], "intended"),
    ("unicode-strings", ["é", "😀", "Ω"], "intended"),
    ("mixed-incomparable", [1, "1"], "invalid-incomparable"),
    ("nested-lists", [[1, 9], [2], [1, 10]], "supplied-model-gap"),
    ("tuples", [(1, 9), (2,), (1, 10)], "supplied-model-gap"),
]

rng = random.Random(350035)
for i in range(150):
    n = rng.randint(1, 20)
    cases.append(
        (
            f"generated-int-{i:03d}",
            [rng.randint(-10**12, 10**12) for _ in range(n)],
            "intended",
        )
    )

alphabet = "abczAZ09"
for i in range(50):
    n = rng.randint(1, 15)
    values = [
        "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 8)))
        for _ in range(n)
    ]
    cases.append((f"generated-str-{i:03d}", values, "intended"))

mismatches: list[str] = []
expected_boundary_differences: list[str] = []
for name, values, category in cases:
    oracle = run(canonical, values)
    observed = run(generated, values)
    same = equivalent(oracle, observed)
    print(
        repr(
            {
                "name": name,
                "category": category,
                "input": values,
                "canonical": oracle,
                "generated": observed,
                "same": same,
            }
        )
    )
    if not same:
        if category == "invalid-empty":
            expected_boundary_differences.append(name)
        else:
            mismatches.append(name)

print(
    repr(
        {
            "seed": 350035,
            "case_count": len(cases),
            "material_mismatch_count": len(mismatches),
            "material_mismatches": mismatches,
            "documented_invalid_boundary_difference_count": len(
                expected_boundary_differences
            ),
            "documented_invalid_boundary_differences": expected_boundary_differences,
        }
    )
)
raise SystemExit(1 if mismatches else 0)
