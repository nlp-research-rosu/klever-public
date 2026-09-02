#!/usr/bin/env python3
"""Append ground assertions to the submitted source without changing its function."""

from __future__ import annotations

import sys
from pathlib import Path


ASSERTIONS = """

assert triangle_area(1, 2, 3) == -1
assert triangle_area(2, 4, 2) == -1
assert triangle_area(4, 2, 2) == -1
assert triangle_area(3, 4, 5) == 6.0
assert triangle_area(2, 2, 3) == 1.98
"""


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_witness_program.py INPUT_SOLUTION OUTPUT_PY", file=sys.stderr)
        return 64
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    Path(sys.argv[2]).write_text(source.rstrip() + ASSERTIONS, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
