#!/usr/bin/env python3
"""Mechanical source/body/constructor checks for the term used by the K claim."""

from __future__ import annotations

import ast
import json
from pathlib import Path
import re
import subprocess


scratch = Path("/tmp/audit-work/54-same-chars")
candidate_dir = scratch / "candidate"
reference_dir = scratch / "reference"


def function(path: Path) -> ast.FunctionDef:
    module = ast.parse(path.read_text(encoding="utf-8"))
    matches = [
        node
        for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == "same_chars"
    ]
    assert len(matches) == 1
    return matches[0]


canonical_function = function(reference_dir / "canonical.py")
candidate_function = function(candidate_dir / "solution.py")
canonical_body = list(canonical_function.body)
if (
    canonical_body
    and isinstance(canonical_body[0], ast.Expr)
    and isinstance(canonical_body[0].value, ast.Constant)
    and isinstance(canonical_body[0].value.value, str)
):
    canonical_body.pop(0)

assert [argument.arg for argument in canonical_function.args.args] == ["s0", "s1"]
assert [argument.arg for argument in candidate_function.args.args] == ["s0", "s1"]
assert ast.dump(ast.Module(body=canonical_body, type_ignores=[])) == ast.dump(
    ast.Module(body=candidate_function.body, type_ignores=[])
)
print("AST BODY IDENTITY OK canonical return body equals candidate return body")

translated = subprocess.run(
    [
        "python3",
        str(reference_dir / "py2mpy.py"),
        str(candidate_dir / "solution.py"),
    ],
    check=True,
    capture_output=True,
    text=True,
).stdout
submitted = (candidate_dir / "solution.mpy").read_text(encoding="utf-8")
assert translated == submitted
print("TRANSLATION IDENTITY OK trusted output equals submitted solution.mpy")

embedded_source = (candidate_dir / "solution-program.k").read_text(encoding="utf-8")
match = re.search(
    r"\brule\s+solutionProgram\s*=>\s*(.*?)\s*endmodule\s*\Z",
    embedded_source,
    re.DOTALL,
)
assert match is not None
embedded_rhs = match.group(1)


def kast(expression: str) -> dict:
    result = subprocess.run(
        [
            "kast",
            "--definition",
            "proof-kompiled",
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Program",
            "--output",
            "json",
            "--expression",
            expression,
        ],
        cwd=candidate_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


translated_kast = kast(translated)
embedded_kast = kast(embedded_rhs)
assert translated_kast == embedded_kast
print("KAST CONSTRUCTOR IDENTITY OK solutionProgram RHS equals trusted translation")

spec_source = (candidate_dir / "spec.k").read_text(encoding="utf-8")
claim_count = len(re.findall(r"(?m)^\s*claim\s*$", spec_source))
pinned_count = len(
    re.findall(r"<k>\s*solutionProgram\s*=>\s*\.K\s*</k>", spec_source)
)
assert claim_count == 7
assert pinned_count == claim_count
print(f"CLAIM PINNING OK claims={claim_count} solutionProgram_entries={pinned_count}")
