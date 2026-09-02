#!/usr/bin/env python3
"""Independent canonical-versus-candidate differential test for HumanEval 81."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path


def load_entry(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.numerical_letter_grade


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: differential_test.py CANONICAL SOLUTION INPUT_RECORD", file=sys.stderr)
        return 64

    canonical = load_entry("trusted_canonical", Path(sys.argv[1]))
    generated = load_entry("candidate_solution", Path(sys.argv[2]))
    input_record = Path(sys.argv[3])

    thresholds = [0.0, 0.7, 1.0, 1.3, 1.7, 2.0, 2.3, 2.7, 3.0, 3.3, 3.7, 4.0]
    cases: list[dict[str, object]] = [
        {"name": "documented-example", "grades": [4.0, 3, 1.7, 2, 3.5]},
        {"name": "empty", "grades": []},
        {"name": "all-exact-boundaries", "grades": thresholds},
        {"name": "integer-boundaries", "grades": [0, 1, 2, 3, 4]},
        {"name": "extended-canonical-domain", "grades": [-10.0, -0.1, 4.1, 10.0]},
    ]

    for value in thresholds:
        cases.append(
            {
                "name": f"nextafter-around-{value!r}",
                "grades": [
                    math.nextafter(value, -math.inf),
                    value,
                    math.nextafter(value, math.inf),
                ],
            }
        )

    rng = random.Random(810081)
    for index in range(200):
        length = rng.randrange(0, 17)
        grades = [rng.uniform(0.0, 4.0) for _ in range(length)]
        cases.append({"name": f"seeded-uniform-{index:03d}", "grades": grades})

    input_record.write_text(
        json.dumps(
            {
                "seed": 810081,
                "generated_case_count": 200,
                "generated_length_range": [0, 16],
                "generated_value_range": [0.0, 4.0],
                "cases": cases,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    checked_values = 0
    for case in cases:
        grades = case["grades"]
        assert isinstance(grades, list)
        expected = canonical(grades)
        actual = generated(grades)
        checked_values += len(grades)
        if expected != actual:
            mismatches.append(
                {
                    "name": case["name"],
                    "grades": grades,
                    "canonical": expected,
                    "candidate": actual,
                }
            )

    print(f"case_count={len(cases)}")
    print(f"grade_value_count={checked_values}")
    print("fixed_cases=17 (example, empty, aggregate boundaries, integers, extended, 12 nextafter triples)")
    print("generated_cases=200 seed=810081 lengths=0..16 values=uniform[0.0,4.0]")
    print(f"mismatch_count={len(mismatches)}")
    if mismatches:
        print(json.dumps(mismatches, indent=2, sort_keys=True))
        return 1
    print("RESULT: canonical and candidate outputs agree on every recorded case")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
