#!/usr/bin/env python3
"""Mechanically compare the submitted MPY function body with the claimed body."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


WORK = Path("/tmp/audit-work/task20")
VERIFICATION = WORK / "verification.k"
SOLUTION_JSON = WORK / "solution-expanded.json"
EXPANDED_TEXT = Path("/audit-output/evidence/claim-body-expanded.kterm")


def extract_rule_rhs(text: str, head: str) -> str:
    marker = f"  rule {head} =>"
    start = text.find(marker)
    if start < 0:
        raise ValueError(f"missing rule head: {head}")
    rhs_start = start + len(marker)
    remainder = text[rhs_start:]
    end_candidates = [
        offset
        for marker_text in ("\n\n  syntax ", "\n\n  rule ", "\n\n  //", "\nendmodule")
        if (offset := remainder.find(marker_text)) >= 0
    ]
    if not end_candidates:
        raise ValueError(f"cannot find end of rule: {head}")
    return remainder[: min(end_candidates)].strip()


def label_name(term: dict[str, Any]) -> str:
    return term.get("label", {}).get("name", "")


def walk(term: Any):
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def main() -> int:
    verification = VERIFICATION.read_text(encoding="utf-8")
    condition = extract_rule_rhs(verification, "findClosestLoopCondition")
    loop_body = extract_rule_rhs(verification, "findClosestLoopBody")
    function_body = extract_rule_rhs(verification, "findClosestBody")

    expanded = function_body.replace(
        "findClosestLoopCondition", f"({condition})"
    ).replace("findClosestLoopBody", f"({loop_body})")
    EXPANDED_TEXT.write_text(expanded + "\n", encoding="utf-8")

    parse = subprocess.run(
        [
            "kast",
            "--input",
            "rule",
            "--expression",
            f"PIN:Stmts => {expanded}",
            "--definition",
            str(WORK / "verification-kompiled"),
            "--module",
            "VERIFICATION",
            "--sort",
            "Stmts",
            "--expand-macros",
            "--output",
            "json",
        ],
        cwd=WORK,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print(f"kast_exit={parse.returncode}")
    print(f"kast_stderr={parse.stderr!r}")
    if parse.returncode != 0:
        return 1
    claimed_body = json.loads(parse.stdout)["term"]["rhs"]

    solution_term = json.loads(SOLUTION_JSON.read_text(encoding="utf-8"))["term"]
    functions = [
        term
        for term in walk(solution_term)
        if term.get("node") == "KApply"
        and label_name(term).startswith("FuncDef(_,_,_)_")
    ]
    if len(functions) != 1:
        print(f"function_node_count={len(functions)}")
        return 1
    function = functions[0]
    function_name = function["args"][0]
    params = function["args"][1]
    submitted_body = function["args"][2]

    expected_name = {
        "node": "KToken",
        "sort": {"node": "KSort", "name": "String"},
        "token": '"find_closest_elements"',
    }
    name_equal = function_name == expected_name

    param_tokens = [
        term.get("token")
        for term in walk(params)
        if term.get("node") == "KToken"
        and term.get("sort", {}).get("name") == "String"
    ]
    params_equal = param_tokens == ['"numbers"']
    body_equal = submitted_body == claimed_body

    print(f"function_name_equal={name_equal}")
    print(f"function_param_tokens={param_tokens}")
    print(f"function_params_equal={params_equal}")
    print(f"constructor_body_equal={body_equal}")
    print(f"expanded_claim_body_artifact={EXPANDED_TEXT}")

    if not body_equal:
        submitted_path = Path("/audit-output/evidence/submitted-body.json")
        claimed_path = Path("/audit-output/evidence/claimed-body.json")
        submitted_path.write_text(
            json.dumps(submitted_body, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        claimed_path.write_text(
            json.dumps(claimed_body, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"submitted_body_json={submitted_path}")
        print(f"claimed_body_json={claimed_path}")

    return 0 if name_equal and params_equal and body_equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
