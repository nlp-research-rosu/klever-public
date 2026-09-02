#!/usr/bin/env python3
"""Extract the complete Module(...) argument of the entry claim's #loadAll."""

from pathlib import Path

text = Path("/tmp/audit-work/fresh/spec.k").read_text(encoding="utf-8")
claim = text.index("claim [correct-bracketing]:")
load = text.index("#loadAll(", claim)
start = text.index("Module(", load)

depth = 0
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
            end = index + 1
            break

if end is None:
    raise SystemExit("unbalanced Module term")

print(text[start:end])
