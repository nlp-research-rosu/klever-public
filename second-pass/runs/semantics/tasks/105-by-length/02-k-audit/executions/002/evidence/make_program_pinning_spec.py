#!/usr/bin/env python3
"""Derive a K body-identity claim directly from regenerated solution.mpy."""

from pathlib import Path


SCRATCH = Path("/tmp/audit-work/105-by-length/recon")


def matching_close(text: str, opening: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(opening, len(text)):
        character = text[index]
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
                return index
    raise ValueError("unbalanced constructor term")


def top_level_arguments(text: str) -> list[str]:
    arguments: list[str] = []
    start = 0
    depth = 0
    quoted = False
    escaped = False
    for index, character in enumerate(text):
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
        elif character == "," and depth == 0:
            arguments.append(text[start:index].strip())
            start = index + 1
    arguments.append(text[start:].strip())
    return arguments


program = (SCRATCH / "regenerated-solution.mpy").read_text(encoding="utf-8")
function_start = program.index('FuncDef("by_length"')
opening = program.index("(", function_start)
closing = matching_close(program, opening)
arguments = top_level_arguments(program[opening + 1 : closing])
assert arguments[0] == '"by_length"'
assert arguments[1] == 'Params("arr")'
body = arguments[2]
assert body.count("ListExpr()") == 2
assert body.count(",\n        ))") == 1
# The external .mpy parser accepts omitted empty list arguments. Inline K
# claims require the corresponding explicit list-unit constructors.
body = body.replace("ListExpr()", "ListExpr(.Exprs)")
body = body.replace(",\n        ))", ",\n        .Stmts))")

def configured_claim(label: str, left: str, right: str) -> str:
    return f'''  claim [{label}]:
    <k>
{left}
    =>
{right}
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
'''


spec = f'''requires "verification.k"

module PROGRAM-PINNING-SPEC
  imports BY-LENGTH-VERIFICATION

{configured_claim(
    "body-constructor-identity",
    "      byLengthBody",
    body,
)}
{configured_claim(
    "closure-constructor-identity",
    "      byLengthClosure",
    f'      closureVal("arr", {body}, 0)',
)}
endmodule
'''
(SCRATCH / "program-pinning-spec.k").write_text(spec, encoding="utf-8")
print(f"WROTE: {SCRATCH / 'program-pinning-spec.k'}")
print("DERIVATION: regenerated-solution.mpy FuncDef third constructor argument")
print("NORMALIZATION: ListExpr() -> ListExpr(.Exprs); omitted If else -> .Stmts")
print(f"BODY_BYTES: {len(body.encode())}")
