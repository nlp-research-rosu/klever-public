#!/usr/bin/env python3
"""Extract the balanced Module(...) term executed by SPEC.histogram."""

from __future__ import annotations

from pathlib import Path


source_path = Path("/tmp/audit-work/111-histogram-audit/spec.k")
output_path = Path("/tmp/audit-work/111-histogram-audit/claim-program.mpy")
normalized_path = Path(
    "/tmp/audit-work/111-histogram-audit/claim-program.normalized.mpy"
)
text = source_path.read_text(encoding="utf-8")
claim_start = text.index("claim [histogram]:")
start = text.index("Module(", claim_start)

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

assert end is not None
term = text[start:end] + "\n"
output_path.write_text(term, encoding="utf-8")
entries_units = term.count(".Entries")
statement_units = term.count(".Stmts")
normalized = term.replace(".Entries", "").replace(".Stmts", "")
normalized_path.write_text(normalized, encoding="utf-8")
print(f"extracted bytes: {len(term.encode('utf-8'))}")
print(f"output: {output_path}")
print(
    "surface normalization: "
    f"removed {entries_units} explicit .Entries unit and "
    f"{statement_units} explicit .Stmts units"
)
print(f"normalized output: {normalized_path}")
