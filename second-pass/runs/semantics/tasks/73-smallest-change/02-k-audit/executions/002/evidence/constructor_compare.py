#!/usr/bin/env python3
"""Mechanical KAST comparison of submitted function bodies and proof macros."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRATCH = Path("/tmp/audit-work/73-smallest-change")
DEFINITION = SCRATCH / "audit-verification-kompiled"


def kast_json(*args: str) -> dict[str, Any]:
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
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.stderr:
        print(f"KAST_STDERR[{args!r}]={completed.stderr!r}")
    return json.loads(completed.stdout)["term"]


def label_name(term: dict[str, Any]) -> str:
    return term.get("label", {}).get("name", "")


def flatten_stmts(term: dict[str, Any]) -> list[dict[str, Any]]:
    if label_name(term).startswith("___MPY-SYNTAX_Stmts_Stmt_Stmts"):
        return [term["args"][0], *flatten_stmts(term["args"][1])]
    if label_name(term).startswith(".List{"):
        return []
    raise ValueError(f"unexpected Stmts term: {label_name(term)}")


def tokens(term: dict[str, Any]) -> list[str]:
    found: list[str] = []
    if term.get("node") == "KToken":
        found.append(term["token"])
    for arg in term.get("args", []):
        found.extend(tokens(arg))
    return found


def digest(term: dict[str, Any]) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    module = kast_json(
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "solution.mpy",
    )
    module_stmts = flatten_stmts(module["args"][0])
    functions: dict[str, dict[str, Any]] = {}
    for stmt in module_stmts:
        if label_name(stmt).startswith("FuncDef(_,_,_)"):
            name = json.loads(stmt["args"][0]["token"])
            functions[name] = stmt

    results: dict[str, Any] = {
        "module_top_level_statement_count": len(module_stmts),
        "module_function_names": sorted(functions),
    }
    ok = True
    for function_name, macro_prefix, expected_params in (
        ("_smallest_change", "helper", ["arr", "left", "right"]),
        ("smallest_change", "main", ["arr"]),
    ):
        function = functions[function_name]
        submitted_body = function["args"][2]
        submitted_params = [json.loads(value) for value in tokens(function["args"][1])]
        macro_body = kast_json(
            "--module",
            "VERIFICATION",
            "--sort",
            "Stmts",
            "--expression",
            f"#{macro_prefix}Body",
            "--expand-macros",
        )
        macro_closure = kast_json(
            "--module",
            "VERIFICATION",
            "--sort",
            "Val",
            "--expression",
            f"#{macro_prefix}Closure",
            "--expand-macros",
        )
        closure_params = [json.loads(value) for value in tokens(macro_closure["args"][0])]
        closure_body = macro_closure["args"][1]
        closure_scope = macro_closure["args"][2].get("token")
        checks = {
            "submitted_params": submitted_params,
            "expected_params": expected_params,
            "macro_closure_params": closure_params,
            "body_equals_expanded_body_macro": submitted_body == macro_body,
            "body_equals_expanded_closure_body": submitted_body == closure_body,
            "closure_scope": closure_scope,
            "closure_is_closureVal": label_name(macro_closure).startswith("closureVal("),
            "submitted_body_sha256": digest(submitted_body),
            "body_macro_sha256": digest(macro_body),
            "closure_body_sha256": digest(closure_body),
            "closure_term_sha256": digest(macro_closure),
        }
        checks_ok = (
            submitted_params == expected_params
            and closure_params == expected_params
            and checks["body_equals_expanded_body_macro"]
            and checks["body_equals_expanded_closure_body"]
            and closure_scope == "0"
            and checks["closure_is_closureVal"]
        )
        checks["all_checks_pass"] = checks_ok
        results[function_name] = checks
        ok = ok and checks_ok

    results["constructor_level_identity"] = ok
    print(json.dumps(results, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
