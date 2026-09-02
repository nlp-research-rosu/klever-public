#!/usr/bin/env python3
"""Mechanical KAST comparison of translated function body and claimed closure."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/reconstruction")
DEFINITION = SCRATCH / "audit-verification-kompiled"
SOLUTION = SCRATCH / "regenerated-solution.mpy"
SPEC = SCRATCH / "spec.k"


def find_matching_parenthesis(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
        character = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return index
    raise AssertionError("unbalanced closure term in spec.k")


def parse_program(path: Path) -> dict:
    completed = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--input",
            "program",
            "--output",
            "json",
        ],
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(completed.stdout)["term"]


def parse_expression(expression: str) -> dict:
    completed = subprocess.run(
        [
            "kast",
            "--expression",
            expression,
            "--definition",
            str(DEFINITION),
            "--input",
            "program",
            "--output",
            "json",
            "--module",
            "VERIFICATION",
            "--sort",
            "Expr",
        ],
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(completed.stdout)["term"]


def label(term: dict) -> str:
    if term.get("node") != "KApply":
        return ""
    return str(term.get("label", {}).get("name", ""))


def walk(term: object):
    if isinstance(term, dict):
        yield term
        for argument in term.get("args", []):
            yield from walk(argument)
    elif isinstance(term, list):
        for item in term:
            yield from walk(item)


spec_text = SPEC.read_text(encoding="utf-8")
function_section = spec_text.split("claim [function-correct]:", 1)[1]
binding_marker = '"separate_paren_groups" |->'
assert binding_marker in function_section
closure_start = function_section.index("closureVal(")
opening = function_section.index("(", closure_start)
closure_end = find_matching_parenthesis(function_section, opening)
closure_text = function_section[closure_start : closure_end + 1]
# Program-parser list notation elides explicit unit tails that the K-rule parser
# accepts for disambiguation. Removing these units does not remove a statement
# or expression; each surrounding singleton/list production re-inserts its unit.
closure_program_text = closure_text.replace(".Stmts", "").replace(".Exprs", "")
solution_kast = parse_program(SOLUTION)
claimed_closure_kast = parse_expression(closure_program_text)

funcdefs = [
    term
    for term in walk(solution_kast)
    if label(term).startswith("FuncDef(_,_,_)_MPY-SYNTAX")
]
closures = [
    term
    for term in walk(claimed_closure_kast)
    if label(term).startswith("closureVal(")
]
assert len(funcdefs) == 1, len(funcdefs)
assert len(closures) == 1, len(closures)

funcdef = funcdefs[0]
closure = closures[0]
function_name, params_wrapper, translated_body = funcdef["args"]
translated_params = params_wrapper["args"][0]
claimed_params, claimed_body, defining_scope = closure["args"]

name_is_target = function_name.get("token") == '"separate_paren_groups"'
params_equal = translated_params == claimed_params
body_equal = translated_body == claimed_body
scope_is_zero = defining_scope.get("token") == "0"

canonical_body = json.dumps(
    translated_body, sort_keys=True, separators=(",", ":")
).encode()
canonical_claimed_body = json.dumps(
    claimed_body, sort_keys=True, separators=(",", ":")
).encode()

print(f"TRANSLATED_FUNCDEF_COUNT={len(funcdefs)}")
print(f"CLAIMED_CLOSURE_COUNT={len(closures)}")
print("ONLY_LIST_UNIT_NORMALIZATION=True")
print(f"FUNCTION_NAME_IS_TARGET={name_is_target}")
print(f"PARAMETERS_KAST_EQUAL={params_equal}")
print(f"BODY_KAST_EQUAL={body_equal}")
print(f"DEFINING_SCOPE_IS_ZERO={scope_is_zero}")
print(f"TRANSLATED_BODY_SHA256={hashlib.sha256(canonical_body).hexdigest()}")
print(
    "CLAIMED_BODY_SHA256="
    f"{hashlib.sha256(canonical_claimed_body).hexdigest()}"
)
if not all((name_is_target, params_equal, body_equal, scope_is_zero)):
    raise SystemExit(1)
