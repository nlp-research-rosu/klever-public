#!/usr/bin/env python3
"""Mechanical KAST comparison of submitted FuncDef and claimed closure body."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/92-any-int-audit")


def load_term(name: str):
    with (SCRATCH / name).open("r", encoding="utf-8") as stream:
        return json.load(stream)["term"]


def label_name(term) -> str | None:
    if isinstance(term, dict) and term.get("node") == "KApply":
        return term["label"]["name"]
    return None


def find_apps(term, prefix: str):
    found = []
    if isinstance(term, dict):
        label = label_name(term)
        if label is not None and label.startswith(prefix):
            found.append(term)
        for value in term.values():
            found.extend(find_apps(value, prefix))
    elif isinstance(term, list):
        for value in term:
            found.extend(find_apps(value, prefix))
    return found


def token(term) -> str:
    assert term["node"] == "KToken", term
    return term["token"]


def digest(term) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


solution = load_term("solution-kast.json")
scope = load_term("scope-kast.json")
call = load_term("call-kast.json")

funcs = find_apps(solution, "FuncDef(_,_,_)")
closures = find_apps(scope, "closureVal(_,_,_)")
scope_nodes = find_apps(scope, "scope(_,_)")
map_entries = find_apps(scope, "_|->_")
calls = find_apps(call, "Call(_,_)")

assert len(funcs) == 1, len(funcs)
assert len(closures) == 1, len(closures)
assert len(scope_nodes) == 1, len(scope_nodes)
assert len(map_entries) == 1, len(map_entries)
assert len(calls) == 1, len(calls)

func = funcs[0]
closure = closures[0]
map_entry = map_entries[0]
call_node = calls[0]

func_name = token(func["args"][0])
map_name = token(map_entry["args"][0])
func_params = func["args"][1]["args"][0]
func_body = func["args"][2]
closure_params = closure["args"][0]
closure_body = closure["args"][1]
closure_location = token(closure["args"][2])
scope_parent = token(scope_nodes[0]["args"][1]["args"][0])
call_name_node = find_apps(call_node["args"][0], "Name(_)")[0]
call_name = token(call_name_node["args"][0])

checks = {
    "submitted module contains one FuncDef": len(funcs) == 1,
    "claimed scope contains one closure": len(closures) == 1,
    "function name is any_int": func_name == '"any_int"',
    "scope map key is any_int": map_name == '"any_int"',
    "expanded call resolves any_int": call_name == '"any_int"',
    "parameter constructor tree identical": func_params == closure_params,
    "body constructor tree identical": func_body == closure_body,
    "closure lexical location is module scope 0": closure_location == "0",
    "module scope parent is builtins scope -1": scope_parent == "-1",
}

for description, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} {description}")
print(f"submitted_params_sha256={digest(func_params)}")
print(f"claimed_params_sha256={digest(closure_params)}")
print(f"submitted_body_sha256={digest(func_body)}")
print(f"claimed_body_sha256={digest(closure_body)}")

raise SystemExit(0 if all(checks.values()) else 1)
