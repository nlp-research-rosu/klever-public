#!/usr/bin/env python3
"""Append reviewer-authored assertions to the exact submitted Python source."""

from __future__ import annotations

import argparse
from pathlib import Path


ASSERTIONS = """

assert not is_happy("")
assert not is_happy("a")
assert not is_happy("aa")
assert is_happy("abc")
assert not is_happy("aab")
assert not is_happy("aba")
assert not is_happy("abb")
assert is_happy("abcd")
assert not is_happy("abcaab")
assert not is_happy("abcaba")
assert not is_happy("abcabb")
assert is_happy("abcabc")
assert not is_happy("abcabcaa")
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("solution", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    source = args.solution.read_text(encoding="utf-8")
    args.output.write_text(source.rstrip() + "\n" + ASSERTIONS, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
