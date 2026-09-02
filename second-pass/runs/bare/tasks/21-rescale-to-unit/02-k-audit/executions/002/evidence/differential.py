#!/usr/bin/env python3
"""Differential tests: trusted HumanEval canonical vs submitted solution.py."""

from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_function(path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(f"loaded_{path.stem}", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def outcome(function: Callable[[list[float]], list[float]], values: list[float]) -> Any:
    try:
        return {"kind": "return", "value": function(values.copy())}
    except Exception as error:  # boundary cases deliberately include invalid inputs
        return {
            "kind": "raise",
            "type": type(error).__name__,
            "message": str(error),
        }


def main() -> int:
    canonical = load_function(Path("/reference/canonical.py"))
    submitted = load_function(Path("/candidate/solution.py"))

    cases: list[tuple[str, list[float]]] = [
        ("documented-example", [1.0, 2.0, 3.0, 4.0, 5.0]),
        ("empty-out-of-domain", []),
        ("singleton-out-of-domain", [4.0]),
        ("equal-pair-degenerate", [4.0, 4.0]),
        ("two-ascending", [-3.5, 9.25]),
        ("two-descending", [9.25, -3.5]),
        ("min-equal-max-branches", [-2.0, -2.0, 5.0, 5.0]),
        ("min-middle-max-first", [8.0, 2.0, -4.0, 2.0, 8.0]),
        ("negative-fractions", [-10.5, -3.25, -7.0, -3.25, -10.5]),
        ("length-six", [3.0, -1.0, 7.0, 0.0, 7.0, 2.5]),
        (
            "wide-magnitude",
            [-1.0e100, 0.0, 1.0e100, -5.0e99, 7.5e99],
        ),
    ]

    rng = random.Random(210721)
    for length in range(2, 13):
        for sample in range(3):
            values = [float(rng.randint(-40, 40)) / 4.0 for _ in range(length)]
            if min(values) == max(values):
                values[-1] += 1.0
            cases.append((f"generated-n{length}-s{sample}", values))

    mismatches = 0
    print(f"case_count={len(cases)}")
    for name, values in cases:
        expected = outcome(canonical, values)
        actual = outcome(submitted, values)
        match = actual == expected
        if not match:
            mismatches += 1
        print(
            json.dumps(
                {
                    "name": name,
                    "input": values,
                    "canonical": expected,
                    "submitted": actual,
                    "match": match,
                },
                sort_keys=True,
                allow_nan=False,
            )
        )
    print(f"mismatches={mismatches}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
