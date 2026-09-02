#!/usr/bin/env python3
"""Independent Python differential test for HumanEval/20."""

from __future__ import annotations

import importlib.util
import math
import pathlib
import random
import sys
from typing import Any, Callable


CANONICAL_PATH = pathlib.Path("/reference/canonical.py")
GENERATED_PATH = pathlib.Path("/tmp/audit-work/source/solution.py")


def load_entry(path: pathlib.Path, module_name: str) -> Callable[[list[float]], Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def capture(function: Callable[[list[float]], Any], values: list[float]) -> tuple[str, Any]:
    try:
        return ("return", function(list(values)))
    except Exception as error:  # Deliberately compare boundary exceptions.
        return ("exception", (type(error).__name__, str(error)))


def same_value(left: Any, right: Any) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
        return left == right
    if isinstance(left, tuple) and isinstance(right, tuple):
        return len(left) == len(right) and all(
            same_value(l_item, r_item) for l_item, r_item in zip(left, right)
        )
    return left == right


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical")
    generated = load_entry(GENERATED_PATH, "scratch_generated")

    cases: list[tuple[str, list[float], bool]] = [
        ("outside-empty", [], False),
        ("outside-singleton", [7.0], False),
        ("example-distinct", [1.0, 2.0, 3.0, 4.0, 5.0, 2.2], True),
        ("example-duplicate", [1.0, 2.0, 3.0, 4.0, 5.0, 2.0], True),
        ("length2-initial-noswap", [1.0, 2.0], True),
        ("length2-initial-swap", [2.0, 1.0], True),
        ("length2-initial-equal", [2.0, 2.0], True),
        ("inner-pair-swap", [0.0, 8.0, 7.0], True),
        ("gap-update", [0.0, 10.0, 1.0], True),
        ("gap-no-update", [0.0, 1.0, 10.0], True),
        ("gap-tie", [0.0, 2.0, 4.0], True),
        ("negative", [-10.0, -3.0, -3.5, 9.0], True),
        ("signed-zero", [-0.0, 0.0, 1.0], True),
        ("mixed-magnitude", [-1e300, -1e-300, 1e-300, 1e300], True),
        ("infinities", [float("-inf"), -1.0, 1.0, float("inf")], True),
        ("nan-first", [float("nan"), 1.0, 2.0], True),
        ("nan-later", [1.0, 2.0, float("nan")], True),
    ]

    rng = random.Random(20260723)
    palette = [float(value) / 4.0 for value in range(-32, 33)]
    for index in range(200):
        length = rng.randint(2, 10)
        values = [rng.choice(palette) for _ in range(length)]
        cases.append((f"generated-{index:03d}", values, True))

    intended_mismatches = 0
    outside_mismatches = 0
    for name, values, intended in cases:
        oracle = capture(canonical, values)
        observed = capture(generated, values)
        matches = (
            oracle[0] == observed[0]
            and same_value(oracle[1], observed[1])
        )
        if not matches:
            if intended:
                intended_mismatches += 1
            else:
                outside_mismatches += 1
        print(
            f"{name}: intended={intended} input={values!r} "
            f"canonical={oracle!r} generated={observed!r} match={matches}"
        )

    intended_count = sum(1 for _, _, intended in cases if intended)
    outside_count = len(cases) - intended_count
    print(f"TOTAL_CASES={len(cases)}")
    print(f"INTENDED_CASES={intended_count}")
    print(f"INTENDED_MISMATCHES={intended_mismatches}")
    print(f"OUTSIDE_CASES={outside_count}")
    print(f"OUTSIDE_MISMATCHES={outside_mismatches}")
    return 1 if intended_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
