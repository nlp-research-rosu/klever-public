#!/usr/bin/env python3
"""Independent candidate/canonical differential suite for HumanEval 129."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path


sys.dont_write_bytecode = True
ROOT = Path("/audit-output/evidence")


def load_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def brute(grid: list[list[int]], k: int) -> list[int]:
    n = len(grid)
    states = [([grid[row][col]], row, col) for row in range(n) for col in range(n)]
    for _ in range(k - 1):
        following = []
        for values, row, col in states:
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = row + dr, col + dc
                if 0 <= nr < n and 0 <= nc < n:
                    following.append((values + [grid[nr][nc]], nr, nc))
        states = following
    return min(values for values, _, _ in states)


def as_grid(cells: list[int], n: int) -> list[list[int]]:
    return [cells[offset : offset + n] for offset in range(0, len(cells), n)]


def main() -> None:
    canonical = load_function("trusted_canonical_129", Path("/reference/canonical.py"))
    generated = load_function(
        "generated_candidate_129", Path("/tmp/audit-work/candidate-src/solution.py")
    )
    cases: list[dict] = []

    def add(label: str, grid: list[list[int]], k: int, in_domain: bool = True) -> None:
        cases.append({"label": label, "grid": grid, "k": k, "in_domain": in_domain})

    add("prompt-example-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3)
    add("prompt-example-2", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1)

    # Exhaustive valid 2x2 grids, including every branch boundary and both
    # neighbor-order outcomes, over several path lengths.
    for permutation in itertools.permutations(range(1, 5)):
        grid = as_grid(list(permutation), 2)
        for k in (1, 2, 3, 4, 5, 6, 7, 10):
            add("exhaustive-n2", grid, k)

    # Every possible position of 1 in a 3x3 grid, with deterministic rotations
    # of the remaining values and short/long path boundaries.
    tail = list(range(2, 10))
    for position in range(9):
        for shift, k in ((0, 1), (1, 2), (3, 6), (5, 11)):
            rotated = tail[shift:] + tail[:shift]
            cells = rotated[:]
            cells.insert(position, 1)
            add("all-one-positions-n3", as_grid(cells, 3), k)

    rng = random.Random(129_2026)
    for n, count in ((3, 120), (4, 80), (5, 30)):
        for sample in range(count):
            cells = list(range(1, n * n + 1))
            rng.shuffle(cells)
            k = rng.choice((1, 2, 3, 4, 5, 6, 9, 17, 50))
            add(f"generated-n{n}", as_grid(cells, n), k)

    # Empty/zero-length diagnostics requested by the audit. These are explicitly
    # outside the source contract (N >= 2 and k > 0) and cannot narrow it.
    add("outside-domain-empty-grid-k0", [], 0, False)
    add("outside-domain-empty-grid-k1", [], 1, False)
    add("outside-domain-zero-length-valid-grid", [[1, 2], [3, 4]], 0, False)

    mismatches = []
    brute_mismatches = []
    results = []
    for index, case in enumerate(cases):
        grid = case["grid"]
        k = case["k"]
        canonical_value = canonical(grid, k)
        generated_value = generated(grid, k)
        result = {
            **case,
            "canonical": canonical_value,
            "generated": generated_value,
        }
        if canonical_value != generated_value:
            mismatches.append({"index": index, **result})
        if case["in_domain"] and len(grid) <= 3 and k <= 7:
            brute_value = brute(grid, k)
            result["brute"] = brute_value
            if brute_value != canonical_value or brute_value != generated_value:
                brute_mismatches.append({"index": index, **result})
        results.append(result)

    output_path = ROOT / "02_differential_cases.json"
    output_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    digest = hashlib.sha256(output_path.read_bytes()).hexdigest()
    scopes: dict[str, int] = {}
    for case in cases:
        scopes[case["label"]] = scopes.get(case["label"], 0) + 1
    print(f"cases_file={output_path}")
    print(f"cases_sha256={digest}")
    print(f"total_cases={len(cases)}")
    print(f"in_domain_cases={sum(case['in_domain'] for case in cases)}")
    print(f"outside_domain_diagnostics={sum(not case['in_domain'] for case in cases)}")
    print(f"scope_counts={json.dumps(scopes, sort_keys=True)}")
    print(f"candidate_canonical_mismatches={len(mismatches)}")
    print(f"brute_checked_cases={sum('brute' in result for result in results)}")
    print(f"brute_mismatches={len(brute_mismatches)}")
    if mismatches:
        print(json.dumps(mismatches[:10], indent=2, sort_keys=True))
    if brute_mismatches:
        print(json.dumps(brute_mismatches[:10], indent=2, sort_keys=True))
    assert not mismatches
    assert not brute_mismatches
    print("DIFFERENTIAL_OK")


if __name__ == "__main__":
    main()
