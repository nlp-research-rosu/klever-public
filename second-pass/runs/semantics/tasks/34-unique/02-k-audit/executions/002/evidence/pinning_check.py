#!/usr/bin/env python3
"""Mechanical constructor-level program/body comparison for the entry claim."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "audit-verification-kompiled"


def run_kast(*arguments: str) -> dict:
    result = subprocess.run(
        ["kast", *arguments],
        cwd=WORK,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def main() -> int:
    submitted = run_kast(
        "solution.regenerated.mpy",
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--output",
        "json",
    )
    assert label(submitted).startswith("Module(_)")
    module_stmts = submitted["args"][0]
    assert label(module_stmts).startswith("___")
    function = module_stmts["args"][0]
    assert label(function).startswith("FuncDef(")
    submitted_name, submitted_params, submitted_body = function["args"]

    verification_text = (WORK / "verification.k").read_text(encoding="utf-8")
    loop_match = re.search(
        r"(?ms)^\s*rule\s+uniqueLoopBody\s*=>\s*(.*?)"
        r"(?=^\s*syntax\s+Stmts\s+::=\s+\"uniqueBody\")",
        verification_text,
    )
    body_match = re.search(
        r"(?ms)^\s*rule\s+uniqueBody\s*=>\s*(.*?)^\s*endmodule\s*$",
        verification_text,
    )
    if loop_match is None or body_match is None:
        raise RuntimeError("could not extract program-body defining RHS rules")
    loop_body_text = loop_match.group(1).strip()
    claimed_body_text = body_match.group(1).strip()
    # Convert K-rule notation for empty associative units back to the surface
    # MPY constructor notation accepted by the program parser.
    claimed_surface_body = claimed_body_text.replace(
        "uniqueLoopBody", loop_body_text
    )
    claimed_surface_body = claimed_surface_body.replace(".Exprs", "")
    claimed_surface_body = claimed_surface_body.replace(".Stmts", "")
    claimed_module = (
        'Module(FuncDef("unique", Params("l"), '
        + claimed_surface_body
        + "))"
    )
    claimed_program = run_kast(
        "--expression",
        claimed_module,
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--output",
        "json",
    )
    claimed_body = claimed_program["args"][0]["args"][0]["args"][2]

    spec_text = (WORK / "spec.k").read_text(encoding="utf-8")
    entry_binding = re.search(
        r'FuncDef\("unique",\s*Params\("l"\),\s*uniqueBody\)',
        spec_text,
    )
    entry_call = re.search(
        r'Call\(Name\("unique"\),\s*list\(INPUT:ValSeq\)\)',
        spec_text,
    )

    expected_name = {
        "node": "KToken",
        "sort": {"node": "KSort", "name": "String"},
        "token": '"unique"',
    }
    print(f"submitted_name_is_unique={submitted_name == expected_name}")
    print(f"submitted_parameter_constructor={label(submitted_params)}")
    print(f"body_constructor_identity={submitted_body == claimed_body}")
    print(f"entry_claim_uses_unique_binding={entry_binding is not None}")
    print(f"entry_claim_calls_unique_on_symbolic_list={entry_call is not None}")
    print(f"submitted_body_root={label(submitted_body)}")
    print(f"claimed_body_root={label(claimed_body)}")
    return 0 if (
        submitted_name == expected_name
        and submitted_body == claimed_body
        and entry_binding is not None
        and entry_call is not None
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
