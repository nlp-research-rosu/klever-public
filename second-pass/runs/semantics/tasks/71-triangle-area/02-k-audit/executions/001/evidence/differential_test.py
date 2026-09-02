#!/usr/bin/env python3
"""Independent differential check for the trusted and submitted Python entries."""

from __future__ import annotations

import importlib.util
import itertools
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path) -> Callable[[Any, Any, Any], Any]:
    spec = importlib.util.spec_from_file_location(f"audit_{path.stem}_{id(path)}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.triangle_area


def outcome(fn: Callable[[Any, Any, Any], Any], case: tuple[Any, Any, Any]) -> dict[str, Any]:
    try:
        value = fn(*case)
    except Exception as exc:  # The exception class is observable too.
        return {"kind": "exception", "type": type(exc).__name__, "message": str(exc)}
    if isinstance(value, float) and math.isnan(value):
        value_repr: Any = "NaN"
    else:
        value_repr = value
    return {"kind": "value", "type": type(value).__name__, "value": value_repr}


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: differential_test.py TRUSTED_CANONICAL SUBMITTED_SOLUTION", file=sys.stderr)
        return 64

    trusted = load_entry(Path(sys.argv[1]))
    submitted = load_entry(Path(sys.argv[2]))

    named_cases: list[tuple[str, tuple[Any, Any, Any]]] = [
        ("documented-valid-3-4-5", (3, 4, 5)),
        ("documented-invalid-1-2-10", (1, 2, 10)),
        ("zero-boundary", (0, 0, 0)),
        ("first-branch-equality", (1, 2, 3)),
        ("first-branch-just-valid", (2, 2, 3)),
        ("second-branch-equality", (2, 4, 2)),
        ("second-branch-just-valid", (2, 3, 2)),
        ("third-branch-equality", (4, 2, 2)),
        ("third-branch-just-valid", (3, 2, 2)),
        ("equilateral-unit", (1, 1, 1)),
        ("negative-mixed", (-1, 3, 3)),
        ("all-negative", (-3, -4, -5)),
        ("large-exact", (10**6, 10**6, 10**6)),
        ("huge-equilateral-python-overflow", (10**400, 10**400, 10**400)),
        ("float-valid", (3.5, 4.5, 5.5)),
        ("float-first-equality", (1.25, 2.5, 3.75)),
        ("float-near-boundary-valid", (1.25, 2.5, 3.749999)),
    ]

    generated_cases: list[tuple[Any, Any, Any]] = []
    # Exhaustive signed integer cube covers every guard direction and many
    # equality/strict branch boundaries.
    generated_cases.extend(itertools.product(range(-8, 21), repeat=3))
    # A deterministic broader positive sample exercises larger magnitudes.
    rng = random.Random(710071)
    generated_cases.extend(
        (rng.randint(0, 10**6), rng.randint(0, 10**6), rng.randint(0, 10**6))
        for _ in range(10_000)
    )
    # Decimal half-step grid checks the untyped contract's ordinary real inputs.
    halves = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 5.0, 10.0]
    generated_cases.extend(itertools.product(halves, repeat=3))

    mismatches: list[dict[str, Any]] = []
    named_results: list[dict[str, Any]] = []
    total = 0

    for name, case in named_cases:
        lhs = outcome(trusted, case)
        rhs = outcome(submitted, case)
        total += 1
        named_results.append({"name": name, "input": case, "trusted": lhs, "submitted": rhs})
        if lhs != rhs:
            mismatches.append(named_results[-1])

    for case in generated_cases:
        case_tuple = tuple(case)
        lhs = outcome(trusted, case_tuple)
        rhs = outcome(submitted, case_tuple)
        total += 1
        if lhs != rhs and len(mismatches) < 20:
            mismatches.append(
                {"name": "generated", "input": case_tuple, "trusted": lhs, "submitted": rhs}
            )

    print(json.dumps({"named_results": named_results}, indent=2, sort_keys=True))
    print(
        json.dumps(
            {
                "scope": {
                    "named": len(named_cases),
                    "exhaustive_integer_cube": "[-8,20]^3",
                    "deterministic_random_nonnegative_integers": 10_000,
                    "half_step_grid": f"{len(halves)}^3",
                },
                "total_cases": total,
                "mismatch_count": len(mismatches),
                "first_mismatches": mismatches,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
