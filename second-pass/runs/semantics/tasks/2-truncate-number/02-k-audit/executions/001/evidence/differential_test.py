#!/usr/bin/env python3
"""Independent fidelity checks for HumanEval problem 2.

The canonical and generated modules are loaded from distinct trusted/candidate
paths.  The decimal-part oracle uses math.modf rather than the submitted `%`
expression.  All randomized inputs are deterministic and printed.
"""

from __future__ import annotations

import importlib.util
import math
import random
import struct
import sys
from pathlib import Path
from typing import Callable


def load_function(path: Path, module_name: str) -> Callable[[float], float]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.truncate_number


def same_float(left: float, right: float) -> bool:
    if math.isnan(left) and math.isnan(right):
        return True
    return struct.pack(">d", left) == struct.pack(">d", right)


def observed(function: Callable[[float], float], value: float) -> tuple[str, object]:
    try:
        return ("value", function(value))
    except BaseException as error:  # evidence records the exact terminating behavior
        return ("exception", (type(error).__name__, str(error)))


def same_outcome(left: tuple[str, object], right: tuple[str, object]) -> bool:
    if left[0] != right[0]:
        return False
    if left[0] == "exception":
        return left[1] == right[1]
    return same_float(float(left[1]), float(right[1]))


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(Path("/candidate/solution.py"), "candidate_generated")

documented_and_boundaries = [
    3.5,
    math.nextafter(0.0, 1.0),
    sys.float_info.min,
    math.nextafter(1.0, 0.0),
    1.0,
    math.nextafter(1.0, math.inf),
    math.nextafter(2.0, 0.0),
    2.0,
    math.nextafter(2.0, math.inf),
    math.nextafter(3.0, 0.0),
    3.0,
    math.nextafter(3.0, math.inf),
    10.25,
    math.nextafter(10.0, 0.0),
    10.0,
    math.nextafter(10.0, math.inf),
    math.nextafter(float(2**52), 0.0),
    float(2**52),
    math.nextafter(float(2**52), math.inf),
    sys.float_info.max,
]

rng = random.Random(0x2_7A11_CAFE)
generated_inputs: list[float] = []
while len(generated_inputs) < 256:
    exponent = rng.randint(-1073, 1023)
    significand = 0.5 + rng.random() * 0.5
    try:
        value = math.ldexp(significand, exponent)
    except OverflowError:
        continue
    if math.isfinite(value) and value > 0.0:
        generated_inputs.append(value)

seen: set[str] = set()
intended_inputs: list[float] = []
for item in documented_and_boundaries + generated_inputs:
    key = item.hex()
    if key not in seen:
        seen.add(key)
        intended_inputs.append(item)

mismatches = 0
oracle_mismatches = 0
print(f"INTENDED_INPUT_COUNT={len(intended_inputs)}")
for index, value in enumerate(intended_inputs):
    left = observed(canonical, value)
    right = observed(generated, value)
    oracle = math.modf(value)[0]
    agrees = same_outcome(left, right)
    oracle_agrees = (
        left[0] == "value"
        and same_float(float(left[1]), oracle)
        and right[0] == "value"
        and same_float(float(right[1]), oracle)
    )
    mismatches += int(not agrees)
    oracle_mismatches += int(not oracle_agrees)
    print(
        f"IN[{index:03d}]={value.hex()} "
        f"canonical={left!r} generated={right!r} "
        f"modf_oracle={oracle.hex()} agree={agrees} oracle_agree={oracle_agrees}"
    )

print("OUT_OF_DOMAIN_DIAGNOSTICS")
for value in [-3.5, -1.0, -0.0, 0.0, math.inf, -math.inf, math.nan]:
    left = observed(canonical, value)
    right = observed(generated, value)
    agrees = same_outcome(left, right)
    mismatches += int(not agrees)
    print(
        f"OUT={value!r} canonical={left!r} generated={right!r} agree={agrees}"
    )

try:
    canonical_empty = ("value", canonical())  # type: ignore[call-arg]
except BaseException as error:
    canonical_empty = ("exception", (type(error).__name__, str(error)))
try:
    generated_empty = ("value", generated())  # type: ignore[call-arg]
except BaseException as error:
    generated_empty = ("exception", (type(error).__name__, str(error)))
empty_agrees = canonical_empty == generated_empty
mismatches += int(not empty_agrees)
print(
    "EMPTY_CALL "
    f"canonical={canonical_empty!r} generated={generated_empty!r} agree={empty_agrees}"
)

print(f"CANONICAL_GENERATED_MISMATCHES={mismatches}")
print(f"IN_DOMAIN_ORACLE_MISMATCHES={oracle_mismatches}")
raise SystemExit(0 if mismatches == 0 and oracle_mismatches == 0 else 1)
