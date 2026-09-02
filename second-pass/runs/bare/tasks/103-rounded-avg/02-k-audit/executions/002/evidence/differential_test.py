#!/usr/bin/env python3
"""Independent differential test of candidate and trusted canonical entry points."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


canonical = load("trusted_canonical", Path("/reference/canonical.py")).rounded_avg
candidate = load(
    "generated_candidate", Path("/tmp/audit-work/reconstruction/solution.py")
).rounded_avg


def outcome(function, n: int, m: int):
    try:
        value = function(n, m)
        return ("return", type(value).__name__, value)
    except Exception as error:  # compare exception behavior as an observable
        return ("raise", type(error).__name__, str(error))


documented_and_boundaries = [
    (1, 5),       # documented integral midpoint
    (7, 5),       # documented reversed interval
    (10, 20),     # documented integral midpoint
    (20, 33),     # documented half-even down
    (1, 1),       # smallest positive singleton
    (2, 1),       # branch boundary just reversed
    (2, 2),       # equal endpoints
    (1, 2),       # 1.5, lower neighbor odd: up
    (2, 3),       # 2.5, lower neighbor even: down
    (3, 4),       # 3.5, lower neighbor odd: up
    (4, 5),       # 4.5, lower neighbor even: down
    (1, 100),
    (100, 1),
    (2**53 - 1, 2**53 - 1),
    (2**53, 2**53),
    (2**53 + 1, 2**53 + 1),
    (2**53 + 3, 2**53 + 3),
]

rng = random.Random(103)
generated = [(rng.randint(1, 250), rng.randint(1, 250)) for _ in range(1000)]
cases = documented_and_boundaries + generated
mismatches = []
for index, (n, m) in enumerate(cases):
    left = outcome(canonical, n, m)
    right = outcome(candidate, n, m)
    print(f"CASE index={index} n={n} m={m} canonical={left!r} candidate={right!r}")
    if left != right:
        mismatches.append((n, m, left, right))

print(
    f"SUMMARY cases={len(cases)} generated={len(generated)} "
    f"mismatches={len(mismatches)}"
)
for mismatch in mismatches[:20]:
    print("MISMATCH", mismatch)
raise SystemExit(1 if mismatches else 0)
