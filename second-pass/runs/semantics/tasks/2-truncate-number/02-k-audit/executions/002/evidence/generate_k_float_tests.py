#!/usr/bin/env python3
"""Generate deterministic concrete .mpy-facing tests of K floatMod vs CPython."""

from __future__ import annotations

import math
import random
import struct


cases = [
    math.nextafter(0.0, math.inf),
    0.25,
    0.5,
    math.nextafter(1.0, 0.0),
    1.0,
    math.nextafter(1.0, math.inf),
    1.5,
    math.nextafter(2.0, 0.0),
    2.0,
    math.nextafter(2.0, math.inf),
    3.5,
    7.75,
    math.nextafter(float(2**52), 0.0),
    float(2**52),
    float(2**53),
    math.nextafter(float.fromhex("0x1.fffffffffffffp+1023"), 0.0),
    float.fromhex("0x1.fffffffffffffp+1023"),
]

rng = random.Random(0xF10A72)
while len(cases) < 273:
    bits = rng.getrandbits(64)
    value = struct.unpack(">d", bits.to_bytes(8, "big"))[0]
    if math.isfinite(value) and value > 0.0:
        cases.append(value)

print("def truncate_number(number: float) -> float:")
print("    return number % 1.0")
print()
for index, value in enumerate(cases):
    expected = value % 1.0
    print(
        f"assert truncate_number({value!r}) == {expected!r}"
        f"  # case {index}: {value.hex()} -> {expected.hex()}"
    )
