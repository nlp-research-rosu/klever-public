#!/usr/bin/env python3
"""Emit a line-addressable inventory of candidate-local and supplied K items."""

from __future__ import annotations

import re
from pathlib import Path

ROOTS = [
    Path("/tmp/audit-work/src/reference-semantics/semantics.k"),
    *sorted(Path("/tmp/audit-work/src/reference-semantics/semantics").glob("*.k")),
    Path("/tmp/audit-work/src/verification.k"),
    Path("/tmp/audit-work/src/spec.k"),
]

START = re.compile(
    r"^\s*(configuration|context|syntax|rule|claim|alias|macro)\b"
)
CONTINUATION = re.compile(r"^\s*(\||\[\s*(?:function|total|functional|"
                          r"simplification|concrete|priority|owise|macro))")

for path in ROOTS:
    lines = path.read_text(encoding="utf-8").splitlines()
    print(f"FILE {path}")
    for number, line in enumerate(lines, 1):
        if START.search(line) or CONTINUATION.search(line):
            print(f"{number:04d}: {line.rstrip()}")
