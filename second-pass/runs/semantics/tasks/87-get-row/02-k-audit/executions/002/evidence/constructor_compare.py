#!/usr/bin/env python3
"""Compare the trusted-translator body and independently transcribed K body ASTs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


DEFINITION = "/tmp/audit-work/rebuild/audit-verification-kompiled"
SOLUTION = "/tmp/audit-work/rebuild/solution.fresh.mpy"
EXPECTED = "/tmp/audit-work/rebuild/expected-body.mpy"


def kast(path: str, sort: str) -> dict:
    command = [
        "kast",
        "--definition",
        DEFINITION,
        "--input",
        "program",
        "--sort",
        sort,
        path,
        "--output",
        "json",
    ]
    print("command=", " ".join(command))
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def digest(term: dict) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> None:
    module = kast(SOLUTION, "Module")
    expected_body = kast(EXPECTED, "Stmts")

    assert label(module).startswith("Module(")
    module_statements = module["args"][0]
    assert label(module_statements).startswith("___MPY-SYNTAX_Stmts")
    function = module_statements["args"][0]
    remaining_module_statements = module_statements["args"][1]
    assert label(function).startswith("FuncDef(")
    assert label(remaining_module_statements).startswith(".List{")

    function_name = function["args"][0]["token"]
    params = function["args"][1]
    translated_body = function["args"][2]
    assert function_name == '"get_row"'

    parameter_names: list[str] = []
    cursor = params["args"][0]
    while cursor.get("args"):
        parameter_names.append(cursor["args"][0]["token"])
        cursor = cursor["args"][1]
    assert parameter_names == ['"lst"', '"x"']

    print(f"function_name={function_name}")
    print(f"parameter_names={parameter_names}")
    print(f"translated_body_kast_sha256={digest(translated_body)}")
    print(f"expected_body_kast_sha256={digest(expected_body)}")
    print(f"constructor_ast_equal={translated_body == expected_body}")
    assert translated_body == expected_body


if __name__ == "__main__":
    main()
