#!/usr/bin/env python3
"""Independent differential test of candidate solution against trusted canonical."""

from __future__ import annotations

import importlib.util
import itertools
import random
import sys
from pathlib import Path


def load_function(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.smallest_change


canonical = load_function(Path("/reference/canonical.py"), "trusted_canonical")
candidate = load_function(Path("/candidate/solution.py"), "generated_solution")

documented = [
    [1, 2, 3, 5, 4, 7, 9, 6],
    [1, 2, 3, 4, 3, 2, 2],
    [1, 2, 3, 2, 1],
]
boundaries = [
    [],
    [0],
    [-7],
    [0, 0],
    [0, 1],
    [2, 9, 2],
    [2, 9, 3],
    [-10**50, 4, 5, -10**50],
    [-10**50, 4, 6, 10**50],
]
cases = list(documented) + list(boundaries)

# Exhaust all lists over a small integer alphabet through length 9. This hits
# every parity, base case, and equal/unequal outer-pair branch repeatedly.
for length in range(10):
    cases.extend(list(values) for values in itertools.product((-1, 0, 1), repeat=length))

# A deterministic broader sample covers large values and longer lists.
rng = random.Random(730073)
for _ in range(10_000):
    length = rng.randrange(0, 81)
    cases.append([rng.randrange(-(10**12), 10**12 + 1) for _ in range(length)])

# The source contract has no maximum length. These straddle the generated
# implementation's recursive-call depth boundary under the recorded CPython.
long_boundaries = [
    [0] * 1990,
    [0] * 2000,
    [index % 2 for index in range(2000)],
]
cases.extend(long_boundaries)


def outcome(function, arr):
    try:
        return ("return", function(list(arr)))
    except Exception as error:  # Preserve observable exceptional divergence.
        return ("exception", type(error).__name__, str(error))


mismatches = []
for index, arr in enumerate(cases):
    expected = outcome(canonical, arr)
    actual = outcome(candidate, arr)
    if expected != actual:
        mismatches.append(
            {
                "index": index,
                "length": len(arr),
                "head": arr[:8],
                "tail": arr[-8:],
                "canonical": expected,
                "candidate": actual,
            }
        )
        if len(mismatches) >= 10:
            break

print(f"documented_cases={len(documented)}")
print(f"explicit_boundary_cases={len(boundaries)}")
print("exhaustive_domain=values{-1,0,1}, lengths 0..9")
print("random_seed=730073")
print("random_cases=10000, lengths 0..80, values [-10^12,10^12]")
print(f"python_recursion_limit={sys.getrecursionlimit()}")
print("long_boundary_lengths=1990,2000,2000")
print(f"total_cases={len(cases)}")
print(f"mismatch_count={len(mismatches)}")
for mismatch in mismatches:
    print(f"mismatch={mismatch!r}")
raise SystemExit(1 if mismatches else 0)
