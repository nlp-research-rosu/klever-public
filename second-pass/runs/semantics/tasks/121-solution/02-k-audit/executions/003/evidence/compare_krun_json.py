#!/usr/bin/env python3
"""Compare canonical KAST JSON final configurations from two krun runs."""

from __future__ import annotations

import json
import sys
from pathlib import Path


if len(sys.argv) != 3:
    raise SystemExit("usage: compare_krun_json.py LEFT.json RIGHT.json")

left_path, right_path = map(Path, sys.argv[1:])
left = json.loads(left_path.read_text())
right = json.loads(right_path.read_text())
print("left:", left_path)
print("right:", right_path)
print("canonical_json_equal:", left == right)
assert left == right
