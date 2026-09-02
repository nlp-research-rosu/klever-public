#!/usr/bin/env python3
"""Generate deterministic end-to-end K-vs-Python sorted/slice assertions."""

from __future__ import annotations

import random


rng = random.Random(120_777)
cases: list[tuple[list[int], int]] = [
    ([-3, -4, 5], 3),
    ([4, -4, 4], 2),
    ([-3, 2, 1, 2, -1, -2, 1], 1),
    ([1, 2, 3], 0),
    ([-1000], 1),
    ([1000], 0),
    ([-1000, 1000], 1),
    ([-1000, 1000], 2),
]
for _ in range(8):
    n = rng.randint(1, 5)
    arr = [rng.randint(-1000, 1000) for _ in range(n)]
    k = rng.choice([0, 1, n // 2, n])
    cases.append((arr, k))

print("def maximum(arr, k):")
print("    if k == 0:")
print("        return []")
print("    return sorted(arr)[-k:]")
print()
for arr, k in cases:
    expected = [] if k == 0 else sorted(arr)[len(arr) - k :]
    print(f"assert maximum({arr!r}, {k}) == {expected!r}")
