#!/usr/bin/env python3
"""Mechanical constructor/body comparison for solution.mpy and #chooseNum."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


def balanced_term(text: str, constructor: str, start: int = 0) -> str:
    marker = constructor + "("
    begin = text.index(marker, start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(begin, len(text)):
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
                return text[begin : index + 1]
    raise ValueError(f"unterminated {constructor}")


def contents(term: str) -> str:
    return term[term.index("(") + 1 : -1]


def split_top_level(text: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for index, char in enumerate(text):
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
        elif char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(text[start:index].strip())
            start = index + 1
    parts.append(text[start:].strip())
    return parts


def canonical(text: str) -> str:
    # The translator renders an empty Stmts argument as the empty surface
    # position after a comma.  verification.k spells the same list as .Stmts.
    return re.sub(r"\s+", "", text.replace(".Stmts", ""))


mpy_path = Path("/tmp/audit-work/regenerated-solution.mpy")
verification_path = Path("/tmp/audit-work/verification.k")
spec_path = Path("/tmp/audit-work/spec.k")

mpy = mpy_path.read_text()
verification = verification_path.read_text()
spec = spec_path.read_text()

module = balanced_term(mpy, "Module")
func = balanced_term(module, "FuncDef")
assert canonical(module) == canonical("Module(" + func + ")")
func_args = split_top_level(contents(func))
assert len(func_args) == 3, func_args
name, params_term, translated_body = func_args
assert name == '"choose_num"'
params = balanced_term(params_term, "Params")
translated_params = contents(params)

closure = balanced_term(verification, "closureVal")
closure_args = split_top_level(contents(closure))
assert len(closure_args) == 3, closure_args
claim_params, claim_body, defining_env = closure_args
assert claim_params.startswith("(") and claim_params.endswith(")")
claim_params = claim_params[1:-1]

body_equal = canonical(translated_body) == canonical(claim_body)
params_equal = canonical(translated_params) == canonical(claim_params)
assert body_equal
assert params_equal
assert canonical(defining_env) == "0"

bridge = balanced_term(verification, "#chooseNum")
assert canonical(bridge) == "#chooseNum(X:Int,Y:Int)"
assert "=> Call(" in verification
assert re.search(r"<env>\s*0\s*</env>", spec)
assert re.search(r"<scopeLoc>\s*1\s*</scopeLoc>", spec)
assert re.search(r"<stack>\s*\.List\s*</stack>", spec)
assert re.search(r"<ret>\s*noRet\s*</ret>", spec)

print("function_name", name)
print("translated_params", canonical(translated_params))
print("claim_closure_params", canonical(claim_params))
print("parameters_equal", params_equal)
print("translated_body_sha256", hashlib.sha256(canonical(translated_body).encode()).hexdigest())
print("claim_body_sha256", hashlib.sha256(canonical(claim_body).encode()).hexdigest())
print("constructor_body_equal", body_equal)
print("closure_defining_env", canonical(defining_env))
print("claim_initial_env", 0)
print("claim_initial_scopeLoc", 1)
print("claim_initial_stack", ".List")
print("claim_initial_ret", "noRet")
