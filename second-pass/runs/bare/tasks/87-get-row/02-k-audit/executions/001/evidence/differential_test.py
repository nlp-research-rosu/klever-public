#!/usr/bin/env python3
"""Independent differential check for HumanEval 87-get-row.

Oracle: /reference/canonical.py.
Candidate implementation: /tmp/audit-work/87-get-row/source/solution.py.

The exhaustive scope contains every ragged integer matrix with 0..3 rows,
each row of length 0..3, elements from {-1, 0, 1}, and x in
{-2, -1, 0, 1, 2}. Random cases extend lengths and integer values.
"""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_entry(
    Path("/tmp/audit-work/87-get-row/source/solution.py"), "audited_candidate"
)

documented_and_boundary_cases = [
    (
        [
            [1, 2, 3, 4, 5, 6],
            [1, 2, 3, 4, 1, 6],
            [1, 2, 3, 4, 5, 1],
        ],
        1,
    ),
    ([], 1),
    ([[], [1], [1, 2, 3]], 3),
    ([[]], 0),
    ([[0]], 0),
    ([[0]], 1),
    ([[1, 0]], 0),
    ([[0, 1]], 0),
    ([[0, 0]], 0),
    ([[0, 1, 0], [], [0]], 0),
    ([[-2, -1, 0], [1, -1]], -1),
]

mismatches = []
case_count = 0
digest = hashlib.sha256()


def check(matrix, x, source):
    global case_count
    case_count += 1
    expected = canonical(matrix, x)
    actual = candidate(matrix, x)
    encoded = json.dumps(
        [matrix, x, expected, actual],
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    digest.update(encoded)
    if actual != expected:
        mismatches.append(
            {
                "source": source,
                "matrix": matrix,
                "x": x,
                "canonical": expected,
                "candidate": actual,
            }
        )


for matrix, x in documented_and_boundary_cases:
    check(matrix, x, "documented-or-boundary")

values = (-1, 0, 1)
rows = [list(items) for n in range(4) for items in itertools.product(values, repeat=n)]
for nrows in range(4):
    for row_tuple in itertools.product(rows, repeat=nrows):
        matrix = [list(row) for row in row_tuple]
        for x in (-2, -1, 0, 1, 2):
            check(matrix, x, "exhaustive-small")

rng = random.Random(870087)
for _ in range(3000):
    matrix = [
        [rng.randint(-7, 7) for _ in range(rng.randint(0, 8))]
        for _ in range(rng.randint(0, 8))
    ]
    x = rng.randint(-9, 9)
    check(matrix, x, "random-seed-870087")

summary = {
    "documented_and_boundary": len(documented_and_boundary_cases),
    "exhaustive_matrices": sum(len(rows) ** n for n in range(4)),
    "exhaustive_x_values": 5,
    "random_cases": 3000,
    "total_cases": case_count,
    "mismatch_count": len(mismatches),
    "result_digest_sha256": digest.hexdigest(),
}
print(json.dumps(summary, indent=2, sort_keys=True))
if mismatches:
    print(json.dumps(mismatches[:20], indent=2, sort_keys=True))
    raise SystemExit(1)
