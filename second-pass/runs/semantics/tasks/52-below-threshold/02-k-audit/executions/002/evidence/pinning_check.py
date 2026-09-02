#!/usr/bin/env python3
"""Mechanical KAST comparison of submitted FuncDef and executed closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/52-below-threshold")


def term(path: Path) -> dict:
    return json.loads(path.read_text())["term"]


def label(node: dict) -> str:
    return node.get("label", {}).get("name", "")


def args(node: dict) -> list[dict]:
    return node.get("args", [])


def token(node: dict) -> str:
    return node.get("token", "")


def digest(node: dict) -> str:
    data = json.dumps(node, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


module = term(SCRATCH / "solution-expanded.json")
call = term(SCRATCH / "call-expanded.json")

assert label(module).startswith("Module(_)")
module_statements = args(module)[0]
assert label(module_statements).startswith("___")
function = args(module_statements)[0]
assert label(function).startswith("FuncDef(_,_,_)")
function_name, function_params, function_body = args(function)
assert label(function_params).startswith("Params(_)")
function_param_names = args(function_params)[0]

assert label(call).startswith("Call(_,_)")
callee, call_arguments = args(call)
assert label(callee).startswith("closureVal(_,_,_)")
closure_params, closure_body, closure_env = args(callee)

checks = {
    "function_name_is_below_threshold": token(function_name) == '"below_threshold"',
    "parameter_constructors_identical": function_param_names == closure_params,
    "body_constructors_identical": function_body == closure_body,
    "closure_environment_is_module_zero": token(closure_env) == "0",
    "call_has_two_arguments": label(call_arguments).startswith("_,__"),
}

print("submitted_funcdef_label=", label(function))
print("executed_callee_label=", label(callee))
print("submitted_function_name=", token(function_name))
print("submitted_params_sha256=", digest(function_param_names))
print("executed_params_sha256=", digest(closure_params))
print("submitted_body_sha256=", digest(function_body))
print("executed_body_sha256=", digest(closure_body))
for name, result in checks.items():
    print(f"{name}={result}")
if not all(checks.values()):
    raise SystemExit(1)
