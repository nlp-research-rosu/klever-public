#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the entry claim."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path("/tmp/audit-work/proof")


def compact(text: str) -> str:
    without_comments = re.sub(r"//.*", "", text)
    result = re.sub(r"\s+", "", without_comments)
    # The parser's empty Exprs list may be written implicitly as `()`.
    return result.replace("ListExpr()", "ListExpr(.Exprs)")


def balanced(text: str, start: int) -> str:
    opening = text.find("(", start)
    assert opening >= 0
    depth = 0
    in_string = False
    escaped = False
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
                return text[start : index + 1]
    raise AssertionError("unbalanced constructor term")


solution = compact((ROOT / "solution.mpy").read_text(encoding="utf-8"))
spec = compact((ROOT / "spec.k").read_text(encoding="utf-8"))

entry_start = spec.index("#loadAll(Module(") + len("#loadAll(")
claim_module = balanced(spec, entry_start)
assert solution == claim_module

solution_func_start = solution.index('FuncDef("rescale_to_unit"')
solution_func = balanced(solution, solution_func_start)
params_end = solution_func.index('Params("numbers"),') + len('Params("numbers"),')
solution_body = solution_func[params_end:-1]

closure_start = spec.index('closureVal(("numbers",.ParamNames),')
closure = balanced(spec, closure_start)
closure_prefix = 'closureVal(("numbers",.ParamNames),'
assert closure.startswith(closure_prefix) and closure.endswith(",0)")
closure_body = closure[len(closure_prefix):-3]
assert solution_body == closure_body

print("module_constructor_identity=yes")
print("function_binding=rescale_to_unit")
print("parameter_identity=numbers")
print("closure_body_identity=yes")
print("normalization=whitespace/comments removed; ListExpr() == ListExpr(.Exprs)")
print(f"normalized_module_sha256={hashlib.sha256(solution.encode()).hexdigest()}")
print(f"normalized_body_sha256={hashlib.sha256(solution_body.encode()).hexdigest()}")
