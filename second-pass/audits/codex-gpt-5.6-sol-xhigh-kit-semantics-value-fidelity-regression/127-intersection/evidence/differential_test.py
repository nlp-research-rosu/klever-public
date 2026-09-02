#!/usr/bin/env python3
"""Independent candidate/canonical differential test for 127-intersection."""

from __future__ import annotations

import importlib.util
import random
from pathlib import Path


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


candidate = load(
    Path("/tmp/audit-work/127-intersection/solution.py"), "audited_solution"
).intersection
canonical = load(Path("/reference/canonical.py"), "trusted_canonical").intersection

# These cases cover all prompt examples and the material decision boundaries:
# either endpoint-selection branch, equality at either endpoint, disjoint and
# touching intervals, zero-width intervals, lengths 0/1/2, prime/composite
# positive lengths, negatives, containment, and coincident intervals.
special_cases = [
    ("prompt-1", (1, 2), (2, 3), "NO"),
    ("prompt-2", (-1, 1), (0, 4), "NO"),
    ("prompt-3", (-3, -1), (-5, 5), "YES"),
    ("empty-left", (0, 1), (3, 4), "NO"),
    ("empty-right", (3, 4), (0, 1), "NO"),
    ("touching", (0, 2), (2, 5), "NO"),
    ("both-points-equal", (4, 4), (4, 4), "NO"),
    ("distinct-points", (1, 1), (2, 2), "NO"),
    ("start-equality", (0, 2), (0, 5), "YES"),
    ("end-equality", (-2, 2), (0, 2), "YES"),
    ("length-1", (0, 1), (-1, 4), "NO"),
    ("length-2-prime", (0, 2), (-1, 4), "YES"),
    ("length-3-prime", (-10, -7), (-12, 0), "YES"),
    ("length-4-composite", (0, 4), (-1, 5), "NO"),
    ("length-5-prime", (10, 15), (0, 20), "YES"),
    ("length-6-composite", (10, 16), (0, 20), "NO"),
    ("first-contained", (2, 7), (0, 10), "YES"),
    ("second-contained", (0, 10), (2, 7), "YES"),
    ("same-interval", (-3, 4), (-3, 4), "YES"),
    ("large-prime-length", (0, 97), (-100, 100), "YES"),
    ("large-composite-length", (0, 100), (-100, 100), "NO"),
]

mismatches: list[tuple[tuple[int, int], tuple[int, int], object, object]] = []
count = 0
print("SPECIAL CASES")
for label, left, right, expected in special_cases:
    c = candidate(left, right)
    o = canonical(left, right)
    count += 1
    print(f"{label}: {left}, {right} -> candidate={c} canonical={o} expected={expected}")
    if c != o or c != expected:
        mismatches.append((left, right, c, o))

intervals = [(a, b) for a in range(-8, 9) for b in range(a, 9)]
for left in intervals:
    for right in intervals:
        c = candidate(left, right)
        o = canonical(left, right)
        count += 1
        if c != o:
            mismatches.append((left, right, c, o))

rng = random.Random(127_20260723)
random_count = 4000
for _ in range(random_count):
    a, b = sorted((rng.randint(-200, 200), rng.randint(-200, 200)))
    c, d = sorted((rng.randint(-200, 200), rng.randint(-200, 200)))
    left, right = (a, b), (c, d)
    got = candidate(left, right)
    expected = canonical(left, right)
    count += 1
    if got != expected:
        mismatches.append((left, right, got, expected))

print(
    "EXHAUSTIVE DOMAIN: every ordered pair of well-formed integer intervals "
    "with endpoints in [-8,8]"
)
print(f"EXHAUSTIVE INTERVALS: {len(intervals)}, PAIRS: {len(intervals) ** 2}")
print(
    "GENERATED DOMAIN: seed=12720260723, 4000 ordered pairs of intervals "
    "formed by sorting independently sampled endpoints in [-200,200]"
)
print(f"TOTAL CASES: {count}")
print(f"MISMATCHES: {len(mismatches)}")
for item in mismatches[:20]:
    print(f"MISMATCH: {item}")
raise SystemExit(1 if mismatches else 0)
