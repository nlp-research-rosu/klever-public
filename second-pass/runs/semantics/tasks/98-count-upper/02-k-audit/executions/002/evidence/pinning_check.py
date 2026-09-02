#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the module executed by the entry claim."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/98-count-upper")
definition = WORK / "audit-verification-kompiled"
spec_text = (WORK / "spec.k").read_text()


def balanced_term(text: str, start: int) -> str:
    """Extract a constructor term starting at start through its matching ')'."""
    open_at = text.find("(", start)
    if open_at < 0:
        raise ValueError("term has no opening parenthesis")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
            if depth == 0 and index >= open_at:
                return text[start : index + 1]
    raise ValueError("unbalanced constructor term")


load_pos = spec_text.index("#loadAll(")
module_pos = spec_text.index("Module(", load_pos)
claim_module = balanced_term(spec_text, module_pos)
# Spec rules may spell out generated right-unit list constructors (`.Stmts`);
# the program parser omits those concrete tokens.  Removing only these explicit
# units is the inert list normalization being tested.
explicit_stmt_units = claim_module.count(".Stmts")
normalized_claim_module = claim_module.replace(".Stmts", "")


def kast_json(*args: str) -> dict:
    command = [
        "kast",
        "--definition",
        str(definition),
        "--sort",
        "Module",
        "--output",
        "json",
        *args,
    ]
    completed = subprocess.run(
        command,
        cwd=WORK,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    print("COMMAND:", " ".join(command))
    print("EXIT:", completed.returncode)
    if completed.stderr:
        print("STDERR:", completed.stderr[:2000])
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)
    return json.loads(completed.stdout)["term"]


submitted_term = kast_json(str(WORK / "solution.mpy"))
claim_term = kast_json("--expression", normalized_claim_module)

print("extracted_claim_module_chars:", len(claim_module))
print("explicit_.Stmts_units_removed:", explicit_stmt_units)
print("submitted_and_claim_KAST_equal:", submitted_term == claim_term)
if submitted_term != claim_term:
    raise SystemExit(1)
print("RESULT: the entry claim executes the submitted translated Module term")
