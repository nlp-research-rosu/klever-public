#!/usr/bin/env python3
"""Emit the exact submitted solution source followed by independent assertions."""

from pathlib import Path


source = Path("/tmp/audit-work/127-intersection/solution.py").read_text(
    encoding="utf-8"
)
assertions = r'''

assert intersection((1, 2), (2, 3)) == "NO"
assert intersection((-1, 1), (0, 4)) == "NO"
assert intersection((-3, -1), (-5, 5)) == "YES"
assert intersection((0, 1), (3, 4)) == "NO"
assert intersection((0, 2), (2, 5)) == "NO"
assert intersection((4, 4), (4, 4)) == "NO"
assert intersection((0, 2), (-1, 4)) == "YES"
assert intersection((0, 4), (-1, 5)) == "NO"
assert intersection((-3, 4), (-3, 4)) == "YES"
assert intersection((10, 16), (0, 20)) == "NO"
'''
print(source.rstrip() + assertions)
