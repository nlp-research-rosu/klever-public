#!/usr/bin/env python3
"""Concrete satisfiability witnesses for each target entry precondition."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Any


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", Path("/tmp/audit-work/47-median/trusted/canonical.py"))
generated = load("generated_solution", Path("/tmp/audit-work/47-median/candidate-src/solution.py"))

witnesses: list[tuple[str, list[Any], tuple[type, ...], Any]] = [
    ("median-odd", [3, 1, 2], (int,), 2),
    ("median-even-int-int", [1, 3], (int, int), 2.0),
    ("median-even-int-bool", [0, True], (int, bool), 0.5),
    ("median-even-bool-int", [False, 1], (bool, int), 0.5),
    ("median-even-bool-bool", [False, True], (bool, bool), 0.5),
    ("median-even-float-float", [1.5, 2.5], (float, float), 2.0),
    ("median-even-int-float", [1, 2.5], (int, float), 1.75),
    ("median-even-float-int", [1.5, 2], (float, int), 1.75),
    ("median-even-bool-float", [False, 1.5], (bool, float), 0.75),
    ("median-even-float-bool", [-1.5, True], (float, bool), -0.25),
]


def same(left: Any, right: Any) -> bool:
    if isinstance(left, float) and isinstance(right, float):
        if math.isnan(left) and math.isnan(right):
            return True
    return type(left) is type(right) and left == right


def main() -> int:
    for label, values, center_types, expected in witnesses:
        ordered = sorted(values)
        assert len(ordered) > 0
        if label == "median-odd":
            assert len(ordered) % 2 == 1
            actual_types = (type(ordered[(len(ordered) - 1) // 2]),)
        else:
            assert len(ordered) % 2 == 0
            actual_types = (
                type(ordered[len(ordered) // 2 - 1]),
                type(ordered[len(ordered) // 2]),
            )
        assert actual_types == center_types, (label, actual_types, center_types)
        trusted = canonical.median(values)
        candidate = generated.median(values)
        assert same(trusted, expected), (label, trusted, expected)
        assert same(candidate, expected), (label, candidate, expected)
        print(
            f"{label}: VS={values!r} HP={{}} HL=0 sorted={ordered!r} "
            f"center_types={[kind.__name__ for kind in actual_types]} "
            f"canonical={trusted!r} generated={candidate!r}"
        )
    print(f"WITNESSES_PASS count={len(witnesses)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
