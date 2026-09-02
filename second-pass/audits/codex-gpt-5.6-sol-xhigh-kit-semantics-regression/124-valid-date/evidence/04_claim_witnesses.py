#!/usr/bin/env python3
"""Concrete satisfying states for both entry claims and RHS substitution."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Callable


def load_entry(path: Path, module_name: str) -> Callable[[str], bool]:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


def valid_date_10_rhs(value: str) -> bool:
    assert len(value) == 10
    codes = [ord(character) for character in value]

    def ascii_digit(code: int) -> bool:
        return 48 <= code <= 57

    def two_digits(tens: int, ones: int) -> int:
        return (tens - 48) * 10 + (ones - 48)

    def max_day(month: int) -> int:
        if month == 2:
            return 29
        if month in (4, 6, 9, 11):
            return 30
        return 31

    month = two_digits(codes[0], codes[1])
    day = two_digits(codes[3], codes[4])
    return (
        codes[2] == 45
        and codes[5] == 45
        and all(ascii_digit(codes[index]) for index in (0, 1, 3, 4, 6, 7, 8, 9))
        and 1 <= month <= 12
        and 1 <= day <= max_day(month)
    )


def main() -> int:
    root = Path("/tmp/audit-work/124-valid-date")
    candidate = load_entry(root / "solution.py", "candidate_witness")
    canonical = load_entry(root / "trusted/canonical.py", "canonical_witness")
    witnesses = (
        ("valid-date-non10", "", False),
        ("valid-date-non10", " 03-11-2000 ", False),
        ("valid-date-ten", "02-29-2000", valid_date_10_rhs("02-29-2000")),
        ("valid-date-ten", "01-31-2000", valid_date_10_rhs("01-31-2000")),
        ("valid-date-ten", "04-31-2000", valid_date_10_rhs("04-31-2000")),
        ("valid-date-ten", "01-01-20a0", valid_date_10_rhs("01-01-20a0")),
    )

    failures = 0
    for claim, value, claimed_rhs in witnesses:
        precondition = len(value) != 10 if claim == "valid-date-non10" else len(value) == 10
        candidate_result = candidate(value)
        canonical_result = canonical(value)
        print(
            f"claim={claim} input={value!r} codepoints={[ord(c) for c in value]} "
            f"precondition={precondition} claimed_rhs={claimed_rhs} "
            f"candidate={candidate_result} canonical={canonical_result}"
        )
        if not precondition or candidate_result != claimed_rhs:
            failures += 1
    print(f"candidate_claim_mismatches={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
