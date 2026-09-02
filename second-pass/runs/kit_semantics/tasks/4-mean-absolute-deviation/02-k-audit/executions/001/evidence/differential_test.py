#!/usr/bin/env python3
"""Independent canonical-versus-generated differential test for HumanEval/4."""

from __future__ import annotations

import importlib.util
import math
import random
import struct
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/reconstruct/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


@dataclass(frozen=True)
class Outcome:
    kind: str
    detail: object


def run(function: Callable[[list[float]], float], values: list[float]) -> Outcome:
    try:
        return Outcome("value", function(list(values)))
    except Exception as error:  # The exception type is the observable result.
        return Outcome("exception", type(error).__name__)


def float_equivalent(left: float, right: float) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    if left != right:
        return False
    if left == 0.0:
        return struct.pack(">d", left) == struct.pack(">d", right)
    return True


def equivalent(left: Outcome, right: Outcome) -> bool:
    if left.kind != right.kind:
        return False
    if left.kind == "exception":
        return left.detail == right.detail
    assert isinstance(left.detail, float) and isinstance(right.detail, float)
    return float_equivalent(left.detail, right.detail)


def main() -> None:
    print("COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 "
          "/audit-output/evidence/differential_test.py")
    print(f"python_version={sys.version.split()[0]}")
    canonical = load_entry(CANONICAL_PATH, "trusted_humaneval4_canonical")
    generated = load_entry(GENERATED_PATH, "audited_humaneval4_generated")

    named_cases: list[tuple[str, list[float]]] = [
        ("documented-example", [1.0, 2.0, 3.0, 4.0]),
        ("empty-branch", []),
        ("singleton-branch-boundary", [1.0]),
        ("two-equal", [7.25, 7.25]),
        ("two-opposite", [-1.0, 1.0]),
        ("mixed-sign", [-3.5, -0.5, 10.0]),
        ("all-zero", [0.0, 0.0, 0.0]),
        ("signed-zero", [-0.0, 0.0]),
        ("smallest-subnormals", [5e-324, -5e-324, 0.0]),
        ("minimum-normal", [sys.float_info.min, -sys.float_info.min]),
        ("maximum-finite", [sys.float_info.max, sys.float_info.max]),
        ("integer-values-runtime-boundary", [1, 2, 3, 4]),
        ("mixed-int-float-runtime-boundary", [1, 2.5, -3]),
        ("positive-infinity", [math.inf, 1.0]),
        ("negative-infinity", [-math.inf, -1.0]),
        ("nan", [math.nan, 1.0]),
    ]

    random_cases: list[tuple[str, list[float]]] = []
    rng = random.Random(0x4BAD2026)
    for size in list(range(1, 18)) + [31, 32, 33, 63, 64]:
        for sample in range(12):
            random_cases.append(
                (
                    f"random-size-{size}-sample-{sample}",
                    [rng.uniform(-1.0e9, 1.0e9) for _ in range(size)],
                )
            )

    mismatches: list[tuple[str, list[float], Outcome, Outcome]] = []
    nonempty_finite_mismatches = 0
    for name, values in named_cases + random_cases:
        expected = run(canonical, values)
        actual = run(generated, values)
        if name in {case_name for case_name, _ in named_cases}:
            print(
                f"NAMED {name}: canonical={expected.kind}:{expected.detail!r} "
                f"generated={actual.kind}:{actual.detail!r} "
                f"equivalent={equivalent(expected, actual)}"
            )
        if not equivalent(expected, actual):
            mismatches.append((name, values, expected, actual))
            if values and all(math.isfinite(value) for value in values):
                nonempty_finite_mismatches += 1

    print(f"total_cases={len(named_cases) + len(random_cases)}")
    print(f"random_cases={len(random_cases)}")
    print(f"all_mismatches={len(mismatches)}")
    print(f"nonempty_finite_mismatches={nonempty_finite_mismatches}")
    for name, values, expected, actual in mismatches:
        print(
            f"MISMATCH {name}: input={values!r} "
            f"canonical={expected} generated={actual}"
        )

    assert nonempty_finite_mismatches == 0
    assert len(mismatches) == 1
    assert mismatches[0][0] == "empty-branch"
    assert mismatches[0][2] == Outcome("exception", "ZeroDivisionError")
    assert mismatches[0][3] == Outcome("value", 0.0)
    print("STATUS: expected sole empty-input divergence confirmed")


if __name__ == "__main__":
    main()
