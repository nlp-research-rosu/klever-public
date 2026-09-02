#!/usr/bin/env python3
"""Extract the Module(...) argument embedded in #runRescale's #loadAll."""

from pathlib import Path

source = Path(
    "/tmp/audit-work/21-rescale-to-unit-audit/verification.k"
).read_text()
anchor = source.index("=> #loadAll(")
start = source.index("Module(", anchor)

depth = 0
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
            end = index + 1
            break

if end is None:
    raise RuntimeError("unterminated Module(...) term")

term = source[start:end] + "\n"
output = Path(
    "/tmp/audit-work/21-rescale-to-unit-audit/extracted-claim-program.mpy"
)
output.write_text(term)
print(f"source_offset={start}:{end}")
print(f"wrote={output}")
print(term)

# `.ParamNames` is the K-source spelling of the List{String,","} unit. The
# external program parser spells the same unit as an empty argument list.
normalized = term.replace("FreeVars(.ParamNames)", "FreeVars()")
normalized_output = output.with_name("extracted-claim-program-normalized.mpy")
normalized_output.write_text(normalized)
print(f"wrote={normalized_output}")
