#!/usr/bin/env python3
"""Append audit assertions to the exact submitted Python source."""

from pathlib import Path
import sys


if len(sys.argv) != 3:
    raise SystemExit(f"usage: {sys.argv[0]} SOURCE.py OUTPUT.py")

source = Path(sys.argv[1]).read_text()
tests = r'''

assert right_angle_triangle(3, 4, 5)
assert right_angle_triangle(5, 3, 4)
assert right_angle_triangle(3, 5, 4)
assert not right_angle_triangle(1, 2, 3)
assert not right_angle_triangle(0, 3, 3)
assert not right_angle_triangle(3, 0, 3)
assert not right_angle_triangle(3, 3, 0)
assert not right_angle_triangle(-3, 4, 5)
assert right_angle_triangle(3000000, 4000000, 5000000)
'''
Path(sys.argv[2]).write_text(source.rstrip() + tests)
