#!/usr/bin/env python3
"""Mutate the function body term used by triangleAreaClosure, not solution.py."""

from __future__ import annotations

import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit("usage: mutate_executed_body.py INPUT_VERIFICATION OUTPUT_VERIFICATION")

source = Path(sys.argv[1]).read_text()
old = 'Return(UnaryOp("-", Int(1)))'
new = 'Return(UnaryOp("-", Int(2)))'
assert source.count(old) == 1, "expected exactly one return -1 body constructor"
Path(sys.argv[2]).write_text(source.replace(old, new))
print(f"changed executed body constructor: {old} -> {new}")
