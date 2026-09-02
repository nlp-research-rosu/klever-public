#!/usr/bin/env python3
"""Append concrete assertions to an exact copy of solution.py on stdout."""

from __future__ import annotations

import sys
from pathlib import Path

TESTS = (
    ("three one five", "one three five"),
    ("", ""),
    (" ", ""),
    ("  three one five  ", "one three five"),
    ("nine  zero   five", "zero five nine"),
    (
        "nine eight seven six five four three two one zero",
        "zero one two three four five six seven eight nine",
    ),
    ("nine zero nine zero nine zero", "zero zero zero nine nine nine"),
)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: make_k_concrete_tests.py SOLUTION.py", file=sys.stderr)
        return 64
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    sys.stdout.write(source)
    if not source.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.write("\n")
    for value, expected in TESTS:
        sys.stdout.write(f"assert sort_numbers({value!r}) == {expected!r}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
