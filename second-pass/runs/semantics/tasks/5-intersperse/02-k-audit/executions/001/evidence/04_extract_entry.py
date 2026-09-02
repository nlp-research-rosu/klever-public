#!/usr/bin/env python3
"""Extract the balanced Module(...) argument of the entry claim's #loadAll."""

import argparse
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument(
    "--program-surface",
    action="store_true",
    help="render K list identities as the corresponding empty program lists",
)
args = parser.parse_args()

text = Path("/tmp/audit-work/candidate/spec.k").read_text(encoding="utf-8")
marker = "#loadAll("
marker_pos = text.index(marker)
start = text.index("Module(", marker_pos + len(marker))
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
    raise RuntimeError("unbalanced Module(...) in entry claim")

term = text[start:end]
if args.program_surface:
    term = term.replace(".Exprs", "").replace(".Stmts", "")
print(term)
