#!/usr/bin/env python3
"""Independent CPython differential and small-state path oracle for 129-minPath."""
import importlib.util
import itertools
import json
import random
import sys
from pathlib import Path

WORK = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/audit-work/minpath-129")

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

candidate = load("audited_candidate", WORK / "solution.py").minPath
canonical = load("trusted_canonical", WORK / "canonical.py").minPath

def rows(values, n):
    return [list(values[i:i+n]) for i in range(0, n*n, n)]

def brute_min_path(grid, k):
    """Enumerate actual moves; deliberately does not use either implementation's formula."""
    n = len(grid)
    neighbors = {}
    for r in range(n):
        for c in range(n):
            neighbors[r, c] = [
                (rr, cc)
                for rr, cc in ((r-1,c), (r+1,c), (r,c-1), (r,c+1))
                if 0 <= rr < n and 0 <= cc < n
            ]
    frontier = [((grid[r][c],), r, c) for r in range(n) for c in range(n)]
    for _ in range(1, k):
        frontier = [
            (path + (grid[rr][cc],), rr, cc)
            for path, r, c in frontier
            for rr, cc in neighbors[r, c]
        ]
    return list(min(path for path, _, _ in frontier))

valid_cases = []
valid_cases.extend([
    ("example-odd", [[1,2,3],[4,5,6],[7,8,9]], 3),
    ("example-k1", [[5,9,3],[4,1,6],[7,8,2]], 1),
    ("example-even", [[5,9,3],[4,1,6],[7,8,2]], 4),
])

for index, perm in enumerate(itertools.permutations(range(1, 5))):
    for k in range(1, 11):
        valid_cases.append((f"n2-perm{index}-k{k}", rows(perm, 2), k))

for one_pos in range(9):
    rest = [x for x in range(2, 10)]
    for variant, tail in enumerate((rest, list(reversed(rest)), rest[3:] + rest[:3])):
        values = tail[:]
        values.insert(one_pos, 1)
        for k in (1, 2, 3, 4, 5, 17):
            valid_cases.append((f"n3-pos{one_pos}-v{variant}-k{k}", rows(values, 3), k))

rng = random.Random(12920260801)
for n in range(3, 9):
    for sample in range(100):
        values = list(range(1, n*n + 1))
        rng.shuffle(values)
        for k in (1, 2, 3, 4, 5, 6, 17, 32):
            valid_cases.append((f"random-n{n}-s{sample}-k{k}", rows(values, n), k))

mismatches = []
length_or_domain_errors = []
for name, grid, k in valid_cases:
    got = candidate([row[:] for row in grid], k)
    expected = canonical([row[:] for row in grid], k)
    if got != expected:
        mismatches.append({"name": name, "grid": grid, "k": k, "candidate": got, "canonical": expected})
    if len(got) != k or any(value not in range(1, len(grid)*len(grid)+1) for value in got):
        length_or_domain_errors.append({"name": name, "candidate": got})

brute_cases = []
for index, perm in enumerate(itertools.permutations(range(1, 5))):
    for k in range(1, 7):
        brute_cases.append((f"brute-n2-perm{index}-k{k}", rows(perm, 2), k))
for n in (3, 4):
    for sample in range(20):
        values = list(range(1, n*n + 1))
        rng.shuffle(values)
        for k in range(1, 7):
            brute_cases.append((f"brute-n{n}-s{sample}-k{k}", rows(values, n), k))

brute_mismatches = []
for name, grid, k in brute_cases:
    got = candidate([row[:] for row in grid], k)
    expected = brute_min_path(grid, k)
    if got != expected:
        brute_mismatches.append({"name": name, "grid": grid, "k": k, "candidate": got, "brute": expected})

def capture(func, *args):
    try:
        return {"return": func(*args)}
    except Exception as err:
        return {"exception": type(err).__name__, "message": str(err)}

invalid_or_outside_contract = []
for name, grid, k in (
    ("empty-k1", [], 1),
    ("n1-k1", [[1]], 1),
    ("n1-k3", [[1]], 3),
    ("k0", [[1,2],[3,4]], 0),
    ("negative-k", [[1,2],[3,4]], -1),
    ("duplicate", [[1,1],[2,3]], 3),
):
    invalid_or_outside_contract.append({
        "name": name,
        "candidate": capture(candidate, [row[:] for row in grid], k),
        "canonical": capture(canonical, [row[:] for row in grid], k),
    })

summary = {
    "seed": 12920260801,
    "valid_cases": len(valid_cases),
    "candidate_canonical_mismatches": len(mismatches),
    "length_or_domain_errors": len(length_or_domain_errors),
    "brute_oracle_cases": len(brute_cases),
    "brute_oracle_mismatches": len(brute_mismatches),
    "documented_example_results": [
        candidate([[1,2,3],[4,5,6],[7,8,9]], 3),
        candidate([[5,9,3],[4,1,6],[7,8,2]], 1),
    ],
    "outside_contract_observations": invalid_or_outside_contract,
    "first_candidate_canonical_mismatches": mismatches[:5],
    "first_brute_mismatches": brute_mismatches[:5],
}
print(json.dumps(summary, indent=2, sort_keys=True))
sys.exit(1 if mismatches or length_or_domain_errors or brute_mismatches else 0)
