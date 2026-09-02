#!/usr/bin/env python3
"""Independent differential check for HumanEval 45 triangle_area."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path, module_name: str) -> Callable[..., Any]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def outcome(function: Callable[..., Any], args: tuple[Any, ...]) -> dict[str, Any]:
    try:
        value = function(*args)
    except Exception as error:  # This records boundary behavior, not just successes.
        return {
            "kind": "exception",
            "type": type(error).__name__,
        }
    if isinstance(value, float):
        if math.isnan(value):
            rendered = "nan"
        elif value == 0.0:
            rendered = "-0.0" if math.copysign(1.0, value) < 0 else "0.0"
        else:
            rendered = value.hex()
    else:
        rendered = repr(value)
    return {
        "kind": "value",
        "type": type(value).__name__,
        "rendered": rendered,
    }


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: differential_triangle_area.py CANONICAL GENERATED")

    canonical = load_function(Path(sys.argv[1]), "trusted_triangle_area")
    generated = load_function(Path(sys.argv[2]), "generated_triangle_area")

    cases: list[tuple[str, tuple[Any, ...]]] = [
        ("documented-example", (5, 3)),
        ("zero-base", (0, 9)),
        ("zero-height", (9, 0)),
        ("both-zero", (0, 0)),
        ("unit", (1, 1)),
        ("odd-product", (3, 3)),
        ("negative-base", (-3, 6)),
        ("negative-height", (3, -6)),
        ("both-negative", (-3, -6)),
        ("large-exact-int", (2**53 - 1, 2)),
        ("largest-finite-scaled-division", ((2**53 - 1) * (2**972), 1)),
        ("huge-int-overflow", (10**400, 1)),
        ("float-halves", (0.5, 0.25)),
        ("negative-zero", (-0.0, 7.0)),
        ("positive-infinity", (float("inf"), 2.0)),
        ("nan", (float("nan"), 2.0)),
        ("empty-arity", ()),
        ("one-argument", (1,)),
        ("extra-argument", (1, 2, 3)),
        ("empty-list-invalid-type", ([], 2)),
    ]

    rng = random.Random(450045)
    for index in range(400):
        cases.append(
            (
                f"generated-int-{index:03d}",
                (rng.randint(-1_000_000, 1_000_000), rng.randint(-1_000_000, 1_000_000)),
            )
        )
    for index in range(80):
        cases.append(
            (
                f"generated-float-{index:03d}",
                (rng.uniform(-10_000.0, 10_000.0), rng.uniform(-10_000.0, 10_000.0)),
            )
        )

    mismatches: list[dict[str, Any]] = []
    encoded_cases: list[dict[str, Any]] = []
    for name, args in cases:
        left = outcome(canonical, args)
        right = outcome(generated, args)
        item = {
            "name": name,
            "args": [repr(arg) for arg in args],
            "canonical": left,
            "generated": right,
        }
        encoded_cases.append(item)
        if left != right:
            mismatches.append(item)

    print(json.dumps(
        {
            "oracle": str(Path(sys.argv[1]).resolve()),
            "generated": str(Path(sys.argv[2]).resolve()),
            "seed": 450045,
            "case_count": len(cases),
            "branch_boundaries": "none: source contains no conditional branches",
            "cases": encoded_cases,
            "mismatch_count": len(mismatches),
            "mismatches": mismatches,
        },
        indent=2,
        sort_keys=True,
    ))
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
