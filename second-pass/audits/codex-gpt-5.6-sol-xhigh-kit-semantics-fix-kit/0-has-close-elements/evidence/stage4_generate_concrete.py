#!/usr/bin/env python3
"""Append fixed boundary assertions to the exact scratch solution source."""

from __future__ import annotations

import argparse
from pathlib import Path


ASSERTIONS = """

assert has_close_elements([], 0.5) == False
assert has_close_elements([1.0], 100.0) == False
assert has_close_elements([1.0, 1.125], 0.25) == True
assert has_close_elements([1.0, 1.5], 0.5) == False
assert has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) == True
assert has_close_elements([-3.0, -3.0], -1.0) == False
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--solution", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.write_text(args.solution.read_text(encoding="utf-8") + ASSERTIONS, encoding="utf-8")
    print(f"generated={args.output}")
    print("assertion_count=6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
