#!/usr/bin/env python3
"""Mechanically compare the regenerated program body with the claim's body alias."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/125-split-words")
DEFINITION = SCRATCH / "auditor-verification-kompiled"


def kast(args: list[str]) -> dict:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--output",
        "json",
        *args,
    ]
    completed = subprocess.run(
        command,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print("COMMAND:", " ".join(command))
    print("EXIT_STATUS:", completed.returncode)
    if completed.stderr:
        print("STDERR:", completed.stderr.rstrip())
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return json.loads(completed.stdout)


module_ast = kast(
    [
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        str(SCRATCH / "solution.regenerated.mpy"),
    ]
)["term"]

stmts = module_ast["args"][0]
func_def = stmts["args"][0]
assert func_def["label"]["name"].startswith("FuncDef(")
function_name = func_def["args"][0]["token"]
parameters = func_def["args"][1]
program_body = func_def["args"][2]
remaining_module_statements = stmts["args"][1]

verification = (SCRATCH / "verification.k").read_text()
start_marker = "rule splitWordsBody =>"
end_marker = "\n\n  // Direct mathematical restatement"
start = verification.index(start_marker) + len(start_marker)
end = verification.index(end_marker, start)
alias_rhs_text = verification[start:end].strip()

alias_rewrite = kast(
    [
        "--module",
        "VERIFICATION",
        "--input",
        "rule",
        "--expression",
        "splitWordsBody => " + alias_rhs_text,
    ]
)["term"]
assert alias_rewrite["node"] == "KRewrite"
alias_body = alias_rewrite["rhs"]


def canonical_sha(term: dict) -> str:
    raw = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


print("function_name:", function_name)
print("parameter_ast:", json.dumps(parameters, sort_keys=True))
print("remaining_module_statement_label:", remaining_module_statements["label"]["name"])
print("program_body_ast_sha256:", canonical_sha(program_body))
print("alias_rhs_ast_sha256:", canonical_sha(alias_body))
print("constructor_level_equal:", program_body == alias_body)

if function_name != '"split_words"' or program_body != alias_body:
    raise SystemExit(1)
