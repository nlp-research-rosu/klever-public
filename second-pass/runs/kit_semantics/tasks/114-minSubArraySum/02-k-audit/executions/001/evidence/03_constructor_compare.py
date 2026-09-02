#!/usr/bin/env python3
"""Mechanically compare translated FuncDef constructors with SPEC.target's closure."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/114-minSubArraySum")
PROGRAM_DEFINITION = WORK / "audit-verification-kompiled"
PARSER_DEFINITION = WORK / "audit-parser-kompiled"


def kast_file(path: Path, sort: str, module: str) -> dict:
    completed = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(PROGRAM_DEFINITION),
            "--module",
            module,
            "--sort",
            sort,
            "--output",
            "json",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(completed.stdout)["term"]


def kast_expression(expression: str, sort: str, module: str) -> dict:
    completed = subprocess.run(
        [
            "kast",
            "--expression",
            expression,
            "--definition",
            str(PARSER_DEFINITION),
            "--module",
            module,
            "--sort",
            sort,
            "--output",
            "json",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return json.loads(completed.stdout)["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def balanced_call(source: str, start: int) -> str:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise ValueError("unterminated constructor call")


module_term = kast_file(WORK / "solution.mpy", "Module", "MPY-SYNTAX")
assert label(module_term).startswith("Module(")
module_statements = module_term["args"][0]
assert label(module_statements).startswith("___MPY-SYNTAX_Stmts")
func_def, module_rest = module_statements["args"]
assert label(module_rest).startswith(".List{")
assert label(func_def).startswith("FuncDef(")
source_name, params_wrapper, source_body = func_def["args"]
assert label(params_wrapper).startswith("Params(")
source_params = params_wrapper["args"][0]

spec_text = (WORK / "spec.k").read_text()
target_text = spec_text.split("claim [target]:", 1)[1]
binding_match = re.search(
    r'(?P<binding>"(?:[^"\\]|\\.)*")\s*\|->\s*closureVal\(',
    target_text,
)
if binding_match is None:
    raise AssertionError("target binding/closure not found")
binding_token = binding_match.group("binding")
closure_start = target_text.index("closureVal(", binding_match.start())
closure_text = balanced_call(target_text, closure_start)
# Claim syntax writes explicit generated-list terminators. The program parser
# accepts the equivalent singleton/statement-list surface form.
parseable_closure = re.sub(r",\s*\.ParamNames", "", closure_text, count=1)
parseable_closure = re.sub(r"\s*\.Stmts", "", parseable_closure)
target_closure = kast_expression(parseable_closure, "Val", "VERIFICATION")
assert label(target_closure).startswith("closureVal(")
target_params, target_body, defining_environment = target_closure["args"]

checks = {
    "one translated top-level function": True,
    "translated function name equals target map binding": (
        source_name["token"] == binding_token
    ),
    "translated parameter constructors equal target closure parameters": (
        source_params == target_params
    ),
    "translated statement constructors equal target closure body": (
        source_body == target_body
    ),
    "target closure defining environment is module frame 0": (
        defining_environment.get("node") == "KToken"
        and defining_environment.get("token") == "0"
        and defining_environment.get("sort", {}).get("name") == "Int"
    ),
}

for description, result in checks.items():
    print(f"{'OK' if result else 'FAIL'}: {description}")

body_json = json.dumps(source_body, sort_keys=True, separators=(",", ":")).encode()
print("SOURCE_FUNCTION_NAME:", source_name["token"])
print("TARGET_BINDING_NAME:", binding_token)
print("BODY_CONSTRUCTOR_SHA256:", hashlib.sha256(body_json).hexdigest())
print("CLOSURE_TEXT:", " ".join(closure_text.split()))

if not all(checks.values()):
    raise SystemExit(1)
