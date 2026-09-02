#!/usr/bin/env python3
"""Concrete witnesses for all seven entry claims."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load(path: Path, name: str) -> Callable[[int, int, int], bool]:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.right_angle_triangle


work = Path("/tmp/audit-work")
canonical = load(work / "canonical.py", "witness_canonical")
candidate = load(work / "solution.py", "witness_candidate")


def precondition(case: str, a: int, b: int, c: int) -> bool:
    if case == "pythagorean-c":
        return a > 0 and b > 0 and c > 0 and a * a + b * b == c * c
    if case == "pythagorean-b":
        return a > 0 and b > 0 and c > 0 and a * a + c * c == b * b
    if case == "pythagorean-a":
        return a > 0 and b > 0 and c > 0 and b * b + c * c == a * a
    if case == "nonpositive-a":
        return a <= 0
    if case == "nonpositive-b":
        return a > 0 and b <= 0
    if case == "nonpositive-c":
        return a > 0 and b > 0 and c <= 0
    if case == "positive-none":
        return (
            a > 0
            and b > 0
            and c > 0
            and a * a + b * b != c * c
            and a * a + c * c != b * b
            and b * b + c * c != a * a
        )
    raise AssertionError(case)


cases = [
    ("pythagorean-c", (3, 4, 5), True),
    ("pythagorean-b", (3, 5, 4), True),
    ("pythagorean-a", (5, 3, 4), True),
    ("nonpositive-a", (0, 4, 5), False),
    ("nonpositive-b", (3, 0, 5), False),
    ("nonpositive-c", (3, 4, 0), False),
    ("positive-none", (1, 2, 3), False),
]

failures = 0
for case, args, claimed in cases:
    satisfies = precondition(case, *args)
    candidate_result = candidate(*args)
    canonical_result = canonical(*args)
    ok = satisfies and candidate_result == claimed and canonical_result == claimed
    failures += not ok
    print(
        f"{case}: args={args} precondition={satisfies} claimed={claimed} "
        f"candidate={candidate_result} canonical={canonical_result} ok={ok}"
    )

print(f"WITNESS_FAILURES: {failures}")
raise SystemExit(1 if failures else 0)
