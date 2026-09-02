#!/usr/bin/env python3
"""Mechanical constructor-level source-to-entry-claim pinning check."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


SCRATCH = Path("/tmp/audit-work/audit-24")
DEFINITION = SCRATCH / "audit-verification-kompiled"


def balanced_application(text: str, marker: str, start_at: int = 0) -> str:
    start = text.index(marker, start_at)
    opening = text.index("(", start + len(marker))
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        char = text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1]
    raise ValueError(f"unbalanced application starting at {marker}")


def run_json(*arguments: str) -> dict:
    completed = subprocess.run(
        list(arguments),
        check=True,
        cwd=SCRATCH,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(completed.stdout)["term"]


def label(term: dict) -> str:
    return term["label"]["name"]


def main() -> None:
    solution_term = run_json(
        "kast",
        "solution.mpy",
        "--definition",
        str(DEFINITION),
        "--output",
        "json",
    )
    spec_text = (SCRATCH / "spec.k").read_text(encoding="utf-8")
    entry_start = spec_text.index("claim [largest-divisor]:")
    binding_start = spec_text.index(
        '"largest_divisor" |->', entry_start
    )
    closure_text = balanced_application(spec_text, "closureVal", binding_start)
    # `.Stmts` is K-source notation for the list unit; the program parser
    # supplies the same unit implicitly at the end of each textual list.
    closure_program_text = closure_text.replace(" .Stmts", "")
    closure_term = run_json(
        "kast",
        "--expression",
        closure_program_text,
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--sort",
        "Val",
        "--output",
        "json",
    )

    assert label(solution_term).startswith("Module(_)")
    top_statements = solution_term["args"][0]
    function_term = top_statements["args"][0]
    assert label(function_term).startswith("FuncDef(")
    function_name, params_wrapper, program_body = function_term["args"]
    assert function_name["token"] == '"largest_divisor"'
    assert label(params_wrapper).startswith("Params(_)")
    program_params = params_wrapper["args"][0]

    assert label(closure_term).startswith("closureVal(")
    claim_params, claim_body, defining_location = closure_term["args"]

    source_text = (SCRATCH / "solution.mpy").read_bytes()
    regenerated_text = (SCRATCH / "regenerated-solution.mpy").read_bytes()
    entry_k_slice = spec_text[entry_start : spec_text.index("endmodule", entry_start)]
    named_call_present = 'Call(Name("largest_divisor"), Int(N))' in entry_k_slice
    constrained_summary_present = (
        "largestDivisorAtOrBelow(N, N -Int 1)" in entry_k_slice
    )

    print(f"solution_mpy_sha256={hashlib.sha256(source_text).hexdigest()}")
    print(
        "trusted_regeneration_byte_equal="
        f"{source_text == regenerated_text}"
    )
    print(f"function_name={function_name['token']}")
    print(f"parameter_constructor_equal={program_params == claim_params}")
    print(f"body_constructor_equal={program_body == claim_body}")
    print(f"claim_defining_location={defining_location['token']}")
    print(f"entry_k_executes_named_call={named_call_present}")
    print(
        "entry_result_constrained_to_summary="
        f"{constrained_summary_present}"
    )

    if not (
        source_text == regenerated_text
        and program_params == claim_params
        and program_body == claim_body
        and defining_location["token"] == "0"
        and named_call_present
        and constrained_summary_present
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
