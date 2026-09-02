#!/usr/bin/env python3
"""Independent source-level differential test for HumanEval/81."""

from __future__ import annotations

import importlib.util
import json
import math
import random
from pathlib import Path


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/candidate/solution.py")
RESULT_PATH = Path("/audit-output/evidence/differential-results.json")


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


def json_value(value):
    if isinstance(value, float):
        if math.isnan(value):
            return {"float": "nan"}
        if math.isinf(value):
            return {"float": "+inf" if value > 0 else "-inf"}
        if value == 0.0 and math.copysign(1.0, value) < 0:
            return {"float": "-0.0"}
    return value


def build_cases() -> list[tuple[str, list[object]]]:
    cases: list[tuple[str, list[object]]] = [
        ("documented-example", [4.0, 3, 1.7, 2, 3.5]),
        ("empty", []),
        ("all-table-boundaries", [
            4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0,
            1.7, 1.3, 1.0, 0.7, 0.0,
        ]),
        ("outside-range", [-math.inf, -1000, -1.0, -0.0, 4.1, 5, 1000, math.inf]),
        ("special-floats", [math.nan, math.inf, -math.inf]),
        ("integers", list(range(-3, 9))),
        ("bool-peripheral", [False, True]),
    ]

    thresholds = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    for threshold in thresholds:
        cases.append(
            (
                f"neighbors-{threshold!r}",
                [
                    math.nextafter(threshold, -math.inf),
                    threshold,
                    math.nextafter(threshold, math.inf),
                ],
            )
        )

    rng = random.Random(810081)
    for index in range(600):
        length = rng.randrange(0, 30)
        values: list[object] = []
        for _ in range(length):
            selector = rng.randrange(5)
            if selector == 0:
                values.append(rng.randint(-100, 100))
            elif selector == 1:
                values.append(rng.uniform(-10.0, 10.0))
            elif selector == 2:
                threshold = rng.choice(thresholds)
                values.append(math.nextafter(threshold, rng.choice([-math.inf, math.inf])))
            elif selector == 3:
                values.append(rng.choice(thresholds))
            else:
                values.append(rng.randint(-(10**18), 10**18))
        cases.append((f"generated-{index:03d}", values))
    return cases


def main() -> int:
    canonical = load_function(CANONICAL_PATH, "trusted_canonical_81")
    generated = load_function(GENERATED_PATH, "generated_solution_81")
    records = []
    mismatches = []

    for name, values in build_cases():
        expected = canonical(list(values))
        actual = generated(list(values))
        record = {
            "name": name,
            "input": [json_value(value) for value in values],
            "canonical": expected,
            "generated": actual,
            "match": expected == actual,
        }
        records.append(record)
        if expected != actual:
            mismatches.append(record)

    result = {
        "oracle": str(CANONICAL_PATH),
        "generated": str(GENERATED_PATH),
        "case_count": len(records),
        "element_count": sum(len(record["input"]) for record in records),
        "mismatch_count": len(mismatches),
        "cases": records,
    }
    RESULT_PATH.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"case_count={result['case_count']}")
    print(f"element_count={result['element_count']}")
    print(f"mismatch_count={result['mismatch_count']}")
    print(f"results={RESULT_PATH}")
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
