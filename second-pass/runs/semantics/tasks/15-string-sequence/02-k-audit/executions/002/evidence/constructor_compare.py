#!/usr/bin/env python3
"""Mechanically compare the submitted MPY constructor tree with proof macros."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/string-sequence")
DEFINITION = WORK / "audit-verification-base-kompiled"


def kast_json(arguments: list[str]) -> dict:
    completed = subprocess.run(
        ["kast", *arguments, "--output", "json"],
        cwd=WORK,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(completed.stdout)["term"]


module = kast_json(
    [
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--expand-macros",
    ]
)
body_macro = kast_json(
    [
        "--expression",
        "sequenceBody",
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION-BASE",
        "--sort",
        "Stmts",
        "--expand-macros",
    ]
)
loop_macro = kast_json(
    [
        "--expression",
        "sequenceLoopBody",
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION-BASE",
        "--sort",
        "Stmts",
        "--expand-macros",
    ]
)

# Module(FuncDef(..., BODY) .Stmts)
function = module["args"][0]["args"][0]
assert function["label"]["name"].startswith("FuncDef(")
name_token, params, submitted_body = function["args"]
assert name_token["token"] == '"string_sequence"'
assert params["args"][0]["args"][0]["token"] == '"n"'
assert submitted_body == body_macro


def find_label(term: dict, prefix: str) -> dict:
    if term.get("node") == "KApply" and term["label"]["name"].startswith(prefix):
        return term
    for argument in term.get("args", []):
        if isinstance(argument, dict):
            try:
                return find_label(argument, prefix)
            except LookupError:
                pass
    raise LookupError(prefix)


for_term = find_label(submitted_body, "For(")
submitted_loop_body = for_term["args"][2]
assert submitted_loop_body == loop_macro

print("function_binding=string_sequence")
print("parameter_constructor=Params(\"n\")")
print("submitted_body_equals_expanded_sequenceBody=yes")
print("submitted_loop_body_equals_expanded_sequenceLoopBody=yes")
