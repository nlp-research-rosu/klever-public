#!/usr/bin/env python3
"""Lexical inventory of every local K declaration/rule for manual audit."""

from __future__ import annotations

import re
from pathlib import Path


for raw in [
    "/tmp/audit-work/task134/semantic.k",
    "/tmp/audit-work/task134/verification.k",
    "/tmp/audit-work/task134/spec.k",
]:
    path = Path(raw)
    print(f"FILE={path}")
    lines = path.read_text().splitlines()
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        if (
            stripped.startswith(("syntax ", "| ", "configuration", "<python>", "<k>"))
            or stripped.startswith(("rule ", "claim ", "requires ", "imports "))
            or re.search(r"\[(?:function|total|functional|simplification|priority|owise|macro|alias|symbol)", stripped)
        ):
            print(f"{number:04d}: {stripped}")
    print()

all_text = (
    Path("/tmp/audit-work/task134/semantic.k").read_text()
    + Path("/tmp/audit-work/task134/verification.k").read_text()
)
for attribute in [
    "function",
    "total",
    "functional",
    "simplification",
    "priority",
    "owise",
    "macro",
    "alias",
    "symbol",
    "opaque",
]:
    pattern = re.compile(r"\b" + attribute + r"\b")
    print(f"ATTRIBUTE_COUNT {attribute}={len(pattern.findall(all_text))}")
