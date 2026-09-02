#!/usr/bin/env python3
"""Ground witnesses for each formal entry precondition and result formula."""

from __future__ import annotations

import importlib.util
from pathlib import Path


def load_entry(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.valid_date


generated = load_entry(
    Path("/tmp/audit-work/fresh/solution.py"), "witness_generated"
)
canonical = load_entry(
    Path("/tmp/audit-work/trusted/canonical.py"), "witness_canonical"
)


def ascii_digit(code: int) -> bool:
    return 48 <= code <= 57


def valid_month_day(month: int, day: int) -> bool:
    return (
        (month == 2 and 1 <= day <= 29)
        or (month in (4, 6, 9, 11) and 1 <= day <= 30)
        or (month in (1, 3, 5, 7, 8, 10, 12) and 1 <= day <= 31)
    )


def formal_summary(date: str) -> bool:
    codes = [ord(character) for character in date]
    if len(codes) != 10:
        return False
    month = (codes[0] - 48) * 10 + codes[1] - 48
    day = (codes[3] - 48) * 10 + codes[4] - 48
    return (
        codes[2] == 45
        and codes[5] == 45
        and all(ascii_digit(codes[index]) for index in (0, 1, 3, 4, 6, 7, 8, 9))
        and valid_month_day(month, day)
    )


def main() -> None:
    witnesses = [
        ("valid-date-10 valid branch", "03-11-2000"),
        ("valid-date-10 false branch", "02-30-2000"),
        ("valid-date-10 day-31 boundary", "01-31-2000"),
        ("valid-date-non10 empty", ""),
    ]
    for label, date in witnesses:
        valid10_precondition = len(date) == 10
        non10_precondition = len(date) != 10
        print(
            f"{label}: input={date!r} len={len(date)} "
            f"pre10={valid10_precondition} pre_non10={non10_precondition} "
            f"formal={formal_summary(date)} generated={generated(date)} "
            f"canonical={canonical(date)}"
        )
        if generated(date) != formal_summary(date):
            raise SystemExit(1)


if __name__ == "__main__":
    main()
