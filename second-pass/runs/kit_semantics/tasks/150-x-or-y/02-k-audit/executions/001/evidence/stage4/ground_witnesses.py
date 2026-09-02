#!/usr/bin/env python3
"""Ground substitutions for the entry claim and loop precondition."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.x_or_y


def claimed_summary(n: int, x, y):
    if n < 2:
        return y
    result = x
    for divisor in range(2, n):
        if n % divisor == 0:
            result = y
    return result


candidate = load("candidate_solution", Path("/candidate/solution.py"))
canonical = load("trusted_canonical", Path("/reference/canonical.py"))

entry_witnesses = [
    (2, 10, 20, "smallest-prime/loop-base"),
    (4, 10, 20, "smallest-composite"),
    (7, 34, 12, "documented-prime"),
    (15, 8, 5, "documented-composite"),
    (0, 10, 20, "lower-boundary-discrepancy"),
]
print("entry_precondition=true (no requires clause)")
for n, x, y, label in entry_witnesses:
    summary = claimed_summary(n, x, y)
    actual = candidate(n, x, y)
    reference = canonical(n, x, y)
    print(
        f"ENTRY label={label} N={n} X={x!r} Y={y!r} "
        f"xOrYSpec={summary!r} candidate={actual!r} canonical={reference!r} "
        f"candidate_matches_summary={actual == summary} "
        f"canonical_matches_summary={reference == summary}"
    )

# Concrete states satisfying I >= 2 and I <= N in [trial-loop].
loop_witnesses = [
    (2, 2, 10, 20),
    (4, 2, 10, 20),
    (7, 2, 34, 12),
]
for n, i, result, y in loop_witnesses:
    assert i >= 2 and i <= n
    remaining = result
    for divisor in range(i, n):
        if n % divisor == 0:
            remaining = y
    print(
        f"LOOP N={n} I={i} R={result!r} Y={y!r} "
        f"precondition=True trialChoice={remaining!r}"
    )
