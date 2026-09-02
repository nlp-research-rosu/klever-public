#!/usr/bin/env python3
"""Independent differential and small-case brute-force check for minPath."""

from __future__ import annotations

import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable


CANONICAL_PATH = Path("/reference/canonical.py")
GENERATED_PATH = Path("/tmp/audit-work/129-minpath/solution.py")
CASES_PATH = Path("/audit-output/evidence/artifacts/differential_cases.json")


def load_entry(path: Path, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


canonical = load_entry(CANONICAL_PATH, "trusted_canonical_minpath")
generated = load_entry(GENERATED_PATH, "generated_minpath")


def brute_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate every length-k path; intentionally independent of both functions."""
    n = len(grid)
    if n == 0 or k <= 0:
        return []
    prefixes = [([grid[row][col]], row, col) for row in range(n) for col in range(n)]
    for _ in range(1, k):
        extended: list[tuple[list[int], int, int]] = []
        for values, row, col in prefixes:
            for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                next_row, next_col = row + drow, col + dcol
                if 0 <= next_row < n and 0 <= next_col < n:
                    extended.append(
                        (values + [grid[next_row][next_col]], next_row, next_col)
                    )
        prefixes = extended
    return min(values for values, _, _ in prefixes)


def outcome(function: Callable[..., Any], grid: list[list[int]], k: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function([row[:] for row in grid], k)}
    except Exception as error:  # audit records exception behavior outside the domain
        return {"kind": "exception", "type": type(error).__name__, "message": str(error)}


cases: list[dict[str, Any]] = []


def add(label: str, grid: list[list[int]], k: int, intended: bool, brute: bool) -> None:
    cases.append(
        {"label": label, "grid": grid, "k": k, "intended_domain": intended, "brute": brute}
    )


# Prompt examples.
add("prompt-example-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, True, True)
add("prompt-example-2", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, True, True)

# Empty/boundary probes. k=0, N<2, and empty grids are explicitly outside the contract.
add("outside-empty-k0", [], 0, False, False)
add("outside-empty-k1", [], 1, False, False)
add("outside-n1-k1", [[1]], 1, False, False)
add("outside-n1-k2", [[1]], 2, False, False)
add("outside-valid-grid-k0", [[1, 2], [3, 4]], 0, False, False)

# Exhaust every 2x2 permutation and k=1..8. This covers every corner position of 1.
for permutation in itertools.permutations(range(1, 5)):
    grid = [list(permutation[:2]), list(permutation[2:])]
    for k in range(1, 9):
        add("all-2x2", grid, k, True, k <= 6)

# Force 1 into every 3x3 position; this exercises each row/column branch boundary.
rng = random.Random(12920260722)
for one_index in range(9):
    rest = list(range(2, 10))
    rng.shuffle(rest)
    values = rest[:]
    values.insert(one_index, 1)
    grid = [values[offset : offset + 3] for offset in range(0, 9, 3)]
    for k in (1, 2, 3, 4, 7):
        add(f"3x3-one-at-{one_index}", grid, k, True, k <= 4)

# Force 1 into every 4x4 position, including all corners, edges, and interiors.
for one_index in range(16):
    rest = list(range(2, 17))
    rng.shuffle(rest)
    values = rest[:]
    values.insert(one_index, 1)
    grid = [values[offset : offset + 4] for offset in range(0, 16, 4)]
    for k in (1, 2, 3, 4, 7, 12):
        add(f"4x4-one-at-{one_index}", grid, k, True, False)

# Deterministic broader generated sample on N=3..7 and both odd/even k.
for sample in range(250):
    n = rng.randint(3, 7)
    values = list(range(1, n * n + 1))
    rng.shuffle(values)
    grid = [values[offset : offset + n] for offset in range(0, n * n, n)]
    for k in (1, 2, 3, 6, 11):
        add(f"generated-{sample}-n{n}", grid, k, True, False)

CASES_PATH.write_text(json.dumps(cases, indent=2) + "\n", encoding="utf-8")

intended_mismatches: list[dict[str, Any]] = []
brute_mismatches: list[dict[str, Any]] = []
outside_observations: list[dict[str, Any]] = []
brute_checks = 0
for index, case in enumerate(cases):
    grid, k = case["grid"], case["k"]
    canonical_result = outcome(canonical, grid, k)
    generated_result = outcome(generated, grid, k)
    if case["intended_domain"] and canonical_result != generated_result:
        intended_mismatches.append(
            {"index": index, "case": case, "canonical": canonical_result, "generated": generated_result}
        )
    if case["brute"]:
        brute_checks += 1
        brute_result = {"kind": "return", "value": brute_min_path(grid, k)}
        if canonical_result != brute_result or generated_result != brute_result:
            brute_mismatches.append(
                {
                    "index": index,
                    "case": case,
                    "canonical": canonical_result,
                    "generated": generated_result,
                    "brute": brute_result,
                }
            )
    if not case["intended_domain"]:
        outside_observations.append(
            {"index": index, "case": case, "canonical": canonical_result, "generated": generated_result}
        )

print(f"seed=12920260722")
print(f"case_file={CASES_PATH}")
print(f"total_cases={len(cases)}")
print(f"intended_cases={sum(bool(case['intended_domain']) for case in cases)}")
print(f"brute_force_checks={brute_checks}")
print(f"intended_canonical_generated_mismatches={len(intended_mismatches)}")
print(f"brute_oracle_mismatches={len(brute_mismatches)}")
print("outside_domain_observations=" + json.dumps(outside_observations, sort_keys=True))

if intended_mismatches or brute_mismatches:
    print("intended_mismatch_details=" + json.dumps(intended_mismatches[:20], sort_keys=True))
    print("brute_mismatch_details=" + json.dumps(brute_mismatches[:20], sort_keys=True))
    sys.exit(1)
