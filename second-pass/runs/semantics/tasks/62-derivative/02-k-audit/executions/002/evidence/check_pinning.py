#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and derivativeClosure."""

from __future__ import annotations

import json
from pathlib import Path


def label(term: dict) -> str:
    return term["label"]["name"]


with Path("/tmp/audit-work/reconstruction/solution.ast.json").open(
    encoding="utf-8"
) as stream:
    solution = json.load(stream)["term"]
with Path("/tmp/audit-work/reconstruction/closure.ast.json").open(
    encoding="utf-8"
) as stream:
    closure = json.load(stream)["term"]

assert label(solution).startswith("Module(_)")
module_stmts = solution["args"][0]
assert label(module_stmts).startswith("___")
function, module_tail = module_stmts["args"]
assert label(function).startswith("FuncDef(_,_,_)")
assert label(module_tail).startswith(".List{")
name, params_wrapper, body = function["args"]
assert name["token"] == '"derivative"'
assert label(params_wrapper).startswith("Params(_)")
params = params_wrapper["args"][0]

assert label(closure).startswith("closureVal(_,_,_)")
closure_params, closure_body, defining_env = closure["args"]

print(f"solution_function_name={name['token']}")
print(f"module_has_exactly_one_statement={label(module_tail).startswith('.List{')}")
print(f"parameter_constructors_identical={params == closure_params}")
print(f"body_constructors_identical={body == closure_body}")
print(f"closure_defining_environment={defining_env['token']}")
print(f"solution_body_json_sha256_input_bytes={len(json.dumps(body, sort_keys=True))}")

assert params == closure_params
assert body == closure_body
assert defining_env["token"] == "0"
