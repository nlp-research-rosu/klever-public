#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and the K claims."""

import hashlib
import json
import re
import subprocess
from pathlib import Path

SCRATCH = Path("/tmp/audit-work/prime31")
DEFINITION = SCRATCH / "reviewer-verification-kompiled"


def kast_file(path: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--output",
        "json",
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{command}: {result.stderr}")
    return json.loads(result.stdout)["term"]


def kast_expression(expression: str, sort: str) -> dict:
    command = [
        "kast",
        "--expression",
        expression,
        "--sort",
        sort,
        "--module",
        "MPY-SYNTAX",
        "--definition",
        str(DEFINITION),
        "--output",
        "json",
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(
            f"failed to parse {sort} expression:\n{expression}\n{result.stderr}"
        )
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def balanced_term(text: str, marker: str, search_from: int = 0) -> str:
    start = text.index(marker + "(", search_from)
    depth = 0
    quoted = False
    escaped = False
    for index in range(start + len(marker), len(text)):
        char = text[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced {marker} term")


def top_level_args(term: str) -> list[str]:
    open_paren = term.index("(")
    close_paren = len(term) - 1
    parts = []
    start = open_paren + 1
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, close_paren):
        char = term[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            parts.append(term[start:index].strip())
            start = index + 1
    parts.append(term[start:close_paren].strip())
    return parts


def flatten_param_names(term: dict) -> list[str]:
    name = label(term)
    if term.get("node") == "KToken":
        return [json.loads(term["token"])]
    if name.startswith(".List{") or name == ".ParamNames":
        return []
    if "ParamNames_String_ParamNames" in name:
        return flatten_param_names(term["args"][0]) + flatten_param_names(term["args"][1])
    raise ValueError(f"unexpected ParamNames constructor: {name}")


def statements(term: dict) -> list[dict]:
    name = label(term)
    if name.startswith(".List{") or name == ".Stmts":
        return []
    if "Stmts_Stmt_Stmts" in name:
        return [term["args"][0], *statements(term["args"][1])]
    raise ValueError(f"unexpected Stmts constructor: {name}")


solution = kast_file(SCRATCH / "submitted-solution.mpy")
module_stmts = solution["args"][0]
top_statements = statements(module_stmts)
assert len(top_statements) == 1
function = top_statements[0]
assert label(function).startswith("FuncDef(")
function_name = json.loads(function["args"][0]["token"])
params_wrapper = function["args"][1]
assert label(params_wrapper).startswith("Params(")
solution_params = flatten_param_names(params_wrapper["args"][0])
solution_body = function["args"][2]

spec_text = (SCRATCH / "spec.k").read_text()
binding_offset = spec_text.index('"is_prime" |->')
closure_text = balanced_term(spec_text, "closureVal", binding_offset)
closure_args = top_level_args(closure_text)
assert len(closure_args) == 3
match = re.fullmatch(r'\(\s*"([^"]+)"\s*,\s*\.ParamNames\s*\)', closure_args[0])
assert match
spec_params = [match.group(1)]
spec_body_source = closure_args[1].replace(".Stmts", "")
spec_body = kast_expression(spec_body_source, "Stmts")
closure_scope = closure_args[2]

body_equal = solution_body == spec_body
params_equal = solution_params == spec_params

solution_while = [
    statement
    for statement in statements(solution_body)
    if label(statement).startswith("While(")
]
assert len(solution_while) == 1
solution_condition, solution_loop_body = solution_while[0]["args"]

loop_claim_offset = spec_text.index("claim [prime-loop]:")
loop_term = balanced_term(spec_text, "#while", loop_claim_offset)
loop_args = top_level_args(loop_term)
assert len(loop_args) == 2
claim_condition = kast_expression(loop_args[0], "Expr")
claim_loop_body = kast_expression(loop_args[1].replace(".Stmts", ""), "Stmts")

condition_equal = solution_condition == claim_condition
loop_body_equal = solution_loop_body == claim_loop_body
body_hash = hashlib.sha256(
    json.dumps(solution_body, sort_keys=True, separators=(",", ":")).encode()
).hexdigest()

print(f"function_name={function_name}")
print(f"solution_params={solution_params}")
print(f"spec_params={spec_params}")
print(f"closure_scope={closure_scope}")
print(f"params_constructor_equal={params_equal}")
print(f"body_constructor_equal={body_equal}")
print(f"body_kast_sha256={body_hash}")
print(f"loop_condition_constructor_equal={condition_equal}")
print(f"loop_body_constructor_equal={loop_body_equal}")

entry_prefix = re.sub(r"\s+", "", spec_text[spec_text.index("Call(Name(") :])
print(
    "entry_call_exact="
    + str(entry_prefix.startswith('Call(Name("is_prime"),(Int(N),.Exprs))=>?R:Bool~>.K'))
)

if not all(
    [
        function_name == "is_prime",
        params_equal,
        body_equal,
        condition_equal,
        loop_body_equal,
        closure_scope == "0",
    ]
):
    raise SystemExit(1)
print("RESULT=PASS")
