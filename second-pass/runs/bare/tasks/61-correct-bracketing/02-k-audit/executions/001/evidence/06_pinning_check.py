#!/usr/bin/env python3
"""Mechanically compare solutionProgram's constructor term with solution.mpy."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

scratch = Path("/tmp/audit-work/candidate-src")
submitted = (scratch / "solution.mpy").read_text()
verification = (scratch / "verification.k").read_text()

marker = "rule solutionProgram =>"
next_comment = "// Declarative reference checker."
if marker not in verification or next_comment not in verification:
    raise SystemExit("could not extract solutionProgram equation")
embedded = verification.split(marker, 1)[1].split(next_comment, 1)[0].strip()


def compact(text: str) -> str:
    # The compared constructor terms contain no whitespace inside string
    # literals; stripping all whitespace therefore gives a stable token check.
    return re.sub(r"\s+", "", text)


submitted_compact = compact(submitted)
embedded_compact = compact(embedded)
definition = scratch / "verification-audit-kompiled"
base_command = [
    "kast",
    "--definition",
    str(definition),
    "--module",
    "MPY-SYNTAX",
    "--sort",
    "Pgm",
    "--output",
    "json",
]
submitted_kast = json.loads(
    subprocess.check_output(base_command + ["solution.mpy"], cwd=scratch, text=True)
)
embedded_kast = json.loads(
    subprocess.check_output(
        # The external List{Stmt,""} parser spells the unit as an omitted
        # argument; K source rules may spell the same unit as .Stmts.
        base_command + ["--expression", embedded.replace(".Stmts", "")],
        cwd=scratch,
        text=True,
    )
)
same = submitted_kast["term"] == embedded_kast["term"]
main_needle = 'Run(solutionProgram, "correct_bracketing", S:String)'
main_uses_solution = main_needle in (scratch / "spec.k").read_text()
print(f"submitted_sha256={hashlib.sha256(submitted.encode()).hexdigest()}")
print(f"submitted_compact_sha256={hashlib.sha256(submitted_compact.encode()).hexdigest()}")
print(f"embedded_compact_sha256={hashlib.sha256(embedded_compact.encode()).hexdigest()}")
print(f"text_compact_equal={str(submitted_compact == embedded_compact).lower()}")
print("text_difference_reason=translator empty else list uses omitted text; embedded term spells .Stmts")
print(f"parsed_constructor_terms_equal={str(same).lower()}")
print(f"spec_main_uses_Run_solutionProgram={str(main_uses_solution).lower()}")
raise SystemExit(0 if same else 1)
