#!/usr/bin/env python3
"""Mechanical KAST comparison between solution.mpy and proof macros."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "verification-kompiled"


def run_kast(*args: str) -> dict:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--output",
        "json",
        "--expand-macros",
        *args,
    ]
    print("COMMAND:", " ".join(command))
    result = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        capture_output=True,
        check=False,
    )
    print("EXIT_STATUS:", result.returncode)
    if result.stderr:
        print("STDERR:", result.stderr.rstrip())
    if result.returncode:
        raise SystemExit(result.returncode)
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def digest(term: dict) -> str:
    data = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


program = run_kast(str(WORK / "solution.mpy"))
assert label(program).startswith("Module(_)")
module_statements = program["args"][0]
assert label(module_statements).startswith("___")
function = module_statements["args"][0]
module_tail = module_statements["args"][1]
assert label(function).startswith("FuncDef(")
assert label(module_tail).startswith(".List")
assert function["args"][0]["token"] == '"is_happy"'
params = function["args"][1]
assert params["args"][0]["args"][0]["token"] == '"s"'
function_body = function["args"][2]

claimed_body = run_kast(
    "--expression", "isHappyBody", "--sort", "Stmts"
)
print("FUNCTION_BODY_SHA256:", digest(function_body))
print("CLAIMED_BODY_SHA256:", digest(claimed_body))
print("FUNCTION_BODY_EQUALS_CLAIMED_BODY:", function_body == claimed_body)
assert function_body == claimed_body

while_nodes: list[dict] = []


def walk(term: object) -> None:
    if isinstance(term, dict):
        if term.get("node") == "KApply" and label(term).startswith("While("):
            while_nodes.append(term)
        for value in term.values():
            walk(value)
    elif isinstance(term, list):
        for value in term:
            walk(value)


walk(function_body)
assert len(while_nodes) == 1
actual_condition, actual_loop_body = while_nodes[0]["args"]
claimed_condition = run_kast(
    "--expression", "happyLoopCondition", "--sort", "Expr"
)
claimed_loop_body = run_kast(
    "--expression", "happyLoopBody", "--sort", "Stmts"
)
print("LOOP_CONDITION_EQUALS_MACRO:", actual_condition == claimed_condition)
print("LOOP_BODY_EQUALS_MACRO:", actual_loop_body == claimed_loop_body)
assert actual_condition == claimed_condition
assert actual_loop_body == claimed_loop_body
print("CONSTRUCTOR_IDENTITY_OK")
