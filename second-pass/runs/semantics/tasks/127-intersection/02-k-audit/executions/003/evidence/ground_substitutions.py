#!/usr/bin/env python3
"""Concrete satisfying substitutions for the universal entry claim."""

import importlib.util
import math
from pathlib import Path


def load(name: str, path: str):
    spec = importlib.util.spec_from_file_location(name, Path(path))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prime(number: int) -> bool:
    return number >= 2 and all(
        number % divisor for divisor in range(2, math.isqrt(number) + 1)
    )


canonical = load("canonical_ground", "/reference/canonical.py")
candidate = load("candidate_ground", "/candidate/solution.py")
substitutions = [
    (0, 2, -1, 5),
    (0, 4, 0, 4),
    (5, 5, 5, 5),
    (-20, -11, -30, 0),
    (-3, 9, -1, 4),
]

for a, b, c, d in substitutions:
    assert a <= b and c <= d
    length = min(b, d) - max(a, c)
    claimed = "YES" if prime(length) else "NO"
    one, two = (a, b), (c, d)
    canonical_value = canonical.intersection(one, two)
    candidate_value = candidate.intersection(one, two)
    assert claimed == canonical_value == candidate_value
    print(
        f"A={a} B={b} C={c} D={d} precondition=true "
        f"overlapLength={length} claimed={claimed} "
        f"canonical={canonical_value} candidate={candidate_value}"
    )

print("GROUND_SUBSTITUTIONS_PASS")
