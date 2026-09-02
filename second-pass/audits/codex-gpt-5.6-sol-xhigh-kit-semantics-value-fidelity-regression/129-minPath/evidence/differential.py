#!/usr/bin/env python3
"""Independent canonical-vs-generated and brute-force differential audit."""

from __future__ import annotations

import argparse
import importlib.util
import itertools
import json
import random
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def brute_min_path(grid: list[list[int]], length: int) -> list[int] | None:
    """Definition-level oracle: enumerate all legal walks of exactly length."""
    if length <= 0:
        return []
    size = len(grid)
    best: list[int] | None = None

    def extend(row: int, col: int, path: list[int]) -> None:
        nonlocal best
        if len(path) == length:
            if best is None or path < best:
                best = path
            return
        for dr, dc in ((-1, 0), (0, -1), (0, 1), (1, 0)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < size and 0 <= nc < size:
                extend(nr, nc, path + [grid[nr][nc]])

    for row in range(size):
        for col in range(size):
            extend(row, col, [grid[row][col]])
    return best


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--canonical", type=Path, required=True)
    parser.add_argument("--generated", type=Path, required=True)
    parser.add_argument("--cases-out", type=Path, required=True)
    args = parser.parse_args()

    canonical = load_module("audit_canonical", args.canonical)
    generated = load_module("audit_generated", args.generated)

    cases: list[dict] = []

    def check(
        label: str,
        grid: list[list[int]],
        k: int,
        *,
        intended: bool = True,
        brute: bool = False,
    ) -> None:
        def invoke(function):
            try:
                return {
                    "kind": "return",
                    "value": function([row[:] for row in grid], k),
                }
            except Exception as error:  # deliberately record excluded-domain behavior
                return {
                    "kind": "exception",
                    "type": type(error).__name__,
                    "message": str(error),
                }

        canon = invoke(canonical.minPath)
        actual = invoke(generated.minPath)
        oracle = brute_min_path(grid, k) if brute else None
        record = {
            "label": label,
            "grid": grid,
            "k": k,
            "intended_domain": intended,
            "canonical": canon,
            "generated": actual,
        }
        if brute:
            record["brute_oracle"] = oracle
        cases.append(record)
        if intended and canon != actual:
            raise AssertionError(f"canonical divergence: {record}")
        if (
            brute
            and intended
            and (
                actual["kind"] != "return"
                or actual["value"] != oracle
            )
        ):
            raise AssertionError(f"contract divergence: {record}")

    # The two documented examples.
    check(
        "documented-example-1",
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        3,
        brute=True,
    )
    check(
        "documented-example-2",
        [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
        1,
        brute=True,
    )

    # Exhaust every valid 2x2 grid and both parity boundaries through k=8.
    for permutation in itertools.permutations(range(1, 5)):
        grid = [list(permutation[:2]), list(permutation[2:])]
        for k in range(1, 9):
            check("exhaustive-2x2", grid, k, brute=True)

    # Explicit corner, edge, and interior locations for 1 on 3x3 grids.
    branch_grids = [
        [[1, 9, 8], [7, 6, 5], [4, 3, 2]],  # corner
        [[9, 1, 8], [7, 6, 5], [4, 3, 2]],  # edge
        [[9, 8, 7], [6, 1, 5], [4, 3, 2]],  # interior
        [[9, 8, 7], [6, 5, 4], [3, 2, 1]],  # opposite corner
    ]
    for index, grid in enumerate(branch_grids):
        for k in (1, 2, 3, 4, 9):
            check(f"3x3-position-{index}", grid, k, brute=True)

    # Seeded representative valid permutations at larger N and larger k.
    rng = random.Random(129_20260723)
    for size, samples, lengths in (
        (3, 120, (1, 2, 3, 4, 5, 10)),
        (4, 80, (1, 2, 3, 8, 17)),
        (5, 50, (1, 2, 7, 26)),
        (7, 20, (1, 2, 13, 50)),
    ):
        for sample in range(samples):
            values = list(range(1, size * size + 1))
            rng.shuffle(values)
            grid = [
                values[row * size : (row + 1) * size]
                for row in range(size)
            ]
            for k in lengths:
                # Brute force is intentionally bounded to small paths.
                check(
                    f"seeded-{size}x{size}-{sample}",
                    grid,
                    k,
                    brute=(size <= 3 and k <= 5),
                )

    # Explicitly record empty/boundary behavior outside the intended domain.
    # Agreement here is evidence only; the formal theorem excludes these cases.
    check("excluded-k-zero", [[1, 2], [3, 4]], 0, intended=False)
    check("excluded-empty-grid-k-one", [], 1, intended=False)
    check("excluded-empty-grid-k-two", [], 2, intended=False)
    check("excluded-one-empty-row", [[]], 2, intended=False)

    args.cases_out.write_text(
        json.dumps(cases, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    intended_count = sum(c["intended_domain"] for c in cases)
    brute_count = sum("brute_oracle" in c for c in cases)
    intended_mismatches = sum(
        c["canonical"] != c["generated"]
        for c in cases
        if c["intended_domain"]
    )
    excluded_mismatches = sum(
        c["canonical"] != c["generated"]
        for c in cases
        if not c["intended_domain"]
    )
    print(f"total cases: {len(cases)}")
    print(f"intended-domain cases: {intended_count}")
    print(f"brute-force oracle cases: {brute_count}")
    print(f"canonical/generated intended-domain mismatches: {intended_mismatches}")
    print(f"canonical/generated excluded-domain mismatches: {excluded_mismatches}")
    print("generated/brute mismatches on intended cases: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
