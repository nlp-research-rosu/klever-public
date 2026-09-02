#!/usr/bin/env python3
"""Extract the balanced Module(...) term from the entry claim's <k> cell."""

from pathlib import Path

text = Path("/tmp/audit-work/src/spec.k").read_text(encoding="utf-8")
k_start = text.index("<k>")
start = text.index("Module(", k_start)
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
    raise RuntimeError("unbalanced Module term")
# Empty K list units are valid in a claim/rule pattern but not as concrete
# surface-program tokens. Removing their printed unit names yields the same
# empty concrete list constructors used by solution.mpy.
print(text[start:end].replace(".Exprs", "").replace(".Stmts", ""))
