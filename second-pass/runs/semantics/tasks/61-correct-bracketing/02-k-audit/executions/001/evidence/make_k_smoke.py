#!/usr/bin/env python3
"""Append concrete assertions to the exact copied candidate source."""

from __future__ import annotations

import argparse
from pathlib import Path


SUFFIX = r'''

assert correct_bracketing("")
assert not correct_bracketing("(")
assert correct_bracketing("()")
assert correct_bracketing("(()())")
assert not correct_bracketing(")(()")
assert not correct_bracketing(")")
assert not correct_bracketing("((")
assert not correct_bracketing("())")
assert not correct_bracketing("(()")
assert correct_bracketing("()()")
assert correct_bracketing("((()))")
assert correct_bracketing("((())())")
'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("solution")
    parser.add_argument("output")
    args = parser.parse_args()
    source = Path(args.solution).read_text(encoding="utf-8")
    Path(args.output).write_text(source.rstrip() + SUFFIX, encoding="utf-8")
    print(f"copied_solution_bytes={len(source.encode('utf-8'))}")
    print("appended_assertions=12")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
