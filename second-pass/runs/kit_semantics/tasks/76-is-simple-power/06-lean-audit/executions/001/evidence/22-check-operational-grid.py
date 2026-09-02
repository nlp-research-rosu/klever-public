#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


def tdiv(a: int, b: int) -> int:
    if b == 0:
        return 0
    magnitude = abs(a) // abs(b)
    return -magnitude if (a < 0) != (b < 0) else magnitude


def tmod(a: int, b: int) -> int:
    if b == 0:
        return a
    return a - tdiv(a, b) * b


def py_mod(a: int, b: int) -> int:
    return tmod(tmod(a, b) + b, b)


def simple_power(x: int, n: int) -> bool:
    if x == 1:
        return True
    if n == 0:
        return x == 0
    if n == 1:
        return False
    if n == -1:
        return x == -1
    if x == 0:
        return False
    if py_mod(x, n) == 0:
        return simple_power(tdiv(x, n), n)
    return False


pattern = re.compile(
    r"^GRID,(-?\d+),(-?\d+),(-?\d+),(-?\d+),(true|false)\r?$"
)
records: list[tuple[int, int, int, int, bool]] = []
for line in Path(
    "/audit-output/evidence/21-operational-bridge-grid-lean.txt"
).read_text().splitlines():
    match = pattern.fullmatch(line)
    if match:
        x, n, division, modulo = map(int, match.groups()[:4])
        summary = match.group(5) == "true"
        records.append((x, n, division, modulo, summary))

expected_count = 19 * 9
if len(records) != expected_count:
    raise AssertionError(
        f"expected {expected_count} Lean grid records, got {len(records)}"
    )

mismatches: list[str] = []
for x, n, division, modulo, summary in records:
    expected = (tdiv(x, n), py_mod(x, n), simple_power(x, n))
    observed = (division, modulo, summary)
    if observed != expected:
        mismatches.append(
            f"x={x}, n={n}: observed={observed}, expected={expected}"
        )

print(f"records={len(records)}")
print(f"mismatches={len(mismatches)}")
for mismatch in mismatches:
    print(mismatch)
if mismatches:
    raise SystemExit(1)
