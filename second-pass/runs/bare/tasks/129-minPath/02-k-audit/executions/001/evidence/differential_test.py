#!/usr/bin/env python3
"""Independent differential and contract-oracle checks for HumanEval 129."""

from __future__ import annotations

import importlib.util
import itertools
import random
from collections.abc import Callable
from pathlib import Path
from typing import Any


def load_function(path: Path, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def oracle_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Lexicographic dynamic programming, independent of either implementation."""
    n = len(grid)
    best_ending_at = {
        (row, column): [grid[row][column]]
        for row in range(n)
        for column in range(n)
    }
    for _ in range(1, k):
        next_best: dict[tuple[int, int], list[int]] = {}
        for row in range(n):
            for column in range(n):
                incoming: list[list[int]] = []
                for delta_row, delta_column in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    source = (row + delta_row, column + delta_column)
                    if source in best_ending_at:
                        incoming.append(best_ending_at[source] + [grid[row][column]])
                next_best[(row, column)] = min(incoming)
        best_ending_at = next_best
    return min(best_ending_at.values())


def outcome(function: Callable[..., Any], grid: list[list[int]], k: int) -> tuple[Any, ...]:
    try:
        return ("return", function([row[:] for row in grid], k))
    except Exception as error:  # Invalid-input probes deliberately observe exceptions.
        return ("exception", type(error).__name__, str(error))


def main() -> int:
    trusted = load_function(Path("/tmp/audit-work/reference/canonical.py"), "trusted_canonical")
    generated = load_function(
        Path("/tmp/audit-work/candidate-src/solution.py"), "candidate_generated"
    )

    valid_cases: list[tuple[str, list[list[int]], int]] = [
        ("prompt-example-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3),
        ("prompt-example-2", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1),
        ("long-alternation", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 25),
    ]

    for cells in itertools.permutations(range(1, 5)):
        grid = [list(cells[:2]), list(cells[2:])]
        for k in range(1, 10):
            valid_cases.append(("exhaustive-2x2", grid, k))

    branch_positions: list[tuple[int, int]] = []
    for one_index in range(9):
        remaining = iter(range(2, 10))
        cells = [1 if index == one_index else next(remaining) for index in range(9)]
        grid = [cells[0:3], cells[3:6], cells[6:9]]
        branch_positions.append(divmod(one_index, 3))
        for k in (1, 2, 3, 8):
            valid_cases.append(("all-1-positions-3x3", grid, k))

    rng = random.Random(129_2026)
    generated_counts: dict[int, int] = {}
    for n, count in ((3, 250), (4, 250), (5, 100)):
        generated_counts[n] = count
        for _ in range(count):
            cells = list(range(1, n * n + 1))
            rng.shuffle(cells)
            grid = [cells[row * n : (row + 1) * n] for row in range(n)]
            valid_cases.append((f"generated-{n}x{n}", grid, rng.randint(1, 18)))

    valid_mismatches: list[tuple[Any, ...]] = []
    category_counts: dict[str, int] = {}
    for category, grid, k in valid_cases:
        category_counts[category] = category_counts.get(category, 0) + 1
        trusted_result = trusted([row[:] for row in grid], k)
        generated_result = generated([row[:] for row in grid], k)
        oracle_result = oracle_min_path(grid, k)
        if trusted_result != generated_result or trusted_result != oracle_result:
            valid_mismatches.append(
                (category, grid, k, trusted_result, generated_result, oracle_result)
            )

    expected_examples = [
        (valid_cases[0], [1, 2, 1]),
        (valid_cases[1], [1]),
    ]
    example_failures = []
    for (_, grid, k), expected in expected_examples:
        actual = generated([row[:] for row in grid], k)
        if actual != expected:
            example_failures.append((grid, k, expected, actual))

    invalid_or_out_of_domain = [
        ("zero-length", [[1, 2], [3, 4]], 0),
        ("negative-length", [[1, 2], [3, 4]], -1),
        ("empty-grid", [], 1),
        ("n-equals-one", [[1]], 1),
    ]
    print("VALID_DOMAIN=N>=2 square permutations of 1..N^2; k>=1")
    print(f"VALID_CASES={len(valid_cases)}")
    print(f"CATEGORY_COUNTS={category_counts}")
    print(f"GENERATED_COUNTS={generated_counts}")
    print(f"BRANCH_POSITIONS_FOR_VALUE_1={branch_positions}")
    print(f"VALID_MISMATCHES={len(valid_mismatches)}")
    if valid_mismatches:
        for mismatch in valid_mismatches[:10]:
            print("MISMATCH", mismatch)
    print(f"EXAMPLE_FAILURES={example_failures}")
    print("OUT_OF_DOMAIN_OBSERVATIONS")
    for label, grid, k in invalid_or_out_of_domain:
        print(label, "canonical=", outcome(trusted, grid, k), "generated=", outcome(generated, grid, k))

    return 0 if not valid_mismatches and not example_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
