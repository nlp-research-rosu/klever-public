#!/usr/bin/env python3
"""Independent differential and brute-force checks for HumanEval 129."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path
from typing import Any, Callable


ROOT = Path("/tmp/audit-work/129-minPath-audit")


def load_function(path: Path, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def capture(function: Callable[..., Any], *args: Any) -> tuple[str, Any]:
    try:
        return ("value", function(*args))
    except Exception as error:  # Boundary observations include exception type.
        return ("exception", type(error).__name__)


def brute_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate every exactly-k-cell path; independent of both implementations."""
    n = len(grid)
    best: tuple[int, ...] | None = None

    def visit(row: int, col: int, prefix: tuple[int, ...]) -> None:
        nonlocal best
        extended = prefix + (grid[row][col],)
        if best is not None and extended >= best[: len(extended)]:
            return
        if len(extended) == k:
            if best is None or extended < best:
                best = extended
            return
        for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < n and 0 <= new_col < n:
                visit(new_row, new_col, extended)

    for row in range(n):
        for col in range(n):
            visit(row, col, ())
    if best is None:
        raise ValueError("no path")
    return list(best)


def make_grid(n: int, values: tuple[int, ...] | list[int]) -> list[list[int]]:
    return [list(values[row * n : (row + 1) * n]) for row in range(n)]


def main() -> None:
    generated = load_function(ROOT / "solution.py", "audited_solution")
    canonical = load_function(ROOT / "canonical.py", "trusted_canonical")
    intended_cases: list[tuple[str, list[list[int]], int, bool]] = []

    intended_cases.extend([
        ("doc-example-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, True),
        ("doc-example-2", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, True),
    ])

    # Exhaust every valid 2x2 input and several path lengths.
    for permutation in itertools.permutations(range(1, 5)):
        grid = make_grid(2, permutation)
        for k in range(1, 7):
            intended_cases.append((f"exhaustive-n2-{permutation}-k{k}", grid, k, True))

    # Put 1 at every corner, edge, and interior position; exercise all directional guards.
    for one_index in range(9):
        remainder = iter(range(2, 10))
        flat = [1 if index == one_index else next(remainder) for index in range(9)]
        grid = make_grid(3, flat)
        for k in (1, 2, 3, 4, 7, 8):
            intended_cases.append((f"n3-one-position-{one_index}-k{k}", grid, k, k <= 7))

    rng = random.Random(129_20260801)
    for case_number in range(600):
        n = rng.randint(2, 8)
        flat = list(range(1, n * n + 1))
        rng.shuffle(flat)
        k = rng.randint(1, 25)
        use_brute = n <= 3 and k <= 7 and case_number < 200
        intended_cases.append((f"random-{case_number}-n{n}-k{k}", make_grid(n, flat), k, use_brute))

    canonical_mismatches: list[tuple[str, Any, Any]] = []
    brute_mismatches: list[tuple[str, Any, Any]] = []
    brute_checks = 0
    for label, grid, k, use_brute in intended_cases:
        actual = generated(grid, k)
        witness = canonical(grid, k)
        if actual != witness:
            canonical_mismatches.append((label, actual, witness))
        if use_brute:
            brute_checks += 1
            oracle = brute_min_path(grid, k)
            if actual != oracle:
                brute_mismatches.append((label, actual, oracle))

    boundary_cases: list[tuple[str, list[list[int]], int]] = [
        ("empty-grid-positive-k", [], 3),
        ("n1-invalid-by-contract", [[1]], 3),
        ("zero-k-invalid-by-contract", [[1, 2], [3, 4]], 0),
        ("negative-k-invalid-by-contract", [[1, 2], [3, 4]], -1),
        ("duplicate-one-invalid-by-contract", [[1, 1], [2, 3]], 3),
        ("missing-one-invalid-by-contract", [[2, 3], [4, 5]], 3),
        ("ragged-invalid-by-contract", [[1, 2], [3]], 3),
    ]
    print(f"intended_cases={len(intended_cases)}")
    print(f"canonical_mismatches={len(canonical_mismatches)}")
    print(f"canonical_mismatch_details={canonical_mismatches[:10]}")
    print(f"brute_force_checks={brute_checks}")
    print(f"brute_force_mismatches={len(brute_mismatches)}")
    print(f"brute_force_mismatch_details={brute_mismatches[:10]}")
    print("out_of_contract_boundary_observations:")
    for label, grid, k in boundary_cases:
        print(
            f"  {label}: generated={capture(generated, grid, k)!r} "
            f"canonical={capture(canonical, grid, k)!r}"
        )
    if canonical_mismatches or brute_mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
