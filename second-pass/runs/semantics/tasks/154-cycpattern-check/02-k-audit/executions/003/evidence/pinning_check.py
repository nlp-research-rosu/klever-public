#!/usr/bin/env python3
"""Mechanical KAST comparison of translated function and claimed closure body."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk(value)


def label_name(node: dict) -> str | None:
    label = node.get("label")
    return label.get("name") if isinstance(label, dict) else None


def unique_label(root, prefix: str) -> dict:
    matches = [
        node
        for node in walk(root)
        if isinstance(label_name(node), str) and label_name(node).startswith(prefix)
    ]
    if len(matches) != 1:
        raise AssertionError(f"{prefix}: expected one node, found {len(matches)}")
    return matches[0]


def digest(node) -> str:
    encoded = json.dumps(node, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def token(node: dict) -> str:
    if node.get("node") != "KToken":
        raise AssertionError(f"expected KToken, got {node}")
    return node["token"]


def main() -> int:
    program = json.loads(Path("/tmp/audit-work/fresh/solution-kast.json").read_text())["term"]
    claim = json.loads(Path("/tmp/audit-work/fresh/audit-spec.json").read_text())["term"]

    function = unique_label(program, "FuncDef(_,_,_)")
    closure = unique_label(claim, "closureVal(_,_,_)")
    call = unique_label(claim, "Call(_,_)")
    summary = unique_label(claim, "rotationsLoop(_,_,_)")

    function_name = token(function["args"][0])
    call_name_node = call["args"][0]
    if not label_name(call_name_node).startswith("Name(_)"):
        raise AssertionError("entry redex does not call a Name")
    call_name = token(call_name_node["args"][0])

    function_params = function["args"][1]["args"][0]
    closure_params = closure["args"][0]
    function_body = function["args"][2]
    closure_body = closure["args"][1]

    checks = {
        "function_name_is_cycpattern_check": function_name == '"cycpattern_check"',
        "call_name_matches_function": call_name == function_name,
        "parameter_constructor_identity": function_params == closure_params,
        "body_constructor_identity": function_body == closure_body,
        "entry_has_rotationsLoop_summary": summary is not None,
    }
    print(f"function_name={function_name}")
    print(f"call_name={call_name}")
    print(f"translated_params_sha256={digest(function_params)}")
    print(f"claimed_params_sha256={digest(closure_params)}")
    print(f"translated_body_sha256={digest(function_body)}")
    print(f"claimed_body_sha256={digest(closure_body)}")
    for name, result in checks.items():
        print(f"{name}={result}")
    final = all(checks.values())
    print(f"MECHANICAL_PINNING_CHECK={'PASS' if final else 'FAIL'}")
    return 0 if final else 1


if __name__ == "__main__":
    raise SystemExit(main())
