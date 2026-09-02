#!/usr/bin/env python3
"""Extract decode_cyclic's constructor-level Stmts term from regenerated MPY."""

from __future__ import annotations

from pathlib import Path


scratch = Path("/tmp/audit-work/38-decode-cyclic")
text = (scratch / "solution.regenerated.mpy").read_text(encoding="utf-8")
needle = 'FuncDef("decode_cyclic", Params("s"),'
start = text.index(needle) + len(needle)

# The FuncDef call's third argument is a Stmts term. Find the closing
# parenthesis of this FuncDef while respecting quoted K String tokens.
depth = 1  # the already-open FuncDef(
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
    raise RuntimeError("unterminated decode_cyclic FuncDef")

body = text[start:end].strip()
(scratch / "decode-body-from-regeneration.mpy").write_text(body + "\n", encoding="utf-8")
(scratch / "decode-body-macro.mpy").write_text("decodeBody\n", encoding="utf-8")
print(f"extracted_bytes={len(body.encode('utf-8'))}")
print(f"source_offset={start}:{end}")
