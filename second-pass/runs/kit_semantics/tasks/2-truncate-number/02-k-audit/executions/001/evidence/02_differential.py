#!/usr/bin/env python3
"""Independent differential test of candidate and trusted canonical entry points."""

from __future__ import annotations

import importlib.util
import math
import random
import struct
from pathlib import Path


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


def generated_positive_finite(rng: random.Random, count: int) -> list[float]:
    values: list[float] = []
    while len(values) < count:
        bits = rng.getrandbits(64)
        value = struct.unpack(">d", bits.to_bytes(8, "big"))[0]
        if value > 0.0 and math.isfinite(value):
            values.append(value)
    return values


def main() -> int:
    canonical = load_function("trusted_canonical", Path("/tmp/audit-work/canonical.py"))
    candidate = load_function(
        "audited_candidate", Path("/tmp/audit-work/candidate/solution.py")
    )

    documented = [3.5]
    boundary = [
        0.0,  # adjacent to, but outside, the strictly positive contract
        math.nextafter(0.0, math.inf),
        math.nextafter(1.0, 0.0),
        1.0,
        math.nextafter(1.0, math.inf),
        math.nextafter(2.0, 0.0),
        2.0,
        math.nextafter(2.0, math.inf),
        2.0**52 - 0.5,
        2.0**52,
        float.fromhex("0x1.fffffffffffffp+1023"),
    ]
    representative = [
        0.125,
        0.5,
        0.75,
        10.25,
        123.875,
        1.0e-300,
        1.0e300,
    ]
    grid = [
        whole + numerator / 16.0
        for whole in range(0, 129)
        for numerator in range(0, 16)
    ]
    random_values = generated_positive_finite(random.Random(20260725), 10000)
    inputs = documented + boundary + representative + grid + random_values

    mismatches: list[tuple[float, object, object]] = []
    for value in inputs:
        expected = canonical(value)
        actual = candidate(value)
        if actual != expected or (
            isinstance(actual, float)
            and isinstance(expected, float)
            and math.copysign(1.0, actual) != math.copysign(1.0, expected)
        ):
            mismatches.append((value, actual, expected))

    print("contract_domain=positive finite Python floats")
    print("empty_case=not applicable: scalar numeric input")
    print("branch_boundaries=not applicable: implementation has no branches")
    print(f"documented_inputs={documented!r}")
    print(f"boundary_inputs={boundary!r}")
    print(f"representative_inputs={representative!r}")
    print(f"grid_inputs={len(grid)}")
    print("random_input_seed=20260725")
    print(f"random_positive_finite_inputs={len(random_values)}")
    print(f"total_inputs={len(inputs)} mismatches={len(mismatches)}")
    if mismatches:
        print(f"first_mismatches={mismatches[:20]!r}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
