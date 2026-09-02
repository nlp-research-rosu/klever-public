#!/usr/bin/env python3
"""Constructor-level comparison of trusted translation and entry/loop claims."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterator


SOLUTION_JSON = Path("/audit-output/evidence/solution-expanded.json")
SPEC_JSON = Path("/audit-output/evidence/spec-expanded.json")


def walk(term: Any) -> Iterator[dict[str, Any]]:
    if isinstance(term, dict):
        yield term
        for value in term.values():
            yield from walk(value)
    elif isinstance(term, list):
        for value in term:
            yield from walk(value)


def label(term: dict[str, Any]) -> str:
    value = term.get("label")
    if isinstance(value, dict):
        name = value.get("name")
        if isinstance(name, str):
            return name
    return ""


def token(term: dict[str, Any]) -> str | None:
    value = term.get("token")
    return value if isinstance(value, str) else None


def digest(term: Any) -> str:
    encoded = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    solution = json.loads(SOLUTION_JSON.read_text())["term"]
    spec = json.loads(SPEC_JSON.read_text())["term"]

    functions = [
        term
        for term in walk(solution)
        if term.get("node") == "KApply" and label(term).startswith("FuncDef(")
    ]
    if len(functions) != 1:
        raise RuntimeError(f"expected one translated function, found {len(functions)}")
    function = functions[0]
    function_name = token(function["args"][0])
    source_params = function["args"][1]["args"][0]
    source_body = function["args"][2]

    closures = [
        term
        for term in walk(spec)
        if term.get("node") == "KApply" and label(term).startswith("closureVal(")
    ]
    loops = [
        term
        for term in walk(spec)
        if term.get("node") == "KApply" and label(term).startswith("#loop(")
    ]
    source_fors = [
        term
        for term in walk(source_body)
        if term.get("node") == "KApply" and label(term).startswith("For(")
    ]
    if len(source_fors) != 1:
        raise RuntimeError(f"expected one source For, found {len(source_fors)}")
    source_for = source_fors[0]

    print(f"translated_function_name={function_name}")
    print(f"source_params_sha256={digest(source_params)}")
    print(f"source_body_sha256={digest(source_body)}")
    print(f"entry_closure_count={len(closures)}")
    closure_ok = True
    for index, closure in enumerate(closures, 1):
        params_equal = closure["args"][0] == source_params
        body_equal = closure["args"][1] == source_body
        defining_env = token(closure["args"][2])
        closure_ok &= params_equal and body_equal and defining_env == "0"
        print(
            f"closure_{index}: params_equal={params_equal} body_equal={body_equal} "
            f"defining_env={defining_env} body_sha256={digest(closure['args'][1])}"
        )

    print(f"source_for_count={len(source_fors)}")
    print(f"spec_loop_count={len(loops)}")
    loop_ok = len(loops) >= 1
    for index, loop in enumerate(loops, 1):
        target_equal = loop["args"][1] == source_for["args"][0]
        body_equal = loop["args"][2] == source_for["args"][2]
        loop_ok &= target_equal and body_equal
        print(
            f"loop_{index}: target_equal={target_equal} body_equal={body_equal} "
            f"source_body_sha256={digest(source_for['args'][2])} "
            f"claim_body_sha256={digest(loop['args'][2])}"
        )

    ok = (
        function_name == '"rolling_max"'
        and len(closures) == 2
        and closure_ok
        and loop_ok
    )
    print(f"PROGRAM_PINNING_OK={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
