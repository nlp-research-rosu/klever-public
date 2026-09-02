#!/usr/bin/env python3
"""Ground witnesses satisfying each submitted entry claim's precondition."""

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


canonical = load_entry("trusted_canonical_witness", Path("/reference/canonical.py"))
candidate = load_entry("submitted_solution_witness", Path("/tmp/audit-work/source/solution.py"))

witnesses = [
    (1, [Fraction(1), Fraction(2), Fraction(3)], Fraction(1, 2), False),
    (
        2,
        [Fraction(1), Fraction(14, 5), Fraction(3), Fraction(4),
         Fraction(5), Fraction(2)],
        Fraction(3, 10),
        True,
    ),
    (3, [], Fraction(0), False),
    (4, [Fraction(7)], Fraction(100), False),
    (5, [Fraction(0), Fraction(1)], Fraction(2), True),
    (6, [Fraction(0), Fraction(1), Fraction(3)], Fraction(2), True),
    (
        7,
        [Fraction(0), Fraction(10), Fraction(20), Fraction(21)],
        Fraction(2),
        True,
    ),
    (8, [Fraction(1), Fraction(3, 2)], Fraction(1, 2), False),
    (
        9,
        [Fraction(1), Fraction(3, 2)],
        Fraction(5000001, 10000000),
        True,
    ),
]

for claim, numbers, threshold, postcondition in witnesses:
    trusted_result = canonical(numbers, threshold)
    submitted_result = candidate(numbers, threshold)
    print(
        f"claim={claim} numbers={numbers!r} threshold={threshold!r} "
        f"claimed={str(postcondition).lower()} "
        f"canonical={str(trusted_result).lower()} "
        f"candidate={str(submitted_result).lower()}"
    )
    if trusted_result != postcondition or submitted_result != postcondition:
        raise SystemExit(1)
