#!/usr/bin/env python3
"""Independent candidate-versus-canonical differential test for HumanEval/21."""

from __future__ import annotations

import importlib.util
import json
import math
import random
import sys
from pathlib import Path
from typing import Any, Callable

CANONICAL_PATH = Path("/tmp/audit-work/21-rescale-to-unit/trusted-canonical.py")
CANDIDATE_PATH = Path("/tmp/audit-work/21-rescale-to-unit/solution.py")
INPUTS_PATH = Path("/audit-output/evidence/differential-inputs.json")


def load_entry(module_name: str, path: Path) -> Callable[[list[float]], list[float]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.rescale_to_unit


def encode_float(value: float) -> str:
    if math.isnan(value):
        return "-nan" if math.copysign(1.0, value) < 0 else "nan"
    return value.hex()


def encode_value(value: Any) -> Any:
    if isinstance(value, float):
        return {"float_hex": encode_float(value)}
    if isinstance(value, list):
        return [encode_value(item) for item in value]
    return value


def outcome(function: Callable[[list[float]], list[float]], values: list[float]) -> dict[str, Any]:
    argument = list(values)
    before = [encode_float(item) for item in argument]
    try:
        result = function(argument)
        observed: dict[str, Any] = {"kind": "return", "value": encode_value(result)}
    except BaseException as error:  # The exception class is part of the observed behavior.
        observed = {"kind": "raise", "type": type(error).__name__, "message": str(error)}
    observed["input_after"] = [encode_float(item) for item in argument]
    observed["input_unchanged"] = observed["input_after"] == before
    return observed


def make_cases() -> list[tuple[str, list[float]]]:
    explicit = [
        ("documented-example", [1.0, 2.0, 3.0, 4.0, 5.0]),
        ("empty-outside-domain", []),
        ("singleton-outside-domain", [2.0]),
        ("two-equal-domain-edge", [2.0, 2.0]),
        ("two-ascending", [1.0, 5.0]),
        ("two-descending", [5.0, 1.0]),
        ("negative-cross-zero", [-3.0, -1.0, 1.0]),
        ("duplicate-extrema", [-2.0, -2.0, 0.0, 4.0, 4.0]),
        ("min-interior-max-first", [9.0, -4.0, 2.0, 1.0]),
        ("max-interior-min-first", [-4.0, 9.0, 2.0, 1.0]),
        ("signed-zero-equal", [-0.0, 0.0]),
        ("small-subnormal-range", [0.0, 5e-324]),
        ("large-finite-range", [-1e308, 0.0, 1e308]),
        ("positive-infinity", [0.0, 1.0, float("inf")]),
        ("two-infinities", [float("-inf"), float("inf")]),
        ("nan-first", [float("nan"), 0.0, 1.0]),
        ("nan-last", [0.0, 1.0, float("nan")]),
    ]
    rng = random.Random(210021)
    pool = [float(value) / 2.0 for value in range(-24, 25)]
    generated: list[tuple[str, list[float]]] = []
    for index in range(500):
        length = rng.randint(2, 10)
        generated.append(
            (f"generated-finite-{index:03d}", [rng.choice(pool) for _ in range(length)])
        )
    return explicit + generated


def main() -> int:
    canonical = load_entry("trusted_canonical_21", CANONICAL_PATH)
    candidate = load_entry("generated_candidate_21", CANDIDATE_PATH)
    cases = make_cases()
    INPUTS_PATH.write_text(
        json.dumps(
            [
                {"label": label, "values": [encode_float(value) for value in values]}
                for label, values in cases
            ],
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    mismatches = []
    return_count = 0
    raise_count = 0
    for label, values in cases:
        expected = outcome(canonical, values)
        actual = outcome(candidate, values)
        if expected["kind"] == "return":
            return_count += 1
        else:
            raise_count += 1
        if expected != actual:
            mismatches.append(
                {"label": label, "input": encode_value(values), "canonical": expected, "candidate": actual}
            )

    print(f"canonical={CANONICAL_PATH}")
    print(f"candidate={CANDIDATE_PATH}")
    print(f"inputs_artifact={INPUTS_PATH}")
    print(f"seed=210021 explicit_cases=17 generated_cases=500 total_cases={len(cases)}")
    print(f"canonical_return_cases={return_count} canonical_raise_cases={raise_count}")
    print(f"mismatch_count={len(mismatches)}")
    for mismatch in mismatches[:20]:
        print(json.dumps(mismatch, sort_keys=True))
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
