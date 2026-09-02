#!/usr/bin/env python3
"""Generate deterministic CPython-oracle assertions for the supplied ceil rule."""

from __future__ import annotations

import hashlib
import math
import random
from pathlib import Path


values: list[int | float] = [
    -10**80,
    -10**20,
    -1000,
    -2,
    -1,
    0,
    1,
    2,
    1000,
    10**20,
    10**80,
    -0.0,
    0.0,
    -float.fromhex("0x0.0000000000001p-1022"),
    float.fromhex("0x0.0000000000001p-1022"),
]
for integer in range(-6, 7):
    point = float(integer)
    values.extend(
        [
            math.nextafter(point, -math.inf),
            point,
            math.nextafter(point, math.inf),
        ]
    )
rng = random.Random(133_05_2026)
values.extend(rng.randint(-100000, 100000) / 64.0 for _ in range(24))

# Stable de-duplication that preserves signed zero as separate textual inputs.
seen: set[tuple[str, str]] = set()
unique: list[int | float] = []
for value in values:
    key = (type(value).__name__, repr(value))
    if key not in seen:
        seen.add(key)
        unique.append(value)

source_lines = ["import math", ""]
for index, value in enumerate(unique):
    expected = math.ceil(value)
    source_lines.append(
        f"assert math.ceil({value!r}) == {expected}  # case {index}"
    )
source = "\n".join(source_lines) + "\n"
target = Path("/tmp/audit-work/reconstruction/ceil-bridge.py")
target.write_text(source)
print(f"ceil_bridge_cases={len(unique)}")
print(f"ceil_bridge_source_sha256={hashlib.sha256(source.encode()).hexdigest()}")
print(f"ceil_bridge_source={target}")
