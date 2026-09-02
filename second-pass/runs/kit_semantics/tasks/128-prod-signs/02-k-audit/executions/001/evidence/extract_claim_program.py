#!/usr/bin/env python3
"""Extract the balanced Module(...) argument of SPEC's first #loadAll."""

from pathlib import Path


source = Path("/tmp/audit-work/128-prod-signs/spec.k").read_text()
marker = "#loadAll("
start = source.index(marker) + len(marker)
while source[start].isspace():
    start += 1
assert source.startswith("Module(", start)

depth = 0
in_string = False
escaped = False
end = None
for index in range(start, len(source)):
    character = source[index]
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
program = source[start:end] + "\n"
output = Path("/tmp/audit-work/128-prod-signs/spec-claim-program.mpy")
output.write_text(program)
normalized = Path(
    "/tmp/audit-work/128-prod-signs/spec-claim-program-normalized.mpy"
)
# `.Stmts` is the associative Stmts unit used explicitly in K claims.  It is
# not part of the surface-program scanner and is semantically inert.
normalized.write_text(program.replace(".Stmts", ""))
print(f"EXTRACTED={output}")
print(f"NORMALIZED={normalized} TRANSFORMATION=remove_Stmts_unit_tokens")
print(f"BYTES={len(program.encode())}")
