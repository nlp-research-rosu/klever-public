#!/usr/bin/env python3
"""Build mechanical AST-identity and concrete-summary witness specs."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess


WORK = Path("/tmp/audit-work/candidate-clean")
CANONICAL = Path("/tmp/audit-work/trusted/canonical.py")
SOLUTION = WORK / "solution.py"
MPY = WORK / "solution.mpy"


def import_function(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.make_palindrome


def int_seq(value: str) -> str:
    term = ".IntSeq"
    for code_point in reversed([ord(char) for char in value]):
        term = f"iCons({code_point}, {term})"
    return term


actual = import_function("audit_candidate_stage4", SOLUTION)
canonical = import_function("audit_canonical_stage4", CANONICAL)

kast_command = [
    "kast",
    str(MPY),
    "--definition",
    str(WORK / "verification-audit-kompiled"),
    "--module",
    "VERIFICATION-SYNTAX",
    "--sort",
    "Module",
    "--output",
    "pretty",
]
parsed_program = subprocess.run(
    kast_command,
    cwd=WORK,
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()
(Path("/audit-output/evidence") / "stage4_solution_parsed_pretty.k").write_text(
    parsed_program + "\n", encoding="utf-8"
)

ast_spec = (
    'requires "verification.k"\n\n'
    "module AST-IDENTITY\n"
    "  imports VERIFICATION\n\n"
    "  claim solutionModule\n"
    "    => "
    + parsed_program
    + "\n"
    "endmodule\n"
)
(WORK / "ast-identity.k").write_text(ast_spec, encoding="utf-8")

inputs = ["", "cat", "cata", "abba", "🙂a", "\ud800a"]
witnesses = []
claims = []
for index, value in enumerate(inputs):
    candidate_result = actual(value)
    canonical_result = canonical(value)
    assert candidate_result == canonical_result
    witnesses.append(
        {
            "index": index,
            "input": value,
            "input_code_points": [ord(char) for char in value],
            "candidate": candidate_result,
            "canonical": canonical_result,
            "result_code_points": [ord(char) for char in candidate_result],
        }
    )
    claims.append(
        f"  claim [ground-{index}]:\n"
        "    <k>\n"
        f"      completePal({int_seq(value)})\n"
        f"      => {int_seq(candidate_result)}\n"
        "    </k>\n"
    )

ground_spec = (
    'requires "verification.k"\n\n'
    "module ADEQUACY-GROUND\n"
    "  imports VERIFICATION\n\n"
    + "\n".join(claims)
    + "endmodule\n"
)
(WORK / "adequacy-ground.k").write_text(ground_spec, encoding="utf-8")

print("mechanical_ast_rhs_source=/tmp/audit-work/candidate-clean/solution.mpy")
print("mechanical_parser_command=" + " ".join(kast_command))
print("ast_identity_spec=/tmp/audit-work/candidate-clean/ast-identity.k")
print("ground_spec=/tmp/audit-work/candidate-clean/adequacy-ground.k")
for witness in witnesses:
    print(json.dumps(witness, ensure_ascii=True, sort_keys=True))
