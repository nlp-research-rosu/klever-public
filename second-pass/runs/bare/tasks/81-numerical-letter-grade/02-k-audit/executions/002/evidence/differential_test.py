#!/usr/bin/env python3
"""Independent differential test of candidate Python against trusted canonical."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import random
import sys


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


def main() -> int:
    canonical = load_function("trusted_canonical", Path("/tmp/audit-work/canonical.py"))
    generated = load_function(
        "candidate_solution", Path("/tmp/audit-work/reconstruction/solution.py")
    )

    thresholds = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    cases: list[tuple[str, list[float]]] = [
        ("documented-example", [4.0, 3.0, 1.7, 2.0, 3.5]),
        ("empty", []),
        ("all-exact-thresholds", thresholds),
        ("outside-GPA-range", [-100.0, -1.0, -0.0, 4.1, 5.0, 100.0]),
        ("special-floats", [float("-inf"), float("inf"), float("nan")]),
    ]

    for threshold in thresholds:
        cases.append(
            (
                f"neighbors-of-{threshold!r}",
                [
                    math.nextafter(threshold, -math.inf),
                    threshold,
                    math.nextafter(threshold, math.inf),
                ],
            )
        )

    rng = random.Random(810081)
    generated_values = [rng.uniform(-1.0, 5.0) for _ in range(100)]
    cases.extend(
        [
            ("generated-first-1", generated_values[:1]),
            ("generated-first-2", generated_values[:2]),
            ("generated-first-5", generated_values[:5]),
            ("generated-all-100", generated_values),
        ]
    )

    mismatches = 0
    print(f"case_count={len(cases)} scalar_occurrences={sum(map(lambda x: len(x[1]), cases))}")
    for name, values in cases:
        expected = canonical(values)
        actual = generated(values)
        same = actual == expected
        if not same:
            mismatches += 1
        print(
            f"CASE {name}: input={values!r} canonical={expected!r} "
            f"candidate={actual!r} match={same}"
        )

    print(f"mismatches={mismatches}")
    if mismatches:
        return 1
    print("DIFFERENTIAL_TEST: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
