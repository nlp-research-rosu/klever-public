#!/usr/bin/env python3
"""Independent CPython differential test for trusted canonical vs candidate source."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import Any, Callable


WORK = Path("/tmp/audit-work")


def load_entry(module_name: str, path: Path) -> Callable[[list[int]], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.unique_digits


canonical = load_entry("trusted_canonical", WORK / "canonical.py")
candidate = load_entry("generated_candidate", WORK / "solution.py")

# Prompt examples; empty/singleton/list behavior; each even-digit rejection
# boundary at the first, middle, and last decimal position; accepted all-odd
# values; sorting and duplicate preservation; and large positive integers.
documented_and_boundary_cases: list[list[int]] = [
    [15, 33, 1422, 1],
    [152, 323, 1422, 10],
    [],
    [1],
    [2],
    [0],  # explicit lower-bound probe (outside positive-integer contract)
    [10, 101, 110],
    [20, 121, 112],
    [40, 141, 114],
    [60, 161, 116],
    [80, 181, 118],
    [3, 5, 7, 9, 11, 13, 15, 31, 99, 111, 97531],
    [222, 135, 55, 15, 135, 3, 8642, 1],
    [9999999999999999999999999999999999999999],
    [9999999999999999999999999999999999999998],
]

cases: list[list[int]] = list(documented_and_boundary_cases)

# Exhaustive singleton coverage through four decimal digits exercises every
# digit and every rejection position.
cases.extend([[value] for value in range(1, 10_001)])

# Deterministically generated lists exercise combinations, order, duplicates,
# sorting, and long values. The seed and generator are the preserved inputs.
rng = random.Random(104_20260723)
for _ in range(2_000):
    length = rng.randrange(0, 21)
    values = [rng.randrange(1, 10**18) for _ in range(length)]
    if values and rng.random() < 0.25:
        values.append(values[rng.randrange(len(values))])
    cases.append(values)

mismatches: list[tuple[int, list[int], Any, Any]] = []
for index, values in enumerate(cases):
    expected = canonical(values)
    actual = candidate(values)
    if expected != actual:
        mismatches.append((index, values, expected, actual))
        if len(mismatches) >= 10:
            break

print("ORACLE=trusted /reference/canonical.py copied byte-for-byte to scratch")
print("GENERATED=/candidate/solution.py copied byte-for-byte to scratch")
print(
    "INPUT_SCOPE=15 explicit cases (including 2 prompt examples and zero probe); "
    "singletons 1..10000; 2000 seed-104_20260723 generated lists"
)
print(f"TOTAL_CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches:
    print(f"MISMATCH={mismatch!r}")

# Preserve a deliberately excluded-domain observation. It does not count as an
# intended-domain mismatch, but makes the positive-integer restriction visible.
try:
    canonical_negative: Any = canonical([-1])
except Exception as error:  # noqa: BLE001 - evidence records exact behavior.
    canonical_negative = f"{type(error).__name__}: {error}"
try:
    candidate_negative: Any = candidate([-1])
except Exception as error:  # noqa: BLE001
    candidate_negative = f"{type(error).__name__}: {error}"
print(f"EXCLUDED_INPUT=[-1] CANONICAL={canonical_negative!r} CANDIDATE={candidate_negative!r}")

raise SystemExit(1 if mismatches else 0)
