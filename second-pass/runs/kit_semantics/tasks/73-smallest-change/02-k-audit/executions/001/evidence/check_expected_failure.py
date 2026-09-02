#!/usr/bin/env python3
"""Validate that a logged kprove run is a meaningful expected failure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument("log", type=Path)
parser.add_argument("patterns", nargs="+")
args = parser.parse_args()

text = args.log.read_text(errors="replace")
statuses = re.findall(r"^EXIT_STATUS: ([0-9]+)$", text, flags=re.MULTILINE)
if len(statuses) != 1:
    raise SystemExit(f"expected one EXIT_STATUS line, found {statuses!r}")
status = int(statuses[0])
print(f"logged_exit_status={status}")
print(f"nonzero={status != 0}")
ok = status != 0
for pattern in args.patterns:
    present = pattern in text
    print(f"contains[{pattern!r}]={present}")
    ok = ok and present
raise SystemExit(0 if ok else 1)
