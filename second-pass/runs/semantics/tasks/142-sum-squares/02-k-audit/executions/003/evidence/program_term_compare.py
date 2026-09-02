#!/usr/bin/env python3
"""Constructor-level comparison of the translated program and proof macros."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


SCRATCH = Path("/tmp/audit-work/reconstruction")


def load_term(name: str) -> dict[str, Any]:
    document = json.loads((SCRATCH / name).read_text(encoding="utf-8"))
    if document.get("format") != "KAST":
        raise RuntimeError(f"{name}: not KAST JSON")
    return document["term"]


def label(term: Any) -> str | None:
    if not isinstance(term, dict) or term.get("node") != "KApply":
        return None
    return term.get("label", {}).get("name")


def descendants(term: Any) -> Iterator[dict[str, Any]]:
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from descendants(value)
    elif isinstance(term, list):
        for value in term:
            yield from descendants(value)


def stable_digest(term: Any) -> str:
    raw = json.dumps(term, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


solution = load_term("solution-kast.json")
function_macro = load_term("function-body-kast.json")
loop_macro = load_term("loop-body-kast.json")

functions = [
    term
    for term in descendants(solution)
    if (label(term) or "").startswith("FuncDef(")
]
if len(functions) != 1:
    raise RuntimeError(f"expected one FuncDef, found {len(functions)}")
function = functions[0]
function_args = function.get("args", [])
if len(function_args) != 3:
    raise RuntimeError(f"unexpected FuncDef arity: {len(function_args)}")
function_name, function_params, translated_body = function_args

function_name_token = function_name.get("token")
param_tokens = [
    term.get("token")
    for term in descendants(function_params)
    if term.get("node") == "KToken"
]

loops = [
    term
    for term in descendants(translated_body)
    if (label(term) or "").startswith("For(")
]
if len(loops) != 1:
    raise RuntimeError(f"expected one For, found {len(loops)}")
translated_loop_body = loops[0].get("args", [None, None, None])[2]

body_equal = translated_body == function_macro
loop_equal = translated_loop_body == loop_macro
binding_equal = (
    function_name_token == '"sum_squares"' and param_tokens == ['"lst"']
)

print(f"translated_function_name={function_name_token}")
print(f"translated_parameter_tokens={param_tokens}")
print(f"binding_signature_matches={binding_equal}")
print(f"translated_body_sha256={stable_digest(translated_body)}")
print(f"expanded_function_macro_sha256={stable_digest(function_macro)}")
print(f"function_body_constructor_identity={body_equal}")
print(f"translated_loop_body_sha256={stable_digest(translated_loop_body)}")
print(f"expanded_loop_macro_sha256={stable_digest(loop_macro)}")
print(f"loop_body_constructor_identity={loop_equal}")
raise SystemExit(0 if binding_equal and body_equal and loop_equal else 1)
