#!/usr/bin/env python3
"""Evaluate concrete instances of the K claim's fold-shaped postcondition."""

from __future__ import annotations

import importlib.util
import math
import struct
from pathlib import Path
from typing import Callable


def load(path: Path, name: str) -> Callable[[list[float]], float]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.mean_absolute_deviation


def bits(value: float) -> str:
    if math.isnan(value):
        return "nan"
    return struct.pack(">d", value).hex()


def claimed_fold(values: list[float]) -> float:
    # Concrete interpretation of:
    # divFloatIntV(absDeviationFold(VS,
    #   divFloatIntV(sumFloatSeq(VS), vsLen(VS)), 0.0), vsLen(VS))
    accumulator = 0.0 + values[0]
    for value in values[1:]:
        accumulator = accumulator + value
    mean = accumulator / len(values)
    total_deviation = 0.0
    for value in values:
        total_deviation = total_deviation + abs(value - mean)
    return total_deviation / len(values)


canonical = load(
    Path("/tmp/audit-work/4mad-review/trusted-source/canonical.py"), "ground_canonical"
)
candidate = load(
    Path("/tmp/audit-work/4mad-review/candidate-source/solution.py"), "ground_candidate"
)

cases = [
    [1.0, 2.0, 3.0, 4.0],
    [-1.0, 1.0],
    [7.25],
]

for values in cases:
    precondition = bool(values) and all(type(value) is float for value in values)
    claim_value = claimed_fold(values)
    canonical_value = canonical(values.copy())
    candidate_value = candidate(values.copy())
    print(
        f"input={values!r} precondition={precondition} "
        f"claim_bits={bits(claim_value)} "
        f"canonical_bits={bits(canonical_value)} "
        f"candidate_bits={bits(candidate_value)}"
    )
    if not precondition or not (
        bits(claim_value) == bits(canonical_value) == bits(candidate_value)
    ):
        raise SystemExit(1)

raise SystemExit(0)
