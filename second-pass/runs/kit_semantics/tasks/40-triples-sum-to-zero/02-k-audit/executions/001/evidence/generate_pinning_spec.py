#!/usr/bin/env python3
"""Generate a constructor-level source/body pinning claim from trusted kast."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/fresh")
DEFINITION = WORK / "verification-kompiled"
PROGRAM = WORK / "solution.mpy"


def label(term: dict) -> str:
    assert term["node"] == "KApply", term
    return term["label"]["name"]


def main() -> None:
    parsed_bytes = subprocess.check_output(
        [
            "kast",
            str(PROGRAM),
            "--definition",
            str(DEFINITION),
            "--module",
            "VERIFICATION",
            "--output",
            "json",
        ],
        cwd=WORK,
    )
    parsed = json.loads(parsed_bytes)
    module_term = parsed["term"]
    assert label(module_term).startswith("Module(_)")
    module_stmts = module_term["args"][0]
    assert label(module_stmts).startswith("___MPY-SYNTAX_Stmts_Stmt_Stmts")
    function = module_stmts["args"][0]
    rest = module_stmts["args"][1]
    assert label(rest).startswith('.List{"___MPY-SYNTAX_Stmts_Stmt_Stmts"}')
    assert label(function).startswith("FuncDef(_,_,_)")
    name, params, body = function["args"]
    assert name["token"] == '"triples_sum_to_zero"'
    assert label(params).startswith("Params(_)")
    param_names = params["args"][0]
    assert label(param_names).startswith("_,__MPY-SYNTAX_ParamNames")
    assert param_names["args"][0]["token"] == '"l"'
    assert label(param_names["args"][1]).startswith(
        '.List{"_,__MPY-SYNTAX_ParamNames_String_ParamNames"}'
    )

    body_document = {"format": "KAST", "version": 3, "term": body}
    body_path = WORK / "solution-body-kast.json"
    body_path.write_text(json.dumps(body_document, separators=(",", ":")) + "\n")
    body_pretty = subprocess.check_output(
        [
            "kast",
            str(body_path),
            "--input",
            "json",
            "--output",
            "pretty",
            "--definition",
            str(DEFINITION),
            "--module",
            "VERIFICATION",
        ],
        cwd=WORK,
        text=True,
    ).strip()

    pinning = f'''requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim [body-constructor-identity]:
    <k>
      programBody()
      =>
      {body_pretty}
    </k>

  claim [closure-constructor-identity]:
    <k>
      triplesClosure()
      =>
      closureVal(("l", .ParamNames), {body_pretty}, 0)
    </k>

  claim [binding-constructor-identity]:
    <k> .K </k>
    <scopes>
      0 |-> scope(
        (solutionBindings()
          =>
          "triples_sum_to_zero"
            |-> closureVal(("l", .ParamNames), {body_pretty}, 0)),
        parent(-1))
      ...
    </scopes>
endmodule
'''
    (WORK / "pinning-spec.k").write_text(pinning)
    print("SOURCE_MODULE_LABEL=" + label(module_term))
    print("SOURCE_FUNCTION_LABEL=" + label(function))
    print("SOURCE_FUNCTION_NAME=triples_sum_to_zero")
    print("SOURCE_PARAMETERS=l")
    print("SOURCE_TRAILING_STATEMENTS=.Stmts")
    print(f"BODY_KAST_BYTES={body_path.stat().st_size}")
    print(f"BODY_PRETTY_BYTES={len(body_pretty.encode())}")
    print("GENERATED_SPEC=" + str(WORK / "pinning-spec.k"))


if __name__ == "__main__":
    main()
