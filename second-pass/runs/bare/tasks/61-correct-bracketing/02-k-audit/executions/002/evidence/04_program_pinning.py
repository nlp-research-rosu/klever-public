#!/usr/bin/env python3
"""Mechanically compare the submitted translated AST with solutionProgram."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


CANDIDATE = Path("/tmp/audit-work/61-correct-bracketing-audit/candidate")
DEFINITION = CANDIDATE / "proof-kompiled"
submitted_text = (CANDIDATE / "solution.mpy").read_text().strip()
verification_text = (CANDIDATE / "verification.k").read_text()
marker = "rule solutionProgram =>"
next_comment = "// Declarative reference checker."
if verification_text.count(marker) != 1 or verification_text.count(next_comment) != 1:
    raise RuntimeError("cannot uniquely extract solutionProgram equation")
claim_text = verification_text.split(marker, 1)[1].split(next_comment, 1)[0].strip()


def parse(term: str, *, input_mode: str, module: str) -> dict:
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            str(DEFINITION),
            "--module",
            module,
            "--input",
            input_mode,
            "--expression",
            term,
            "--output",
            "json",
        ],
        cwd=CANDIDATE,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"kast failed ({completed.returncode}):\n{completed.stdout}\n{completed.stderr}"
        )
    return json.loads(completed.stdout)


submitted_ast = parse(
    submitted_text, input_mode="program", module="MPY-SYNTAX"
)
claim_rule_ast = parse(
    "solutionProgram => " + claim_text,
    input_mode="rule",
    module="MPY-VERIFICATION",
)
submitted_term = submitted_ast["term"]
claim_rewrite = claim_rule_ast["term"]
if claim_rewrite.get("node") != "KRewrite":
    raise RuntimeError("solutionProgram equation did not parse as a rewrite")
claim_term = claim_rewrite["rhs"]
same = submitted_term == claim_term
summary = {
    "submitted_file": str(CANDIDATE / "solution.mpy"),
    "verification_file": str(CANDIDATE / "verification.k"),
    "submitted_sha256": hashlib.sha256(
        (submitted_text + "\n").encode()
    ).hexdigest(),
    "extraction_marker_count": verification_text.count(marker),
    "submitted_kast_module": "MPY-SYNTAX",
    "submitted_kast_input": "program",
    "claim_kast_module": "MPY-VERIFICATION",
    "claim_kast_input": "rule",
    "constructor_ast_identical": same,
    "submitted_top_node": submitted_term.get("node"),
    "claim_top_node": claim_term.get("node"),
}
print(json.dumps(summary, indent=2))
if not same:
    print("SUBMITTED:")
    print(json.dumps(submitted_term, indent=2))
    print("CLAIM:")
    print(json.dumps(claim_term, indent=2))
raise SystemExit(0 if same else 1)
