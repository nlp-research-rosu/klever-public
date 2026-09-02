#!/usr/bin/env python3
"""Independent differential test for HumanEval/129 minPath."""

from __future__ import annotations

import importlib.util
import itertools
import random
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.minPath


def brute_min_path(grid: list[list[int]], k: int) -> list[int]:
    """Enumerate all walks; independent oracle for bounded, valid inputs."""
    n = len(grid)
    states = [([grid[i][j]], i, j) for i in range(n) for j in range(n)]
    for _ in range(1, k):
        next_states = []
        for values, i, j in states:
            for di, dj in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < n and 0 <= nj < n:
                    next_states.append((values + [grid[ni][nj]], ni, nj))
        states = next_states
    return min(values for values, _, _ in states)


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
generated = load_function(Path("/tmp/audit-work/129-minPath/solution.py"), "generated_solution")

cases: list[tuple[str, list[list[int]], int, bool]] = [
    ("prompt-1", [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 3, True),
    ("prompt-2", [[5, 9, 3], [4, 1, 6], [7, 8, 2]], 1, True),
    ("n2-k1-top-left", [[1, 2], [3, 4]], 1, True),
    ("n2-bottom-right-even-k", [[4, 3], [2, 1]], 8, False),
    ("edge-one", [[2, 1, 7], [3, 6, 8], [4, 5, 9]], 7, False),
    ("interior-one", [[9, 8, 7], [6, 1, 2], [5, 4, 3]], 6, True),
    ("n4-corner-one", [[1, 16, 3, 4], [2, 15, 6, 5], [9, 10, 7, 8], [13, 14, 11, 12]], 5, False),
]

# Exhaust every 2x2 branch arrangement at several k boundaries.
for permutation in itertools.permutations(range(1, 5)):
    grid = [list(permutation[:2]), list(permutation[2:])]
    for k in (1, 2, 3, 4, 5, 9):
        cases.append(("exhaustive-n2", grid, k, True))

# Seeded representative permutations across the unrestricted N>=2 domain.
rng = random.Random(129_20260726)
for n in range(2, 9):
    for sample in range(40):
        values = list(range(1, n * n + 1))
        rng.shuffle(values)
        grid = [values[i * n : (i + 1) * n] for i in range(n)]
        k = (sample % 15) + 1
        cases.append((f"seeded-n{n}", grid, k, n <= 4 and k <= 6))

mismatches = []
brute_mismatches = []
for index, (label, grid, k, use_brute) in enumerate(cases):
    expected = canonical(grid, k)
    actual = generated(grid, k)
    if expected != actual:
        mismatches.append((index, label, grid, k, expected, actual))
    if use_brute:
        brute = brute_min_path(grid, k)
        if expected != brute or actual != brute:
            brute_mismatches.append((index, label, grid, k, brute, expected, actual))

print("valid_cases:", len(cases))
print("canonical_generated_mismatches:", len(mismatches))
print("bounded_bruteforce_cases:", sum(use_brute for _, _, _, use_brute in cases))
print("bruteforce_mismatches:", len(brute_mismatches))
if mismatches:
    print("first_canonical_generated_mismatch:", mismatches[0])
if brute_mismatches:
    print("first_bruteforce_mismatch:", brute_mismatches[0])

# Required empty/boundary characterization. These are outside the source
# precondition and therefore reported, not asserted as correctness failures.
out_of_domain = [
    ("empty-grid-k1", [], 1),
    ("empty-grid-k2", [], 2),
    ("valid-grid-k0", [[1, 2], [3, 4]], 0),
]
print("out_of_domain_characterization:")
for label, grid, k in out_of_domain:
    row = [label]
    for name, fn in (("canonical", canonical), ("generated", generated)):
        try:
            row.append(f"{name}={fn(grid, k)!r}")
        except Exception as err:
            row.append(f"{name}=raises {type(err).__name__}: {err}")
    print("  " + " | ".join(row))

assert not mismatches
assert not brute_mismatches
print("DIFFERENTIAL_TEST: PASS")
