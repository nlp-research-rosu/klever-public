#!/usr/bin/env python3
"""Extract the balanced Module(...) argument of the first #loadAll in spec.k."""

from pathlib import Path


text = Path("/tmp/audit-work/reconstruction/spec.k").read_text()
start = text.index("Module(FuncDef(", text.index("#loadAll("))

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

assert end is not None
program = text[start:end]

# `.Exprs` is the internal unit of the `List{Expr, ","}` production. The MPY
# program parser represents that same list unit with no tokens between the
# parentheses.
program = program.replace("ListExpr(.Exprs)", "ListExpr()")
print(program)
