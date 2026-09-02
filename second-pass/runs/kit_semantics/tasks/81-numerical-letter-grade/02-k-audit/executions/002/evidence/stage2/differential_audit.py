#!/usr/bin/env python3
"""Independent differential test: trusted canonical.py versus candidate solution.py."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/candidate-src/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/stage2/differential-inputs.json")


def load_entry(path: Path, module_name: str) -> Callable[[list[Any]], list[str]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    entry = getattr(module, "numerical_letter_grade")
    if not callable(entry):
        raise RuntimeError(f"missing callable entry in {path}")
    return entry


def jsonable(value: Any) -> Any:
    if isinstance(value, float):
        if math.isnan(value):
            return {"float": "nan"}
        if math.isinf(value):
            return {"float": "+inf" if value > 0 else "-inf"}
        if value == 0.0 and math.copysign(1.0, value) < 0:
            return {"float": "-0.0"}
    return value


def build_cases() -> tuple[list[dict[str, Any]], list[float]]:
    cutoffs = [4.0, 3.7, 3.3, 3.0, 2.7, 2.3, 2.0, 1.7, 1.3, 1.0, 0.7, 0.0]
    boundary_values: list[float] = []
    for cutoff in cutoffs:
        boundary_values.extend(
            [
                math.nextafter(cutoff, -math.inf),
                cutoff,
                math.nextafter(cutoff, math.inf),
            ]
        )
    boundary_values.extend(
        [
            -math.inf,
            -100.0,
            -1.0,
            -0.0,
            4.1,
            100.0,
            math.inf,
            math.nan,
        ]
    )

    cases: list[dict[str, Any]] = [
        {"kind": "documented-example", "grades": [4.0, 3, 1.7, 2, 3.5]},
        {"kind": "empty", "grades": []},
        {"kind": "all-boundaries", "grades": list(boundary_values)},
        {"kind": "integer-representatives", "grades": [-2, -1, 0, 1, 2, 3, 4, 5]},
    ]
    for index, value in enumerate(boundary_values):
        cases.append({"kind": f"boundary-singleton-{index}", "grades": [value]})

    rng = random.Random(810729)
    choices: list[int | float] = [
        -10,
        -1,
        0,
        1,
        2,
        3,
        4,
        5,
        10,
        *boundary_values,
    ]
    for index in range(2000):
        length = rng.randrange(0, 41)
        grades: list[int | float] = []
        for _ in range(length):
            mode = rng.randrange(4)
            if mode == 0:
                grades.append(rng.randrange(-10, 11))
            elif mode == 1:
                grades.append(rng.uniform(-2.0, 6.0))
            else:
                grades.append(rng.choice(choices))
        cases.append({"kind": f"generated-{index}", "grades": grades})
    return cases, boundary_values


def main() -> int:
    canonical = load_entry(CANONICAL_PATH, "trusted_canonical_audit")
    candidate = load_entry(CANDIDATE_PATH, "candidate_solution_audit")
    cases, boundary_values = build_cases()

    serialized = [
        {"kind": case["kind"], "grades": [jsonable(value) for value in case["grades"]]}
        for case in cases
    ]
    INPUTS_PATH.write_text(
        json.dumps(serialized, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    input_digest = hashlib.sha256(INPUTS_PATH.read_bytes()).hexdigest()

    mismatches = 0
    exception_mismatches = 0
    for case in cases:
        grades = case["grades"]
        try:
            expected = canonical(list(grades))
            expected_exc: BaseException | None = None
        except BaseException as error:
            expected = None
            expected_exc = error
        try:
            actual = candidate(list(grades))
            actual_exc: BaseException | None = None
        except BaseException as error:
            actual = None
            actual_exc = error
        if expected_exc is not None or actual_exc is not None:
            expected_type = type(expected_exc) if expected_exc is not None else None
            actual_type = type(actual_exc) if actual_exc is not None else None
            if expected_type != actual_type:
                exception_mismatches += 1
                print(
                    f"EXCEPTION_MISMATCH kind={case['kind']} "
                    f"expected={expected_type} actual={actual_type}"
                )
        elif expected != actual:
            mismatches += 1
            print(
                f"RESULT_MISMATCH kind={case['kind']} "
                f"grades={grades!r} expected={expected!r} actual={actual!r}"
            )

    example = [4.0, 3, 1.7, 2, 3.5]
    print(f"documented_example={candidate(example)!r}")
    print(
        f"cases={len(cases)} boundary_values={len(boundary_values)} "
        f"generated_cases=2000 result_mismatches={mismatches} "
        f"exception_mismatches={exception_mismatches}"
    )
    print(f"inputs_path={INPUTS_PATH} sha256={input_digest}")
    return 1 if mismatches or exception_mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
