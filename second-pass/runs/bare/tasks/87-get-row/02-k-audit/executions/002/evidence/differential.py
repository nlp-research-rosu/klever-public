#!/usr/bin/env python3
"""Independent differential tests for trusted and generated get_row."""

from __future__ import annotations

import importlib.util
from itertools import product
from pathlib import Path
import random


ROOT = Path("/tmp/audit-work/87-get-row-review")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", ROOT / "trusted_canonical.py").get_row
generated = load("generated_solution", ROOT / "solution.py").get_row


documented_and_boundary = [
    (
        [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]],
        1,
    ),
    ([], 1),
    ([[], [1], [1, 2, 3]], 3),
    ([[]], 0),
    ([[], [], []], -1),
    ([[0]], 0),
    ([[0]], 1),
    ([[1, 0]], 1),
    ([[1, 0]], 0),
    ([[1, 0, 1]], 1),
    ([[1, 1, 1]], 1),
    ([[1, 2], [], [2, 1, 2], [1]], 2),
    ([[-1, 0, -1], [], [-1]], -1),
]


def check(rows, key, label):
    got = generated(rows, key)
    want = canonical(rows, key)
    if got != want:
        raise AssertionError(
            f"{label}: rows={rows!r} key={key!r} generated={got!r} canonical={want!r}"
        )


def all_rows(values=(-1, 0, 1), max_len=3):
    yield []
    for length in range(1, max_len + 1):
        for cells in product(values, repeat=length):
            yield list(cells)


def main() -> None:
    checks = 0
    for index, (rows, key) in enumerate(documented_and_boundary):
        check(rows, key, f"direct-{index}")
        checks += 1
    print(f"documented_and_boundary_cases={checks}")

    row_space = list(all_rows())
    exhaustive = 0
    for row_count in range(3):
        for rows_tuple in product(row_space, repeat=row_count):
            rows = [list(row) for row in rows_tuple]
            for key in (-1, 0, 1):
                check(rows, key, "exhaustive-small")
                exhaustive += 1
    print(
        "exhaustive_small_cases="
        f"{exhaustive} values=[-1,0,1] rows=0..2 row_length=0..3"
    )

    rng = random.Random(870087)
    randomized = 2000
    for _ in range(randomized):
        rows = [
            [rng.randint(-20, 20) for _ in range(rng.randrange(0, 13))]
            for _ in range(rng.randrange(0, 13))
        ]
        key = rng.randint(-20, 20)
        check(rows, key, "random")
    print(
        f"random_cases={randomized} seed=870087 rows=0..12 row_length=0..12 "
        "cell_and_key_range=-20..20"
    )
    print("mismatches=0")


if __name__ == "__main__":
    main()
