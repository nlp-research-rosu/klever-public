#!/usr/bin/env python3
"""Ground evaluation of the PairState/scanPairsVS equations in verification.k."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Callable


def load(path: Path, name: str) -> Callable[[list[float]], tuple[float, float]]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.find_closest_elements


def order_pair(a: float, b: float) -> tuple[float, float]:
    return (b, a) if a > b else (a, b)


def consider(pair: tuple[float, float], a: float, b: float) -> tuple[float, float]:
    low, high = order_pair(a, b)
    return (low, high) if high - low < pair[1] - pair[0] else pair


def claimed_scan(values: list[float]) -> tuple[float, float]:
    pair = order_pair(values[0], values[1])
    i, j = 0, 1
    while i < len(values) - 1:
        pair = consider(pair, values[i], values[j])
        if j + 1 == len(values):
            i, j = i + 1, i + 2
        else:
            j += 1
    return pair


def scalar_equal(a: float, b: float) -> bool:
    return (math.isnan(a) and math.isnan(b)) or a == b


def pair_equal(a: tuple[float, float], b: tuple[float, float]) -> bool:
    return scalar_equal(a[0], b[0]) and scalar_equal(a[1], b[1])


canonical = load(Path("/reference/canonical.py"), "substitution_canonical")
candidate = load(Path("/tmp/audit-work/reconstruction/solution.py"), "substitution_candidate")
cases = [
    [2.0, 1.0],
    [1.0, 2.0, 3.0, 4.0, 5.0, 2.2],
    [1.0, 2.0, 3.0, 4.0, 5.0, 2.0],
]

failures = 0
for values in cases:
    model_result = claimed_scan(values)
    canonical_result = canonical(list(values))
    candidate_result = candidate(list(values))
    agrees = pair_equal(model_result, canonical_result) and pair_equal(
        model_result, candidate_result
    )
    failures += not agrees
    print(
        f"input={values!r} precondition_len_ge_2={len(values) >= 2} "
        f"claimed_scan={model_result!r} canonical={canonical_result!r} "
        f"candidate={candidate_result!r} agrees={agrees}"
    )

print(f"failures={failures}")
raise SystemExit(1 if failures else 0)
