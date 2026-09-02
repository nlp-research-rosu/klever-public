#!/usr/bin/env python3
"""Extract the balanced `solution` function RHS from verification.k.

This lets the audit parse the submitted translator output and the exact term
embedded in the proof definition independently, then compare their KORE bytes.
The rule notation spells empty list units as `.Stmts`; the program parser spells
the same list unit as an empty character sequence, so that syntax-only spelling
is normalized before parsing.
"""

from pathlib import Path


source = Path("/tmp/audit-work/closest-audit/verification.k").read_text()
marker = "rule solution =>"
marker_index = source.index(marker)
start = source.index("Module(", marker_index + len(marker))

depth = 0
quoted = False
escaped = False
end = None
for index, character in enumerate(source[start:], start):
    if quoted:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == '"':
            quoted = False
        continue
    if character == '"':
        quoted = True
    elif character == "(":
        depth += 1
    elif character == ")":
        depth -= 1
        if depth == 0:
            end = index + 1
            break

if end is None:
    raise RuntimeError("unbalanced solution RHS")

rhs = source[start:end]
if rhs.count(".Stmts") != 3:
    raise RuntimeError("unexpected number of explicit empty Stmts units")
print(rhs.replace(".Stmts", ""))
