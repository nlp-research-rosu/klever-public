#!/usr/bin/env python3
"""Compare the translated function body with the closure executed by the claim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


EVIDENCE = Path("/audit-output/evidence")


def walk(term: Any) -> Iterator[dict[str, Any]]:
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def label(node: dict[str, Any]) -> str | None:
    value = node.get("label")
    if isinstance(value, dict):
        return value.get("name")
    return None


def stable_hash(term: Any) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


program = json.loads((EVIDENCE / "fresh-program-kast.json").read_text())
specification = json.loads((EVIDENCE / "fresh-spec-kast.json").read_text())

function_nodes = [
    node
    for node in walk(program["term"])
    if (label(node) or "").startswith("FuncDef(_,_,_)_")
]
if len(function_nodes) != 1:
    raise SystemExit(f"expected one translated FuncDef, found {len(function_nodes)}")
function = function_nodes[0]
function_name, function_params, function_body = function["args"]
if not (label(function_params) or "").startswith("Params(_)_"):
    raise SystemExit("translated function lacks the semantics' Params constructor")
normalized_function_params = function_params["args"][0]

correct_claims = [
    node
    for node in walk(specification["term"])
    if node.get("node") == "KClaim"
    and node.get("att", {}).get("att", {}).get("label")
    == "FIBFIB-SPEC.fibfib-correct"
]
if len(correct_claims) != 1:
    raise SystemExit(f"expected one fibfib-correct claim, found {len(correct_claims)}")
claim = correct_claims[0]
closures = [
    node
    for node in walk(claim["body"])
    if (label(node) or "").startswith("closureVal(_,_,_)_")
]
if len(closures) != 1:
    raise SystemExit(f"expected one closure in entry claim, found {len(closures)}")
closure_params, closure_body, closure_environment = closures[0]["args"]

calls = [
    node
    for node in walk(claim["body"])
    if (label(node) or "").startswith("Call(_,_)_")
]
summaries = [
    node
    for node in walk(claim["body"])
    if (label(node) or "").startswith("fibFrom(_,_,_,_)_")
]

name_ok = function_name.get("token") == '"fibfib"'
params_equal = normalized_function_params == closure_params
body_equal = function_body == closure_body
closure_env_ok = closure_environment.get("token") == "0"

print(f"translated_function_count={len(function_nodes)}")
print(f"translated_name={function_name.get('token')} name_ok={name_ok}")
print("params_normalization=removed exact Params(_) wrapper consumed by functions.k:14")
print(f"params_equal={params_equal}")
print(f"body_equal={body_equal}")
print(f"closure_environment={closure_environment.get('token')} env_ok={closure_env_ok}")
print(f"function_params_surface_sha256={stable_hash(function_params)}")
print(f"function_params_normalized_sha256={stable_hash(normalized_function_params)}")
print(f"closure_params_sha256={stable_hash(closure_params)}")
print(f"function_body_sha256={stable_hash(function_body)}")
print(f"closure_body_sha256={stable_hash(closure_body)}")
print(f"entry_call_count={len(calls)}")
print(f"fibFrom_occurrence_count_in_entry_claim={len(summaries)}")

if not (
    name_ok
    and params_equal
    and body_equal
    and closure_env_ok
    and len(calls) == 1
    and len(summaries) >= 1
):
    raise SystemExit("constructor-level pinning check failed")
