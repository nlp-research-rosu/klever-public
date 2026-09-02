#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy with the executed proof wrapper."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
DEFINITION = WORK / "verification-audit-kompiled"


def run_kast(arguments: list[str]) -> dict:
    command = [
        "kast",
        "--definition",
        str(DEFINITION),
        "--output",
        "json",
        *arguments,
    ]
    print("COMMAND:", " ".join(command))
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    print("EXIT_STATUS:", result.returncode)
    if result.stderr:
        print("STDERR:", result.stderr.rstrip())
    if result.returncode != 0:
        raise RuntimeError("kast failed")
    return json.loads(result.stdout)["term"]


def label(term: dict) -> str:
    return term.get("label", {}).get("name", "")


def args(term: dict) -> list[dict]:
    return term.get("args", [])


def token(term: dict) -> str:
    return term.get("token", "")


def canonical_hash(term: dict) -> str:
    data = json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def expect(name: str, condition: bool, detail: str = "") -> None:
    print(f"{name}: {'PASS' if condition else 'FAIL'}{(' — ' + detail) if detail else ''}")
    if not condition:
        raise AssertionError(name)


def main() -> int:
    program = run_kast(
        [
            "--input",
            "program",
            "--sort",
            "Module",
            str(WORK / "submitted-solution.mpy"),
        ]
    )

    verification_text = (WORK / "verification.k").read_text()
    matches = re.findall(r"(?ms)^\s*rule\s+(<k>.*?</k>)", verification_text)
    expect("exactly one local operational rule", len(matches) == 1, f"count={len(matches)}")
    rule = run_kast(["--input", "rule", "--expression", matches[0]])

    expect("program root is Module", label(program).startswith("Module(_)"))
    program_stmts = args(program)[0]
    expect("program statement list is nonempty", label(program_stmts).startswith("___MPY-SYNTAX_Stmts"))
    function, program_tail = args(program_stmts)
    expect("program has exactly one statement", label(program_tail).startswith(".List{"))
    expect("sole statement is 3-argument FuncDef", label(function).startswith("FuncDef(_,_,_)"))
    function_name, params_wrapper, function_body = args(function)
    expect(
        "submitted binding name",
        token(function_name) == '"is_equal_to_sum_even"',
        token(function_name),
    )
    expect("submitted Params wrapper", label(params_wrapper).startswith("Params(_)"))
    submitted_params = args(params_wrapper)[0]

    expect("rule root is k cell", label(rule) == "<k>")
    sequence = args(rule)[0]
    expect("rule k cell is a K sequence", sequence.get("node") == "KSequence")
    rewrite, continuation = sequence["items"]
    expect("wrapper preserves an arbitrary continuation", continuation.get("node") == "KVariable")
    expect("rule contains a rewrite", rewrite.get("node") == "KRewrite")
    lhs, rhs = rewrite["lhs"], rewrite["rhs"]
    expect("wrapper LHS symbol", label(lhs).startswith("#isEqualToSumEven(_)"))
    lhs_n = args(lhs)[0]
    expect(
        "wrapper LHS has symbolic Int argument",
        lhs_n.get("node") == "KVariable"
        and lhs_n.get("name") == "N"
        and lhs_n.get("sort", {}).get("name") == "Int",
    )
    expect("wrapper RHS calls supplied Call constructor", label(rhs).startswith("Call(_,_)"))
    closure, call_args = args(rhs)
    expect("wrapper constructs a closure", label(closure).startswith("closureVal(_,_,_)"))
    proof_params, proof_body, proof_env = args(closure)

    expect(
        "constructor-identical parameter list",
        submitted_params == proof_params,
        f"submitted={canonical_hash(submitted_params)} proof={canonical_hash(proof_params)}",
    )
    expect(
        "constructor-identical function body",
        function_body == proof_body,
        f"submitted={canonical_hash(function_body)} proof={canonical_hash(proof_body)}",
    )
    expect(
        "closure captures initial scope 0",
        token(proof_env) == "0" and proof_env.get("sort", {}).get("name") == "Int",
    )
    expect("call argument list is nonempty", label(call_args).startswith("_,__MPY-SYNTAX_Exprs"))
    call_n, call_tail = args(call_args)
    expect("call argument is the same symbolic N", call_n == lhs_n)
    expect("call has exactly one argument", label(call_tail).startswith(".List{"))

    print(f"submitted_parameter_tree_sha256={canonical_hash(submitted_params)}")
    print(f"proof_parameter_tree_sha256={canonical_hash(proof_params)}")
    print(f"submitted_body_tree_sha256={canonical_hash(function_body)}")
    print(f"proof_body_tree_sha256={canonical_hash(proof_body)}")
    print("OVERALL: PASS")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as error:
        print(f"OVERALL: FAIL ({error})")
        sys.exit(1)
