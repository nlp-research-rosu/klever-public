#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy with every entry claim."""

from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
from pathlib import Path


DEFINITION = Path("/tmp/audit-work/build/proof-kompiled")
PROGRAM = Path("/tmp/audit-work/candidate/solution.mpy")
SPEC_JSON = Path("/tmp/audit-work/spec-claims.json")


def digest(term: object) -> str:
    return hashlib.sha256(
        json.dumps(term, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def label_of(term: dict) -> str:
    return term["label"]["name"]


def string_tokens(term: object) -> list[str]:
    result: list[str] = []
    if isinstance(term, dict):
        if term.get("node") == "KToken" and term.get("sort", {}).get("name") == "String":
            result.append(json.loads(term["token"]))
        else:
            for value in term.values():
                result.extend(string_tokens(value))
    elif isinstance(term, list):
        for value in term:
            result.extend(string_tokens(value))
    return result


def main() -> None:
    command = [
        "kast",
        str(PROGRAM),
        "--definition",
        str(DEFINITION),
        "--module",
        "SEMANTIC-SYNTAX",
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    print("INNER_COMMAND:", shlex.join(command))
    result = subprocess.run(command, check=False, text=True, capture_output=True)
    print(f"INNER_EXIT_STATUS: {result.returncode}")
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError("kast failed")
    submitted_program = json.loads(result.stdout)["term"]
    submitted_digest = digest(submitted_program)
    print(f"submitted_program_kast_sha256={submitted_digest}")

    assert label_of(submitted_program).startswith("Module(_)")
    statements = submitted_program["args"][0]
    assert label_of(statements).startswith("___SEMANTIC-SYNTAX_Stmts")
    function_definition = statements["args"][0]
    assert label_of(function_definition).startswith("FuncDef(")
    function_name, params, function_body = function_definition["args"]
    parameter_names = string_tokens(params)
    assert len(parameter_names) == 1

    spec = json.loads(SPEC_JSON.read_text())
    claims = spec["term"]["term"][0]["localSentences"]
    seen = 0
    for claim in claims:
        claim_label = claim["att"]["att"]["label"]
        assert claim["requires"]["token"] == "true"
        assert claim["ensures"]["token"] == "true"
        generated_top = claim["body"]
        k_rewrite = generated_top["args"][0]["args"][0]
        claim_program = k_rewrite["lhs"]["items"][0]
        claim_digest = digest(claim_program)
        program_equal = claim_program == submitted_program

        functions_rewrite = generated_top["args"][1]["args"][0]
        assert label_of(functions_rewrite["lhs"]) == ".Map"
        binding = functions_rewrite["rhs"]
        binding_name, function_value = binding["args"]
        bound_parameter, bound_body = function_value["args"]
        binding_equal = (
            binding_name == function_name
            and json.loads(bound_parameter["token"]) == parameter_names[0]
            and bound_body == function_body
        )
        print(
            f"{claim_label}: claim_program_kast_sha256={claim_digest} "
            f"program_equal={program_equal} binding_body_equal={binding_equal}"
        )
        assert program_equal
        assert binding_equal
        seen += 1

    assert seen == 3
    print(f"CLAIMS_COMPARED={seen}")
    print("PROGRAM_PINNING=PASS")


if __name__ == "__main__":
    main()
