#!/usr/bin/env python3
import hashlib
import json
from pathlib import Path


ROOT = Path("/tmp/audit-work/reconstruction")


def walk(value):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def applications(tree, label_fragment):
    return [
        node
        for node in walk(tree)
        if isinstance(node, dict)
        and node.get("node") == "KApply"
        and label_fragment in node.get("label", {}).get("name", "")
    ]


solution = json.loads((ROOT / "solution.kast.json").read_text())
spec = json.loads((ROOT / "audit-spec.json").read_text())
function_defs = applications(solution, "FuncDef(_,_,_)")
closures = applications(spec, "closureVal(_,_,_)")
assert len(function_defs) == 1, len(function_defs)
assert len(closures) == 1, len(closures)

function_def = function_defs[0]
closure = closures[0]
function_name = function_def["args"][0]
function_params_wrapper = function_def["args"][1]
function_params = function_params_wrapper["args"][0]
function_body = function_def["args"][2]
closure_params = closure["args"][0]
closure_body = closure["args"][1]
closure_environment = closure["args"][2]

name_ok = function_name.get("token") == '"double_the_difference"'
params_ok = function_params == closure_params
body_ok = function_body == closure_body
environment_ok = closure_environment.get("token") == "0"

def canonical_digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


print(f"FUNCTION_DEFS_FOUND={len(function_defs)}")
print(f"ENTRY_CLOSURES_FOUND={len(closures)}")
print(f"FUNCTION_NAME_OK={name_ok} token={function_name.get('token')}")
print(f"PARAMS_CONSTRUCTOR_EQUAL={params_ok}")
print(f"BODY_CONSTRUCTOR_EQUAL={body_ok}")
print(f"FUNCTION_BODY_SHA256={canonical_digest(function_body)}")
print(f"CLAIM_CLOSURE_BODY_SHA256={canonical_digest(closure_body)}")
print(f"CLOSURE_ENVIRONMENT_ZERO={environment_ok}")
raise SystemExit(0 if name_ok and params_ok and body_ok and environment_ok else 1)
