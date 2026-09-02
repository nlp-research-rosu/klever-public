#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and SPEC.target."""

from __future__ import annotations

import re
from pathlib import Path


SOLUTION = Path("/tmp/audit-work/review/candidate-src/solution.mpy")
SPEC = Path("/tmp/audit-work/review/candidate-src/spec.k")


def match_call(text: str, name: str, start: int = 0) -> tuple[str, int, int]:
    marker = name + "("
    pos = text.find(marker, start)
    if pos < 0:
        raise AssertionError(f"missing {marker}")
    open_pos = pos + len(name)
    depth = 0
    in_string = False
    escaped = False
    for i in range(open_pos, len(text)):
        char = text[i]
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
                return text[open_pos + 1 : i], pos, i + 1
    raise AssertionError(f"unterminated {marker}")


def split_top_level(arguments: str) -> list[str]:
    parts = []
    start = 0
    depth = 0
    in_string = False
    escaped = False
    for i, char in enumerate(arguments):
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
        elif char == "," and depth == 0:
            parts.append(arguments[start:i])
            start = i + 1
    parts.append(arguments[start:])
    return parts


def normalize(term: str) -> str:
    # `.Stmts` is the explicit identity of the Stmts list; the translator
    # emits an omitted list item in the same empty branch.
    term = term.replace(".Stmts", "")
    return re.sub(r"\s+", "", term)


solution_text = SOLUTION.read_text()
spec_text = SPEC.read_text()

module_args, _, _ = match_call(solution_text, "Module")
func_args, func_start, func_end = match_call(module_args, "FuncDef")
assert not normalize(module_args[:func_start])
assert not normalize(module_args[func_end:])
function_parts = split_top_level(func_args)
assert len(function_parts) == 3, function_parts
function_name, params_term, solution_body = function_parts
params_args, _, _ = match_call(params_term, "Params")

target_pos = spec_text.index("claim [target]:")
binding_pos = spec_text.index('"how_many_times" |->', target_pos)
closure_args, closure_start, closure_end = match_call(
    spec_text, "closureVal", binding_pos
)
closure_parts = split_top_level(closure_args)
assert len(closure_parts) == 3, closure_parts
closure_params, spec_body, closure_env = closure_parts

solution_params_norm = normalize(params_args)
spec_params_norm = normalize(closure_params)
if spec_params_norm.startswith("(") and spec_params_norm.endswith(")"):
    spec_params_norm = spec_params_norm[1:-1]

checks = {
    "function_name_is_how_many_times": normalize(function_name)
    == '"how_many_times"',
    "target_binding_is_how_many_times": binding_pos < closure_start < closure_end,
    "parameter_list_equal": solution_params_norm == spec_params_norm,
    "body_constructor_term_equal_mod_empty_stmts": normalize(solution_body)
    == normalize(spec_body),
    "closure_environment_is_module_scope_zero": normalize(closure_env) == "0",
}

print(f"SOLUTION={SOLUTION}")
print(f"SPEC={SPEC}")
print(f"SOLUTION_PARAMS={solution_params_norm}")
print(f"SPEC_PARAMS={spec_params_norm}")
print(f"SOLUTION_BODY_NORMALIZED_SHA256_INPUT_LENGTH={len(normalize(solution_body))}")
print(f"SPEC_BODY_NORMALIZED_SHA256_INPUT_LENGTH={len(normalize(spec_body))}")
for name, value in checks.items():
    print(f"{name}={value}")
if not all(checks.values()):
    raise SystemExit(1)
print("PINNING_CHECK_EXIT=0")
