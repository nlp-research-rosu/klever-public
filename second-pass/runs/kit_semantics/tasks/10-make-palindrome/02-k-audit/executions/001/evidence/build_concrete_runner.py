#!/usr/bin/env python3
"""Append independent assertions to the exact candidate source in scratch."""

from pathlib import Path


SOURCE = Path("/tmp/audit-work/candidate-clean/solution.py")
RUNNER = Path("/tmp/audit-work/candidate-clean/concrete_runner.py")

assertions = [
    ("", ""),
    ("a", "a"),
    ("aa", "aa"),
    ("ab", "aba"),
    ("cat", "catac"),
    ("cata", "catac"),
    ("race", "racecar"),
    ("abba", "abba"),
    ("abca", "abcacba"),
    ("aaaaab", "aaaaabaaaaa"),
]

suffix = "\n\n" + "\n".join(
    f"assert make_palindrome({value!r}) == {expected!r}"
    for value, expected in assertions
) + "\n"
RUNNER.write_text(SOURCE.read_text(encoding="utf-8") + suffix, encoding="utf-8")
print(f"runner={RUNNER}")
print(f"candidate_prefix_byte_identity={RUNNER.read_bytes().startswith(SOURCE.read_bytes())}")
print(f"assertion_count={len(assertions)}")
