#!/usr/bin/env python3
"""Emit a direct Run(Module(...), Call(...)) program for semantic.k."""

from __future__ import annotations

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("integers", nargs="*", type=int)
args = parser.parse_args()

module = Path(
    "/tmp/audit-work/candidate-src/solution.regenerated.mpy"
).read_text(encoding="utf-8").strip()
assert module.startswith("Module(") and module.endswith(")")
items = ", ".join(f"Int({integer})" for integer in args.integers)
list_term = f"ListExpr({items})"
print(f'Run({module}, Call(Name("specialFilter"), {list_term}))')
