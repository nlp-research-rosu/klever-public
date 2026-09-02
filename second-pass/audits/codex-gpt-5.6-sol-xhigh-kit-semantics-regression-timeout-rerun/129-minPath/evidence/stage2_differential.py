#!/usr/bin/env python3
"""Independent candidate/canonical/contract-oracle differential audit."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import random
from itertools import permutations
from pathlib import Path
from typing import Any, Callable


def load_entry(path: str, module_name: str) -> Callable[[list[list[int]], int], list[int]]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def exhaustive_oracle(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate all legal length-k paths; independent of both implementations."""
    n = len(grid)
    paths = [((grid[r][c],), r, c) for r in range(n) for c in range(n)]
    for _ in range(1, k):
        next_paths = []
        for values, row, col in paths:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < n:
                    next_paths.append((values + (grid[nr][nc],), nr, nc))
        paths = next_paths
    return list(min(values for values, _, _ in paths))


def outcome(function: Callable[..., Any], grid: list[list[int]], k: int) -> dict[str, Any]:
    try:
        return {"kind": "value", "value": function([row[:] for row in grid], k)}
    except Exception as err:  # Deliberately records out-of-contract behavior.
        return {"kind": "exception", "type": type(err).__name__, "message": str(err)}


def make_grid(n: int, one_index: int) -> list[list[int]]:
    values = list(range(2, n * n + 1))
    values.insert(one_index, 1)
    return [values[offset : offset + n] for offset in range(0, n * n, n)]


def build_cases() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    valid: list[dict[str, Any]] = [
        {
            "group": "prompt-example",
            "grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            "k": 3,
        },
        {
            "group": "prompt-example",
            "grid": [[5, 9, 3], [4, 1, 6], [7, 8, 2]],
            "k": 1,
        },
    ]

    # Intended-domain lower boundary N=2, all placements and all permutations.
    for values in permutations(range(1, 5)):
        grid = [list(values[:2]), list(values[2:])]
        for k in range(1, 8):
            valid.append({"group": "n2-exhaustive", "grid": grid, "k": k})

    # Explicitly place 1 at every corner, edge, and interior position. Across
    # these cases all four neighbor-guard true/false boundaries are exercised.
    for one_index in range(9):
        for k in range(1, 9):
            valid.append(
                {
                    "group": "n3-one-position-boundaries",
                    "grid": make_grid(3, one_index),
                    "k": k,
                }
            )

    rng = random.Random(129_2026)
    for n, samples, max_k in ((3, 50, 8), (4, 30, 6), (5, 15, 5)):
        for _ in range(samples):
            values = list(range(1, n * n + 1))
            rng.shuffle(values)
            grid = [values[offset : offset + n] for offset in range(0, n * n, n)]
            for k in range(1, max_k + 1):
                valid.append({"group": f"generated-n{n}", "grid": grid, "k": k})

    # These are explicitly outside the prompt domain and are characterization
    # tests only. They include the requested empty/boundary probes.
    invalid = [
        {"group": "out-of-contract-empty-grid", "grid": [], "k": 1},
        {"group": "out-of-contract-zero-k", "grid": [[1, 2], [3, 4]], "k": 0},
        {"group": "out-of-contract-negative-k", "grid": [[1, 2], [3, 4]], "k": -1},
        {"group": "out-of-contract-n1", "grid": [[1]], "k": 1},
    ]
    return valid, invalid


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs-json")
    args = parser.parse_args()

    canonical = load_entry("/reference/canonical.py", "trusted_canonical")
    generated = load_entry(
        "/tmp/audit-work/reconstruction/solution.py", "generated_solution"
    )
    valid, invalid = build_cases()

    serialized = json.dumps(
        {"valid": valid, "out_of_contract": invalid},
        sort_keys=True,
        separators=(",", ":"),
    )
    if args.inputs_json:
        Path(args.inputs_json).write_text(
            json.dumps(
                {"valid": valid, "out_of_contract": invalid},
                sort_keys=True,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    canonical_candidate_mismatches = []
    oracle_mismatches = []
    groups: dict[str, int] = {}
    for index, case in enumerate(valid):
        grid, k = case["grid"], case["k"]
        groups[case["group"]] = groups.get(case["group"], 0) + 1
        expected = exhaustive_oracle(grid, k)
        trusted = outcome(canonical, grid, k)
        actual = outcome(generated, grid, k)
        if trusted != actual:
            canonical_candidate_mismatches.append((index, case, trusted, actual))
        if trusted != {"kind": "value", "value": expected}:
            oracle_mismatches.append((index, case, "canonical", expected, trusted))
        if actual != {"kind": "value", "value": expected}:
            oracle_mismatches.append((index, case, "generated", expected, actual))

    invalid_results = []
    for case in invalid:
        invalid_results.append(
            {
                "case": case,
                "canonical": outcome(canonical, case["grid"], case["k"]),
                "generated": outcome(generated, case["grid"], case["k"]),
            }
        )

    print(f"valid_cases={len(valid)}")
    print(f"groups={json.dumps(groups, sort_keys=True)}")
    print(f"inputs_sha256={hashlib.sha256(serialized.encode()).hexdigest()}")
    print(f"canonical_candidate_mismatches={len(canonical_candidate_mismatches)}")
    print(f"oracle_mismatches={len(oracle_mismatches)}")
    print("out_of_contract_results=" + json.dumps(invalid_results, sort_keys=True))
    if canonical_candidate_mismatches:
        print(
            "first_canonical_candidate_mismatch="
            + repr(canonical_candidate_mismatches[0])
        )
    if oracle_mismatches:
        print("first_oracle_mismatch=" + repr(oracle_mismatches[0]))
    return 1 if canonical_candidate_mismatches or oracle_mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
