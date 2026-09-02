#!/usr/bin/env python3
"""Append reviewer-authored ground assertions to the exact scratch solution."""

from pathlib import Path

solution = Path("/tmp/audit-work/candidate-src/solution.py").read_text(encoding="utf-8")
assertions = r'''

assert longest([]) is None
assert longest(["a", "b", "c"]) == "a"
assert longest(["a", "bb", "ccc"]) == "ccc"
assert longest(["bb", "a"]) == "bb"
assert longest(["aa", "bb"]) == "aa"
assert longest(["", "", ""]) == ""
'''
print(solution.rstrip() + assertions)
