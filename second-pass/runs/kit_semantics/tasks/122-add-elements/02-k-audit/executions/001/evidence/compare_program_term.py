#!/usr/bin/env python3
"""Mechanical constructor-level pinning check using K's parsed JSON terms."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def label(term: dict[str, Any]) -> str | None:
    value = term.get("label")
    return value.get("name") if isinstance(value, dict) else None


def walk(term: Any):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def canonical_hash(term: Any) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


solution_doc = json.loads(
    Path("/tmp/audit-work/122-add-elements/solution-kast.json").read_text()
)
spec_doc = json.loads(
    Path("/tmp/audit-work/122-add-elements/spec-claims.json").read_text()
)
solution_module = solution_doc["term"]

load_nodes = [
    node for node in walk(spec_doc)
    if label(node) == "#loadAll(_)_MPY-CORE_KItem_Module"
]
if len(load_nodes) != 1:
    raise SystemExit(f"expected one #loadAll node, found {len(load_nodes)}")
claim_module = load_nodes[0]["args"][0]

module_equal = solution_module == claim_module
print(f"solution_module_hash={canonical_hash(solution_module)}")
print(f"claim_loaded_module_hash={canonical_hash(claim_module)}")
print(f"module_constructor_identity={module_equal}")

function_label = "FuncDef(_,_,_)_MPY-SYNTAX_Stmt_String_Params_Stmts"
solution_functions = [
    node for node in walk(solution_module) if label(node) == function_label
]
claim_functions = [
    node for node in walk(spec_doc) if label(node) == function_label
]
print(f"solution_function_nodes={len(solution_functions)}")
print(f"claim_function_nodes={len(claim_functions)}")
if len(solution_functions) != 1:
    raise SystemExit("solution should contain exactly one function")

source_function = solution_functions[0]
same_function_count = sum(node == source_function for node in claim_functions)
print(f"claim_nodes_identical_to_solution_function={same_function_count}")

closure_label = "closureVal(_,_,_)_MPY-CORE_Val_ParamNames_Stmts_Int"
closures = [node for node in walk(spec_doc) if label(node) == closure_label]
matching_closures = 0
for closure in closures:
    params_and_body_equal = (
        closure["args"][0] == source_function["args"][1]["args"][0]
        and closure["args"][1] == source_function["args"][2]
    )
    matching_closures += int(params_and_body_equal)
print(f"claim_closure_nodes={len(closures)}")
print(f"closures_with_source_params_and_body={matching_closures}")

success = module_equal and same_function_count >= 1 and matching_closures >= 1
print(f"REAL_PROGRAM_PINNING={'PASS' if success else 'FAIL'}")
raise SystemExit(0 if success else 1)
