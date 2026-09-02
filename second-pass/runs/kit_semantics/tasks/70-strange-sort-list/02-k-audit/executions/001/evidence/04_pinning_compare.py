#!/usr/bin/env python3
"""Mechanical KAST comparison of submitted MPY and the entry claim closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


WORK = Path("/tmp/audit-work/reconstruction.tZYoqF")
SOLUTION_KAST = WORK / "solution-kast.json"
SPEC_KAST = WORK / "spec-compiled.json"


def label(node: Any) -> str | None:
    if isinstance(node, dict) and node.get("node") == "KApply":
        return node["label"]["name"]
    return None


def descendants(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from descendants(value)
    elif isinstance(node, list):
        for value in node:
            yield from descendants(value)


def unique_apply(root: Any, fragment: str) -> dict[str, Any]:
    found = [
        node
        for node in descendants(root)
        if (name := label(node)) is not None and fragment in name
    ]
    if len(found) != 1:
        raise AssertionError(f"expected one {fragment!r} node, got {len(found)}")
    return found[0]


def canonical_hash(node: Any) -> str:
    encoded = json.dumps(
        node, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


solution = json.loads(SOLUTION_KAST.read_text())
spec = json.loads(SPEC_KAST.read_text())

func = unique_apply(solution, "FuncDef(_,_,_)")
closure = unique_apply(spec, "closureVal(_,_,_)")

solution_name = func["args"][0]["token"]
solution_params = func["args"][1]["args"][0]
solution_body = func["args"][2]
claim_params = closure["args"][0]
claim_body = closure["args"][1]
captured_env = closure["args"][2]["token"]

entry_claim = spec["term"]["term"][0]["localSentences"][0]
entry_k_cell = entry_claim["body"]["args"][0]
entry_call = entry_k_cell["args"][0]["lhs"]
assert "Call(_,_)_MPY-SYNTAX_Expr_Expr_Exprs" in label(entry_call)
entry_name_node = entry_call["args"][0]
entry_name = unique_apply(entry_name_node, "Name(_)")["args"][0]["token"]

print(f"solution_name={solution_name}")
print(f"entry_call_name={entry_name}")
print(f"captured_env={captured_env}")
print(f"solution_param_hash={canonical_hash(solution_params)}")
print(f"claim_param_hash={canonical_hash(claim_params)}")
print(f"params_equal={solution_params == claim_params}")
print(f"solution_body_hash={canonical_hash(solution_body)}")
print(f"claim_body_hash={canonical_hash(claim_body)}")
print(f"body_equal={solution_body == claim_body}")

assert solution_name == '"strange_sort_list"'
assert entry_name == solution_name
assert captured_env == "0"
assert solution_params == claim_params
assert solution_body == claim_body
