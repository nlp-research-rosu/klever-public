#!/usr/bin/env python3
"""Extract the Module argument actually placed under #loadAll in the entry claim."""

from __future__ import annotations

import sys
from pathlib import Path


spec_path = Path(
    sys.argv[1]
    if len(sys.argv) > 1
    else "/tmp/audit-work/15-string-sequence/candidate-src/spec.k"
)
text = spec_path.read_text(encoding="utf-8")
marker = "#loadAll("
start = text.index(marker) + len(marker)

depth = 1
in_string = False
escaped = False
end = None
for index in range(start, len(text)):
    char = text[index]
    if in_string:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            in_string = False
        continue
    if char == '"':
        in_string = True
    elif char == "(":
        depth += 1
    elif char == ")":
        depth -= 1
        if depth == 0:
            end = index
            break

if end is None:
    raise RuntimeError("unterminated #loadAll argument")

program = text[start:end].strip()
if not program.startswith("Module("):
    raise RuntimeError(f"entry term is not a Module: {program[:80]!r}")

if "--rule" in sys.argv[2:]:
    print(f"{program} => .K")
else:
    print(program)
