#!/usr/bin/env python3
"""Independent constructor-level identity check for the submitted MPY body."""

from pathlib import Path


def compact_k(text: str) -> str:
    out = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    if in_string:
        raise ValueError("unterminated string")
    return "".join(out)


def constructor_args(text: str, start: int, name: str):
    prefix = name + "("
    if not text.startswith(prefix, start):
        raise ValueError(f"expected {prefix!r} at offset {start}")
    args = []
    arg_start = start + len(prefix)
    depth = 0
    in_string = False
    escaped = False
    for index in range(arg_start, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            if depth == 0:
                args.append(text[arg_start:index])
                return args, index + 1
            depth -= 1
        elif char == "," and depth == 0:
            args.append(text[arg_start:index])
            arg_start = index + 1
    raise ValueError(f"unterminated {name}")


submitted = compact_k(
    Path("/tmp/audit-work/36-fizz-buzz/candidate-source/solution.mpy").read_text()
)
module_args, module_end = constructor_args(submitted, 0, "Module")
if module_end != len(submitted) or len(module_args) != 1:
    raise SystemExit("submitted Module is not exactly one function statement")
function_args, function_end = constructor_args(module_args[0], 0, "FuncDef")
if function_end != len(module_args[0]) or len(function_args) != 3:
    raise SystemExit("submitted function constructor has an unexpected shape")
if function_args[:2] != ['"fizz_buzz"', 'Params("n")']:
    raise SystemExit("submitted function name/parameters differ from the contract")

spec = compact_k(Path("/tmp/audit-work/36-fizz-buzz/spec.k").read_text())
closure_offsets = []
cursor = 0
while True:
    found = spec.find("closureVal(", cursor)
    if found < 0:
        break
    closure_offsets.append(found)
    cursor = found + 1
if len(closure_offsets) != 1:
    raise SystemExit(f"expected one entry closure, found {len(closure_offsets)}")
closure_args, _ = constructor_args(spec, closure_offsets[0], "closureVal")
if len(closure_args) != 3 or closure_args[0] != '"n"' or closure_args[2] != "0":
    raise SystemExit("entry closure parameters or defining environment differ")

submitted_body = function_args[2]
claim_body = closure_args[1]
if submitted_body.count(".Stmts") != 0:
    raise SystemExit("unexpected explicit .Stmts in submitted body")
if claim_body.count(".Stmts") != 1:
    raise SystemExit("expected exactly one explicit empty else branch in claim body")
if ",.Stmts))" not in claim_body:
    raise SystemExit("the explicit .Stmts is not the If empty-else argument")
if claim_body.replace(".Stmts", "") != submitted_body:
    raise SystemExit("claim closure body is not constructor-identical after empty-list normalization")

required_entry_fragments = [
    '<k>Call(Name("fizz_buzz"),Int(N:Int))=>?R:Int</k>',
    '<env>0</env>',
    '"fizz_buzz"|->closureVal(',
    "parent(-1)",
    "-1|->builtinsScope",
    "<scopeLoc>1</scopeLoc>",
    "<heap>.Map</heap>",
    "<heapLoc>0</heapLoc>",
    "<stack>.List</stack>",
    "<ret>noRet</ret>",
    "<exc>NoExc</exc>",
    "<exit-code>0</exit-code>",
    "ensures?R==IntfizzResult(0,N)",
]
missing = [fragment for fragment in required_entry_fragments if fragment not in spec]
if missing:
    raise SystemExit(f"entry configuration is missing fragments: {missing}")

audit_module = compact_k(
    Path("/tmp/audit-work/36-fizz-buzz/audit-concrete-tests.mpy").read_text()
)
audit_function_start = audit_module.find('FuncDef("fizz_buzz",')
audit_function_args, _ = constructor_args(audit_module, audit_function_start, "FuncDef")
if audit_function_args != function_args:
    raise SystemExit("fresh concrete test does not execute the submitted function constructor")

print("submitted_module_shape=one FuncDef")
print('entry_signature=FuncDef("fizz_buzz", Params("n"), BODY)')
print("claim_closure_count=1 defining_environment=0")
print("normalization=one explicit .Stmts empty If-else unit")
print("claim_body_constructor_identity=PASS")
print("fresh_concrete_body_constructor_identity=PASS")
print("entry_call_and_observable_cells_pinned=PASS")
