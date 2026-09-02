#!/usr/bin/env python3
"""Python oracle outputs for the fresh concrete K semantics cases."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


scratch = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("generated_solution", scratch / "solution.py")
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load generated solution")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

cases = [
    ("empty-equality", [], 0),
    ("empty-overweight", [], -1),
    ("nonpalindrome", [1, 2], 5),
    ("palindrome-normal", [3, 2, 3], 9),
    ("negative-weight-equality", [2, -5, 2], -1),
    ("negative-mixed-overweight", [-2, 5, -2], 0),
]

for name, q, w in cases:
    print(f"{name}: q={q!r} w={w} result={module.will_it_fly(q, w)!r}")
