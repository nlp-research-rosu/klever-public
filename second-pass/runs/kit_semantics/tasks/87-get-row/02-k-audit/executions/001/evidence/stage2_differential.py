#!/usr/bin/env python3
"""Independent differential audit for HumanEval 87 get_row."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Callable


TRUSTED = Path("/reference/canonical.py")
GENERATED = Path("/tmp/audit-work/src/solution.py")


def load_entry(path: Path, module_name: str) -> Callable[[list[list[int]], int], list]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.get_row


def independent_contract_oracle(lst: list[list[int]], x: int) -> list[tuple[int, int]]:
    result = [
        (row_index, column_index)
        for row_index, row in enumerate(lst)
        for column_index, value in enumerate(row)
        if value == x
    ]
    return sorted(result, key=lambda coordinate: (coordinate[0], -coordinate[1]))


def row_space(max_length: int, values: tuple[int, ...]):
    for length in range(max_length + 1):
        for row in itertools.product(values, repeat=length):
            yield list(row)


def run_case(
    case_name: str,
    lst: list[list[int]],
    x: int,
    canonical: Callable,
    generated: Callable,
) -> None:
    expected = canonical(lst, x)
    actual = generated(lst, x)
    contract = independent_contract_oracle(lst, x)
    if expected != contract or actual != expected:
        raise AssertionError(
            f"{case_name}: lst={lst!r}, x={x!r}, canonical={expected!r}, "
            f"generated={actual!r}, contract={contract!r}"
        )


def main() -> None:
    canonical = load_entry(TRUSTED, "audit_trusted_canonical")
    generated = load_entry(GENERATED, "audit_generated_solution")
    count = 0

    documented = [
        (
            [[1, 2, 3, 4, 5, 6], [1, 2, 3, 4, 1, 6], [1, 2, 3, 4, 5, 1]],
            1,
        ),
        ([], 1),
        ([[], [1], [1, 2, 3]], 3),
    ]
    boundaries = [
        ([[]], 0),
        ([[0]], 0),
        ([[0]], 1),
        ([[1, 1, 1]], 1),
        ([[1, 0, 1, 0, 1]], 1),
        ([[1], [], [1, 1], []], 1),
        ([[-1, 0, -1], [0, -1], [-1]], -1),
        ([[10**80, -(10**80)]], 10**80),
        ([[2, 1, 2], [2], [1, 2, 1, 2]], 2),
    ]
    for index, (lst, x) in enumerate(documented):
        run_case(f"documented-{index}", lst, x, canonical, generated)
        count += 1
    for index, (lst, x) in enumerate(boundaries):
        run_case(f"boundary-{index}", lst, x, canonical, generated)
        count += 1

    rows = list(row_space(3, (-1, 0, 1)))
    exhaustive_count = 0
    for row_count in range(3):
        for matrix_tuple in itertools.product(rows, repeat=row_count):
            matrix = [list(row) for row in matrix_tuple]
            for x in (-1, 0, 1, 2):
                run_case(
                    f"exhaustive-{exhaustive_count}",
                    matrix,
                    x,
                    canonical,
                    generated,
                )
                exhaustive_count += 1
                count += 1

    rng = random.Random(870087)
    generated_count = 5000
    for index in range(generated_count):
        row_count = rng.randrange(0, 9)
        matrix = [
            [rng.randrange(-5, 6) for _ in range(rng.randrange(0, 10))]
            for _ in range(row_count)
        ]
        x = rng.randrange(-7, 8)
        run_case(f"generated-{index}", matrix, x, canonical, generated)
        count += 1

    print(f"documented_cases={len(documented)}")
    print(f"boundary_cases={len(boundaries)}")
    print(f"exhaustive_cases={exhaustive_count}")
    print(f"generated_cases={generated_count}")
    print(f"total_cases={count}")
    print("mismatches=0")


if __name__ == "__main__":
    main()
