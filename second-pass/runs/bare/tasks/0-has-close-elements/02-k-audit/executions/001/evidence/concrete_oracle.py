#!/usr/bin/env python3
"""Independent Python oracle for the concrete generated-semantics cases."""

import importlib.util
from fractions import Fraction
from pathlib import Path


def load_entry(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.has_close_elements


canonical = load_entry("trusted_canonical_concrete", Path("/reference/canonical.py"))
candidate = load_entry(
    "submitted_solution_concrete", Path("/tmp/audit-work/source/solution.py")
)

cases = [
    ("example_false", [Fraction(1), Fraction(2), Fraction(3)], Fraction(1, 2)),
    (
        "example_true",
        [Fraction(1), Fraction(14, 5), Fraction(3), Fraction(4),
         Fraction(5), Fraction(2)],
        Fraction(3, 10),
    ),
    ("empty", [], Fraction(1)),
    ("singleton", [Fraction(1)], Fraction(1)),
    ("strict_equal", [Fraction(1), Fraction(3, 2)], Fraction(1, 2)),
    (
        "strict_just_above",
        [Fraction(1), Fraction(3, 2)],
        Fraction(5000001, 10000000),
    ),
    ("negative_threshold", [Fraction(1), Fraction(1)], Fraction(-1)),
    (
        "negative_rational_strict",
        [Fraction(-1, 2), Fraction(0)],
        Fraction(1, 2),
    ),
    (
        "negative_rational_above",
        [Fraction(-1, 2), Fraction(0)],
        Fraction(5000001, 10000000),
    ),
    (
        "pair_only_at_end",
        [Fraction(100), Fraction(-100), Fraction(5), Fraction(21, 4)],
        Fraction(3, 10),
    ),
]

for label, numbers, threshold in cases:
    canonical_result = canonical(numbers, threshold)
    candidate_result = candidate(numbers, threshold)
    print(
        f"{label}: canonical={str(canonical_result).lower()} "
        f"candidate={str(candidate_result).lower()}"
    )
    if canonical_result != candidate_result:
        raise SystemExit(1)
