#!/usr/bin/env python3
"""Extract the balanced Module(...) constructor term from the entry claim."""

from __future__ import annotations

from pathlib import Path


SPEC = Path("/tmp/audit-work/rebuild/spec.k")
text = SPEC.read_text()
k_start = text.index("<k>")
start = text.index("Module(", k_start)

depth = 0
in_string = False
escaped = False
end = None
for index in range(start, len(text)):
    character = text[index]
    if in_string:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == '"':
            in_string = False
        continue
    if character == '"':
        in_string = True
    elif character == "(":
        depth += 1
    elif character == ")":
        depth -= 1
        if depth == 0:
            end = index + 1
            break

assert end is not None, "unterminated Module(...) term"
print(text[start:end])
