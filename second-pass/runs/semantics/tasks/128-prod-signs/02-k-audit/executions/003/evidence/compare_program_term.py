#!/usr/bin/env python3
"""Mechanically compare the submitted MPY function with the claim's closure."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

WORK = Path("/tmp/audit-work/128-prod-signs-audit/candidate")
DEFINITION = WORK / "audit-verification-kompiled"


def run_kast(arguments: list[str]) -> dict:
    completed = subprocess.run(
        ["kast", *arguments, "--output", "json"],
        cwd=WORK,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(completed.stdout)["term"]


module = run_kast(
    [
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--expand-macros",
    ]
)
closure = run_kast(
    [
        "--expression",
        "prodSignsFunction",
        "--definition",
        str(DEFINITION),
        "--module",
        "PROD-SIGNS-VERIFICATION",
        "--sort",
        "Val",
        "--expand-macros",
    ]
)

module_stmts = module["args"][0]
function = module_stmts["args"][0]
module_tail = module_stmts["args"][1]
name, params, body = function["args"]
closure_params, closure_body, closure_location = closure["args"]

checks = {
    "module_constructor": module["label"]["name"].startswith("Module("),
    "single_function_binding": module_tail["arity"] == 0,
    "function_constructor": function["label"]["name"].startswith("FuncDef("),
    "function_name_prod_signs": name.get("token") == '"prod_signs"',
    "parameters_exact": params["args"][0] == closure_params,
    "body_exact": body == closure_body,
    "definition_location_zero": closure_location.get("token") == "0",
}

for key, value in checks.items():
    print(f"{key}={value}")
print(f"all_constructor_checks={all(checks.values())}")

raise SystemExit(0 if all(checks.values()) else 1)
