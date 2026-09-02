#!/usr/bin/env python3
"""Wrap the freshly regenerated submitted Module term in a concrete Run."""

from __future__ import annotations

import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("x", type=int)
parser.add_argument("y", type=int)
parser.add_argument("output", type=Path)
args = parser.parse_args()

module_term = Path("/tmp/audit-work/regenerated.mpy").read_text(encoding="utf-8").strip()
args.output.write_text(
    f"Run(\n{module_term},\n  Int({args.x}), Int({args.y}))\n",
    encoding="utf-8",
)
