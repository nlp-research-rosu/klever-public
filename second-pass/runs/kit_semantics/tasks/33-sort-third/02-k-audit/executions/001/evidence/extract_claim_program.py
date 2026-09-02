#!/usr/bin/env python3
"""Extract the first Module(...) term executed under #loadAll in SPEC.sort-third."""

from __future__ import annotations

import pathlib


SPEC = pathlib.Path("/tmp/audit-work/33-sort-third/spec.k")
OUTPUT = pathlib.Path("/tmp/audit-work/33-sort-third/claimed-program.mpy")
RULE_OUTPUT = pathlib.Path("/tmp/audit-work/33-sort-third/claimed-program.rule")


text = SPEC.read_text(encoding="utf-8")
load_start = text.index("#loadAll(")
start = text.index("Module(", load_start)
depth = 0
quote = False
escaped = False
end = None
for index in range(start, len(text)):
    character = text[index]
    if quote:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == '"':
            quote = False
        continue
    if character == '"':
        quote = True
    elif character == "(":
        depth += 1
    elif character == ")":
        depth -= 1
        if depth == 0:
            end = index + 1
            break

assert end is not None
program = text[start:end] + "\n"
OUTPUT.write_text(program, encoding="utf-8")
RULE_OUTPUT.write_text(f"{program.strip()} => {program.strip()}\n", encoding="utf-8")
print(f"source={SPEC}")
print(f"start_offset={start}")
print(f"end_offset={end}")
print(f"output={OUTPUT}")
print(f"rule_output={RULE_OUTPUT}")
print(f"characters={len(program)}")
