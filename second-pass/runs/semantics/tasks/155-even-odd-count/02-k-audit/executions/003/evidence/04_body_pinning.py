#!/usr/bin/env python3
"""Mechanical constructor-level pinning check for the submitted function."""

import hashlib
import json
import subprocess
from pathlib import Path


DEFINITION = "/tmp/audit-work/fresh/verification-base-kompiled"
MODULE = "EVEN-ODD-VERIFICATION"


def kast(path: str, sort: str):
    command = [
        "kast",
        path,
        "--definition",
        DEFINITION,
        "--module",
        MODULE,
        "--sort",
        sort,
        "--expand-macros",
        "--output",
        "json",
    ]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    return json.loads(completed.stdout)["term"]


def label(term):
    if term.get("node") != "KApply":
        return None
    return term["label"]["name"]


def descendants(term):
    yield term
    for argument in term.get("args", []):
        yield from descendants(argument)


program = kast("/tmp/audit-work/fresh/regenerated-solution.mpy", "Module")
body_macro = kast("/audit-output/evidence/04_macro_term.mpy", "Stmts")
scope_macro = kast("/audit-output/evidence/04_scope_term.mpy", "Scope")

function_nodes = [
    term for term in descendants(program)
    if (label(term) or "").startswith("FuncDef(_,_,_)_")
]
assert len(function_nodes) == 1
function = function_nodes[0]
name, params, body = function["args"]
assert name["token"] == '"even_odd_count"'
assert body == body_macro

scope_nodes = [term for term in descendants(scope_macro) if (label(term) or "").startswith("scope(_,_)_")]
closure_nodes = [term for term in descendants(scope_macro) if (label(term) or "").startswith("closureVal(")]

assert len(scope_nodes) == 1
assert len(closure_nodes) == 1
scope = scope_nodes[0]
closure = closure_nodes[0]
assert scope["args"][0]["label"]["name"] == "_|->_"
assert scope["args"][0]["args"][0]["token"] == '"even_odd_count"'
assert scope["args"][0]["args"][1] == closure
assert scope["args"][1]["label"]["name"].startswith("parent(_)_")
assert scope["args"][1]["args"][0]["token"] == "-1"
assert closure["args"][0] == params["args"][0]
assert closure["args"][1] == body
assert closure["args"][2]["token"] == "0"

def digest(term):
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


print("functions_in_regenerated_module=1")
print("entry_name=even_odd_count")
print("params_match=True")
print("body_macro_matches_regenerated_body=True")
print("module_scope_closure_matches_name_params_body_and_defenv=True")
print(f"body_kast_sha256={digest(body)}")
print(f"macro_body_kast_sha256={digest(body_macro)}")
