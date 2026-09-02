#!/usr/bin/env python3
"""Mechanical constructor-level comparison of translated function and claim."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path


def extract_call(text: str, constructor: str, start: int = 0) -> str:
    pos = text.index(constructor + "(", start)
    depth = 0
    quoted = False
    escaped = False
    for i in range(pos + len(constructor), len(text)):
        ch = text[i]
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[pos : i + 1]
    raise ValueError(f"unbalanced {constructor}")


def split_args(call: str) -> list[str]:
    inner = call[call.index("(") + 1 : -1]
    out: list[str] = []
    depth = 0
    quoted = False
    escaped = False
    mark = 0
    for i, ch in enumerate(inner):
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            out.append(inner[mark:i].strip())
            mark = i + 1
    out.append(inner[mark:].strip())
    return out


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


translated = Path("/tmp/audit-work/fresh/regenerated-solution.mpy").read_text()
spec = Path("/tmp/audit-work/fresh/spec.k").read_text()

function = extract_call(translated, "FuncDef")
function_args = split_args(function)
assert len(function_args) == 3, function_args
name, params_call, body = function_args
params = split_args(params_call)
assert params_call.startswith("Params(")
assert len(params) == 1

claim_closure = extract_call(spec, "closureVal")
expected_closure = (
    f"closureVal(({params[0]}, .ParamNames), ({body} .Stmts), 0)"
)

assert name == '"truncate_number"'
assert compact(claim_closure) == compact(expected_closure)
assert '"truncate_number" <-' in spec
assert compact('Expr(Str("HumanEval solution for returning the fractional part of a float."))') in compact(translated)

print("translated_function", compact(function))
print("expected_claim_closure", compact(expected_closure))
print("actual_claim_closure", compact(claim_closure))
print("FUNCTION_NAME_MATCH true")
print("PARAMETER_CONSTRUCTOR_MATCH true")
print("BODY_CONSTRUCTOR_MATCH true")
print("DEFINING_ENV_MATCH 0")
print("DOCSTRING_PREFIX_PRESENT true")
print("CONSTRUCTOR_PINNING_EXIT 0")


def load(path: str, name: str):
    module_spec = importlib.util.spec_from_file_location(name, path)
    if module_spec is None or module_spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


canonical = load("/reference/canonical.py", "canonical_witness")
candidate = load("/tmp/audit-work/fresh/solution.py", "candidate_witness")
for value in (0.5, 1.0, 3.5, 123.875):
    expected = canonical.truncate_number(value)
    actual = candidate.truncate_number(value)
    print(
        "WITNESS",
        repr(value),
        "canonical",
        repr(expected),
        "candidate",
        repr(actual),
        "claimed_term",
        f"floatMod({value!r}, 1.0)",
    )
    assert actual == expected

