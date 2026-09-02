#!/usr/bin/env python3
"""Extract the Module argument of the whole-program claim's #loadAll term."""

import re
from pathlib import Path


source = Path("/tmp/audit-work/reconstruction/spec.k").read_text(encoding="utf-8")
marker = "#loadAll("
marker_index = source.find(marker)
if marker_index < 0:
    raise SystemExit("missing #loadAll term")

start = marker_index + len(marker)
depth = 1
quoted = False
escaped = False
end = None
for index in range(start, len(source)):
    character = source[index]
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
            end = index
            break

if end is None:
    raise SystemExit("unbalanced #loadAll term")

program = source[start:end].strip() + "\n"
# The trusted translator renders an empty Stmts list as an empty constructor
# field, while rule syntax admits the equivalent explicit `.Stmts` token.
program, normalized_empty_stmts = re.subn(r",\s*\.Stmts\)", ",)", program)
output = Path("/tmp/audit-work/reconstruction/spec_program.mpy")
output.write_text(program, encoding="utf-8")
print(f"extracted={output}")
print(f"characters={len(program)}")
print(f"normalized_explicit_empty_stmts={normalized_empty_stmts}")
