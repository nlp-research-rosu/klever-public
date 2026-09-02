#!/usr/bin/env python3
"""Mechanical constructor/body comparisons for the submitted program and claims."""

from __future__ import annotations

from pathlib import Path


ROOT = Path("/tmp/audit-work/candidate")


def matching_paren(text: str, open_at: int) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"unbalanced constructor at offset {open_at}")


def constructor_args(text: str, constructor: str, start: int = 0) -> tuple[list[str], int, int]:
    token = constructor + "("
    head = text.index(token, start)
    open_at = head + len(constructor)
    close_at = matching_paren(text, open_at)
    inside = text[open_at + 1 : close_at]
    args: list[str] = []
    depth = 0
    quoted = False
    escaped = False
    arg_start = 0
    for index, char in enumerate(inside):
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(inside[arg_start:index])
            arg_start = index + 1
    args.append(inside[arg_start:])
    return args, head, close_at


def compact(text: str) -> str:
    out: list[str] = []
    quoted = False
    escaped = False
    for char in text:
        if quoted:
            out.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            out.append(char)
        elif not char.isspace():
            out.append(char)
    return "".join(out)


mpy = (ROOT / "solution.mpy").read_text()
spec = (ROOT / "spec.k").read_text()
verification = (ROOT / "verification.k").read_text()

module_args, _, _ = constructor_args(mpy, "Module")
func_args, _, _ = constructor_args(module_args[0], "FuncDef")
closure_args, _, _ = constructor_args(spec, "closureVal")

if len(func_args) != 3:
    raise AssertionError(f"submitted FuncDef has {len(func_args)} args")
if len(closure_args) != 3:
    raise AssertionError(f"claim closureVal has {len(closure_args)} args")

mpy_body = compact(func_args[2])
claim_body = compact(closure_args[1])
print(f"submitted_function_name={compact(func_args[0])}")
print(f"submitted_params={compact(func_args[1])}")
print(f"claim_params={compact(closure_args[0])}")
print(f"submitted_body={mpy_body}")
print(f"claim_body={claim_body}")
print(f"function_body_constructor_identity={mpy_body == claim_body}")

spec_loop_args, _, _ = constructor_args(spec, "#loop")
rule_loop_args, _, _ = constructor_args(verification, "#loop")
spec_loop = compact(",".join(spec_loop_args))
rule_loop = compact(",".join(rule_loop_args))
print(f"loop_claim_term={spec_loop}")
print(f"promoted_loop_rule_term={rule_loop}")
print(f"loop_term_identity={spec_loop == rule_loop}")

required_fixed_rules = {
    "module_load": (
        ROOT / "reference-semantics/semantics/core.k",
        "#loadAll(Module(SS:Stmts)) => SS",
    ),
    "import_noop": (
        ROOT / "reference-semantics/semantics/float.k",
        "Import(_:String) => .K",
    ),
    "function_binding": (
        ROOT / "reference-semantics/semantics/functions.k",
        "FuncDef(F:String, Params(PNS:ParamNames), BODY:Stmts) => .K",
    ),
    "closure_call": (
        ROOT / "reference-semantics/semantics/call.k",
        "#applyK(toCall(closureVal(PNS:ParamNames, BODY:Stmts, DEFL:Int)), ACC:Vals",
    ),
}
for name, (path, needle) in required_fixed_rules.items():
    present = needle in path.read_text()
    print(f"fixed_rule_{name}={present} source={path}")
    if not present:
        raise AssertionError(f"missing fixed rule {name}")

if mpy_body != claim_body or spec_loop != rule_loop:
    raise SystemExit(1)
