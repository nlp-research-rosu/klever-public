#!/usr/bin/env python3
"""Compare the fresh parsed submitted function body with proof macro expansion."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/142-sum-squares-audit")
DEFINITION = WORK / "audit-verification-kompiled"


def run_json(command: list[str]) -> dict:
    print("COMMAND: " + " ".join(command))
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    print(f"EXIT_STATUS: {result.returncode}")
    if result.stderr:
        print("STDERR: " + result.stderr.strip())
    if result.returncode:
        raise RuntimeError("kast failed")
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def digest(term: dict) -> str:
    encoded = json.dumps(term, separators=(",", ":"), sort_keys=True).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    module_term = run_json(
        [
            "kast",
            str(WORK / "solution.mpy"),
            "--definition",
            str(DEFINITION),
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Module",
            "--expand-macros",
            "--output",
            "json",
        ]
    )
    macro_body = run_json(
        [
            "kast",
            "--expression",
            "sumSquaresFunctionBody",
            "--definition",
            str(DEFINITION),
            "--module",
            "SUM-SQUARES-VERIFICATION",
            "--sort",
            "Stmts",
            "--expand-macros",
            "--output",
            "json",
        ]
    )
    loop_macro = run_json(
        [
            "kast",
            "--expression",
            "sumSquaresLoopBody",
            "--definition",
            str(DEFINITION),
            "--module",
            "SUM-SQUARES-VERIFICATION",
            "--sort",
            "Stmts",
            "--expand-macros",
            "--output",
            "json",
        ]
    )

    if not label(module_term).startswith("Module("):
        raise AssertionError(label(module_term))
    module_stmts = module_term["args"][0]
    function = module_stmts["args"][0]
    module_tail = module_stmts["args"][1]
    if not label(function).startswith("FuncDef("):
        raise AssertionError(label(function))
    function_name, params, submitted_body = function["args"]
    checks = {
        "module_has_one_statement": label(module_tail).startswith(".List{"),
        "function_name_is_sum_squares": function_name["token"] == '"sum_squares"',
        "parameter_is_exactly_lst": (
            params["args"][0]["args"][0]["token"] == '"lst"'
            and label(params["args"][0]["args"][1]).startswith(".List{")
        ),
        "submitted_body_equals_expanded_proof_macro": submitted_body == macro_body,
        "for_body_equals_expanded_loop_macro": (
            # Body is Assign; Assign; For; Return.  Follow Stmts tails twice.
            submitted_body["args"][1]["args"][1]["args"][0]["args"][2] == loop_macro
        ),
    }
    print(f"submitted_body_sha256={digest(submitted_body)}")
    print(f"proof_macro_body_sha256={digest(macro_body)}")
    print(f"submitted_for_body_sha256={digest(submitted_body['args'][1]['args'][1]['args'][0]['args'][2])}")
    print(f"proof_loop_macro_sha256={digest(loop_macro)}")
    for name, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'} {name}")
    failures = sum(not passed for passed in checks.values())
    print(f"failure_count={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
