#!/usr/bin/env python3
"""Independent differential test for HumanEval 115 max_fill.

Inputs are generated deterministically below.  The trusted oracle is loaded
from /reference/canonical.py; the submitted implementation is loaded from the
clean scratch copy at /tmp/audit-work/candidate-src/solution.py.
"""

from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import random


def load(path, module_name):
    spec = spec_from_file_location(module_name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


oracle = load("/reference/canonical.py", "trusted_canonical")
candidate = load(
    "/tmp/audit-work/candidate-src/solution.py", "submitted_solution"
)

named_cases = [
    (
        "example-1",
        [[0, 0, 1, 0], [0, 1, 0, 0], [1, 1, 1, 1]],
        1,
    ),
    (
        "example-2",
        [[0, 0, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 1, 1, 1]],
        2,
    ),
    ("example-3", [[0, 0, 0], [0, 0, 0]], 5),
    ("empty-grid-extension", [], 1),
    ("empty-row-extension", [[]], 10),
    ("min-valid", [[0]], 1),
    ("min-valid-one", [[1]], 1),
    ("max-all-zero", [[0] * 100 for _ in range(100)], 10),
    ("max-all-one", [[1] * 100 for _ in range(100)], 10),
]

cases = [(grid, capacity, name) for name, grid, capacity in named_cases]

# Exhaust all binary rows through length six.  For each capacity, check a
# one-row grid, a two-row grid (loop accumulation), and reversed row order.
for row_len in range(1, 7):
    for bits in product((0, 1), repeat=row_len):
        row = list(bits)
        for capacity in range(1, 11):
            cases.append(([row], capacity, "exhaustive-small-single"))
            cases.append(([row, row], capacity, "exhaustive-small-double"))
            cases.append(
                ([row, list(reversed(row))], capacity, "exhaustive-small-order")
            )

# Hit every ceil-division transition s = k*capacity and the adjacent sums
# within representative and maximum row lengths.
for row_len in (1, 2, 9, 10, 11, 99, 100):
    for capacity in range(1, 11):
        sums = {0, 1, row_len}
        for multiple in range(0, row_len + capacity, capacity):
            for delta in (-1, 0, 1):
                if 0 <= multiple + delta <= row_len:
                    sums.add(multiple + delta)
        for water in sorted(sums):
            row = [1] * water + [0] * (row_len - water)
            cases.append(([row], capacity, "ceil-boundary-single"))
            cases.append(
                ([row, [0] * row_len, row], capacity, "ceil-boundary-accumulate")
            )

# Reproducible generated valid inputs across the full documented dimensions.
rng = random.Random(115_20260729)
for _ in range(5000):
    rows = rng.randint(1, 100)
    cols = rng.randint(1, 100)
    capacity = rng.randint(1, 10)
    grid = [
        [rng.randint(0, 1) for _ in range(cols)]
        for _ in range(rows)
    ]
    cases.append((grid, capacity, "seeded-valid-random"))

mismatches = []
named_results = []
for index, (grid, capacity, source) in enumerate(cases):
    expected = oracle.max_fill(grid, capacity)
    actual = candidate.max_fill(grid, capacity)
    if source.startswith(("example", "empty", "min-", "max-")):
        named_results.append((source, expected, actual))
    if expected != actual:
        mismatches.append(
            {
                "index": index,
                "source": source,
                "grid": grid,
                "capacity": capacity,
                "expected": expected,
                "actual": actual,
            }
        )
        if len(mismatches) >= 20:
            break

print("ORACLE=/reference/canonical.py:max_fill")
print("CANDIDATE=/tmp/audit-work/candidate-src/solution.py:max_fill")
print("SEED=11520260729")
print(
    "SCOPE=3 prompt examples; empty extensions; min/max documented bounds; "
    "all binary rows of lengths 1..6 at capacities 1..10 in three grid "
    "contexts; ceil boundaries for row lengths 1,2,9,10,11,99,100; "
    "5000 seeded valid grids with rows/cols 1..100 and capacity 1..10"
)
for result in named_results:
    print("NAMED_RESULT", result)
print(f"CASES={len(cases)}")
print(f"MISMATCHES={len(mismatches)}")
for mismatch in mismatches:
    print("MISMATCH", mismatch)

raise SystemExit(1 if mismatches else 0)
