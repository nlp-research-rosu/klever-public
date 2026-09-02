#!/usr/bin/env python3
"""Independent stage-2 differential and small-domain contract oracle."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import itertools
import json
import random
from pathlib import Path
from typing import Any, Callable


def load_entry(path: Path, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def run(function: Callable[..., Any], grid: list[list[int]], k: int) -> dict[str, Any]:
    try:
        return {"kind": "return", "value": function(copy.deepcopy(grid), k)}
    except Exception as error:  # compare exception behavior explicitly
        return {"kind": "raise", "type": type(error).__name__, "message": str(error)}


def brute_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate all legal walks; independent of the alternating-path formula."""
    n = len(grid)
    if k == 0:
        return []
    paths: list[tuple[tuple[int, int], tuple[int, ...]]] = []
    for row in range(n):
        for col in range(n):
            paths.append(((row, col), (grid[row][col],)))
    for _ in range(1, k):
        extended: list[tuple[tuple[int, int], tuple[int, ...]]] = []
        for (row, col), values in paths:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                next_row, next_col = row + dr, col + dc
                if 0 <= next_row < n and 0 <= next_col < n:
                    extended.append(
                        (
                            (next_row, next_col),
                            values + (grid[next_row][next_col],),
                        )
                    )
        paths = extended
    return list(min(values for _, values in paths))


def grid_from_values(n: int, values: tuple[int, ...] | list[int]) -> list[list[int]]:
    return [list(values[row * n : (row + 1) * n]) for row in range(n)]


parser = argparse.ArgumentParser()
parser.add_argument("--cases-output", required=True, type=Path)
args = parser.parse_args()

canonical = load_entry(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_entry(
    Path("/tmp/audit-work/129-minPath/solution.py"), "audited_generated"
)

cases: list[dict[str, Any]] = []


def add_case(
    label: str,
    grid: list[list[int]],
    k: int,
    *,
    intended: bool,
    use_oracle: bool,
) -> None:
    cases.append(
        {
            "label": label,
            "grid": grid,
            "k": k,
            "intended": intended,
            "use_oracle": use_oracle,
        }
    )


add_case(
    "prompt-example-1",
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
    3,
    intended=True,
    use_oracle=True,
)
add_case(
    "prompt-example-2",
    [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
    1,
    intended=True,
    use_oracle=True,
)

# Boundary N=2, every permutation and k boundary/parity/longer values.
for permutation in itertools.permutations(range(1, 5)):
    grid = grid_from_values(2, permutation)
    for k in range(1, 9):
        add_case(
            "exhaustive-n2",
            grid,
            k,
            intended=True,
            use_oracle=True,
        )

# Every location of 1 in a 3x3 grid: collectively exercises each neighbor guard
# at false/true boundaries (corners, edges, and interior).
for one_position in range(9):
    values = [value for value in range(2, 10)]
    values.insert(one_position, 1)
    grid = grid_from_values(3, values)
    for k in (1, 2, 3, 6):
        add_case(
            f"n3-one-position-{one_position}",
            grid,
            k,
            intended=True,
            use_oracle=True,
        )

# Representative deterministic generated cases over larger dimensions/lengths.
rng = random.Random(129_20260723)
for n, samples in ((3, 160), (4, 160), (5, 80)):
    for sample in range(samples):
        values = list(range(1, n * n + 1))
        rng.shuffle(values)
        grid = grid_from_values(n, values)
        for k in (1, 2, 3, 7, 12):
            add_case(
                f"seeded-n{n}-sample-{sample}",
                grid,
                k,
                intended=True,
                use_oracle=False,
            )

# Explicit empty/beyond-contract probes. Divergence here is recorded separately.
add_case("empty-path-valid-grid", [[1, 2], [3, 4]], 0, intended=False, use_oracle=True)
add_case("empty-grid-empty-path", [], 0, intended=False, use_oracle=False)
add_case("empty-grid-positive-path", [], 1, intended=False, use_oracle=False)
add_case("n1-grid", [[1]], 1, intended=False, use_oracle=False)

intended_mismatches: list[dict[str, Any]] = []
outside_mismatches: list[dict[str, Any]] = []
oracle_mismatches: list[dict[str, Any]] = []
serialized_cases: list[dict[str, Any]] = []
oracle_checks = 0

for index, case in enumerate(cases):
    grid = case["grid"]
    k = case["k"]
    canonical_result = run(canonical, grid, k)
    generated_result = run(generated, grid, k)
    record = {
        "index": index,
        **case,
        "canonical": canonical_result,
        "generated": generated_result,
    }
    if canonical_result != generated_result:
        if case["intended"]:
            intended_mismatches.append(record)
        else:
            outside_mismatches.append(record)
    if case["use_oracle"]:
        oracle_checks += 1
        oracle_result = {"kind": "return", "value": brute_min_path(grid, k)}
        record["oracle"] = oracle_result
        if canonical_result != oracle_result or generated_result != oracle_result:
            oracle_mismatches.append(record)
    serialized_cases.append(record)

args.cases_output.write_text(
    json.dumps(
        {
            "seed": 129_20260723,
            "cases": serialized_cases,
            "summary": {
                "case_count": len(cases),
                "intended_case_count": sum(case["intended"] for case in cases),
                "outside_case_count": sum(not case["intended"] for case in cases),
                "oracle_check_count": oracle_checks,
                "intended_mismatch_count": len(intended_mismatches),
                "outside_mismatch_count": len(outside_mismatches),
                "oracle_mismatch_count": len(oracle_mismatches),
            },
        },
        indent=2,
        sort_keys=True,
    )
    + "\n"
)

print("seed=12920260723")
print(f"cases={len(cases)}")
print(f"intended_cases={sum(case['intended'] for case in cases)}")
print(f"outside_cases={sum(not case['intended'] for case in cases)}")
print(f"oracle_checks={oracle_checks}")
print(f"intended_mismatches={len(intended_mismatches)}")
print(f"oracle_mismatches={len(oracle_mismatches)}")
print(f"outside_mismatches={len(outside_mismatches)}")
for mismatch in outside_mismatches:
    print(
        "OUTSIDE_MISMATCH "
        f"label={mismatch['label']} grid={mismatch['grid']} k={mismatch['k']} "
        f"canonical={mismatch['canonical']} generated={mismatch['generated']}"
    )

if intended_mismatches or oracle_mismatches:
    raise SystemExit(1)
