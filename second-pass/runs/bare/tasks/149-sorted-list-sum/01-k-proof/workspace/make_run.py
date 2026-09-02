#!/usr/bin/env python3
"""Wrap solution.mpy and a constructor expression in a semantic Run term."""

import pathlib
import sys


module = pathlib.Path("solution.mpy").read_text(encoding="utf-8").strip()
print(f"Run({module}, {sys.argv[1]})")
