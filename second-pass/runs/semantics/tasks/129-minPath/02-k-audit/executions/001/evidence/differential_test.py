#!/usr/bin/env python3
"""Independent candidate/canonical differential and small brute-force audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def brute_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate all legal paths; used only on small valid grids."""
    if k == 0:
        return []
    n = len(grid)
    paths = [((r, c), [grid[r][c]]) for r in range(n) for c in range(n)]
    for _ in range(1, k):
        next_paths: list[tuple[tuple[int, int], list[int]]] = []
        for (r, c), values in paths:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    next_paths.append(((nr, nc), values + [grid[nr][nc]]))
        paths = next_paths
    return min(values for _, values in paths)


def branch_observations(grid: list[list[int]]) -> tuple[dict[str, bool], dict[str, bool]]:
    """Record the guard and nested-min branch outcomes of the submitted algorithm."""
    n = len(grid)
    row = column = 0
    for i in range(n):
        for j in range(n):
            if grid[i][j] == 1:
                row, column = i, j
    neighbor = n * n + 1
    guards: dict[str, bool] = {}
    comparisons: dict[str, bool] = {}
    directions = (
        ("up", row > 0, row - 1, column),
        ("down", row + 1 < n, row + 1, column),
        ("left", column > 0, row, column - 1),
        ("right", column + 1 < n, row, column + 1),
    )
    for name, guard, nr, nc in directions:
        guards[name] = guard
        if guard:
            take = grid[nr][nc] < neighbor
            comparisons[name] = take
            if take:
                neighbor = grid[nr][nc]
    return guards, comparisons


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--inputs-out", type=Path, required=True)
    args = parser.parse_args()

    generated = load_entry(args.candidate, "audit_generated_solution")
    canonical = load_entry(args.canonical, "audit_trusted_canonical")
    rng = random.Random(129_2026)

    cases: list[dict[str, object]] = []

    def add(category: str, grid: list[list[int]], k: int, brute: bool = False) -> None:
        cases.append({"category": category, "grid": grid, "k": k, "brute": brute})

    add("documented-example", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, True)
    add("documented-example", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, True)

    # Explicit outside-contract probes: empty grid and non-positive path length.
    add("outside-domain-empty", [], 0)
    add("outside-domain-empty", [], 1)
    add("outside-domain-empty", [], 4)
    add("outside-domain-k-zero", [[1, 2], [3, 4]], 0)

    # Exhaust all valid 2x2 grids and path-length boundaries/repetition cases.
    for perm in itertools.permutations(range(1, 5)):
        grid = [list(perm[:2]), list(perm[2:])]
        for k in (1, 2, 3, 4, 5, 8):
            add("exhaustive-2x2", grid, k, True)

    # Ensure every location class for 1 appears in seeded 3x3 samples.
    for one_pos in range(9):
        rest = [value for value in range(2, 10)]
        for _ in range(20):
            rng.shuffle(rest)
            values = rest.copy()
            values.insert(one_pos, 1)
            grid = [values[0:3], values[3:6], values[6:9]]
            for k in (1, 2, 3, 4, 5, 9, 12):
                add("seeded-3x3", grid, k, k <= 5)

    # Representative larger valid grids.
    for n in (4, 5, 6):
        for _ in range(120):
            values = list(range(1, n * n + 1))
            rng.shuffle(values)
            grid = [values[i * n : (i + 1) * n] for i in range(n)]
            for k in (1, 2, 3, n, n * n, n * n + 3):
                add(f"seeded-{n}x{n}", grid, k)

    args.inputs_out.write_text(json.dumps(cases, sort_keys=True, separators=(",", ":")) + "\n")

    mismatches: list[dict[str, object]] = []
    brute_mismatches: list[dict[str, object]] = []
    guard_seen = {name: set() for name in ("up", "down", "left", "right")}
    comparison_seen = {name: set() for name in ("up", "down", "left", "right")}
    category_counts: dict[str, int] = {}

    for index, case in enumerate(cases):
        category = str(case["category"])
        grid = case["grid"]
        k = int(case["k"])
        assert isinstance(grid, list)
        category_counts[category] = category_counts.get(category, 0) + 1
        expected = canonical(grid, k)
        actual = generated(grid, k)
        if actual != expected:
            mismatches.append(
                {"index": index, "category": category, "grid": grid, "k": k,
                 "canonical": expected, "candidate": actual}
            )
        if bool(case["brute"]):
            brute = brute_min_path(grid, k)
            if expected != brute or actual != brute:
                brute_mismatches.append(
                    {"index": index, "category": category, "grid": grid, "k": k,
                     "brute": brute, "canonical": expected, "candidate": actual}
                )
        if len(grid) >= 2:
            guards, comparisons = branch_observations(grid)
            for name, value in guards.items():
                guard_seen[name].add(value)
            for name, value in comparisons.items():
                comparison_seen[name].add(value)

    input_digest = hashlib.sha256(args.inputs_out.read_bytes()).hexdigest()
    result = {
        "seed": 129_2026,
        "case_count": len(cases),
        "category_counts": dict(sorted(category_counts.items())),
        "candidate_canonical_mismatch_count": len(mismatches),
        "brute_check_count": sum(bool(case["brute"]) for case in cases),
        "brute_mismatch_count": len(brute_mismatches),
        "guard_outcomes_seen": {key: sorted(values) for key, values in guard_seen.items()},
        "nested_min_outcomes_seen": {
            key: sorted(values) for key, values in comparison_seen.items()
        },
        "inputs_sha256": input_digest,
        "first_candidate_canonical_mismatches": mismatches[:5],
        "first_brute_mismatches": brute_mismatches[:5],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 1 if mismatches or brute_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
