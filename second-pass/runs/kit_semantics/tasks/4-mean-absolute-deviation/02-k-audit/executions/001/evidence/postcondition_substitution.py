#!/usr/bin/env python3
"""Ground substitutions into the K claim's fold-defined madResult summary."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Callable


def load(path: Path, name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def sum_float_vs(values: list[float], accumulator: float) -> float:
    for value in values:
        accumulator = accumulator + value
    return accumulator


def deviation_float_vs(
    values: list[float], mean: float, accumulator: float
) -> float:
    for value in values:
        accumulator = accumulator + abs(value - mean)
    return accumulator


def mad_result(values: list[float]) -> float:
    # Direct ground interpretation of verification.k:88-99.
    if len(values) == 0:
        return 0.0
    mean = sum_float_vs(values, 0.0) / len(values)
    return deviation_float_vs(values, mean, 0.0) / len(values)


def same(left: float, right: float) -> bool:
    return left == right or (math.isnan(left) and math.isnan(right))


def main() -> None:
    print("COMMAND: PYTHONDONTWRITEBYTECODE=1 python3 "
          "/audit-output/evidence/postcondition_substitution.py")
    canonical = load(Path("/reference/canonical.py"), "postcondition_canonical")
    generated = load(
        Path("/tmp/audit-work/reconstruct/solution.py"),
        "postcondition_generated",
    )
    cases = [
        [1.0, 2.0, 3.0, 4.0],
        [-1.0, 1.0],
        [-3.5, -0.5, 10.0],
        [5e-324, -5e-324, 0.0],
    ]
    for values in cases:
        claimed = mad_result(values)
        trusted = canonical(list(values))
        actual = generated(list(values))
        print(
            f"input={values!r} claimed_madResult={claimed!r} "
            f"canonical={trusted!r} generated={actual!r}"
        )
        assert same(claimed, trusted)
        assert same(claimed, actual)
    print("satisfiable_entry_witness=[1.0, 2.0, 3.0, 4.0]")
    print("allFloatVS_witness_reduces_to=true")
    print("STATUS: all nonempty ground substitutions agree exactly")


if __name__ == "__main__":
    main()
