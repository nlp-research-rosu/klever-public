#!/usr/bin/env python3
"""Mechanically compare the Program constructor in SPEC with solution.mpy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys


ROOT = Path("/tmp/audit-work/change-base-audit-20260726/candidate")


def balanced_constructor(text: str, start: int) -> str:
    depth = 0
    quote = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quote = False
            continue
        if char == '"':
            quote = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return text[start:index + 1]
    raise ValueError("unbalanced constructor term")


def parse_kast(source: str, from_file: bool) -> tuple[dict, list[str]]:
    command = [
        "kast",
        "--definition",
        "verification-fresh-kompiled",
        "--sort",
        "Program",
        "--module",
        "MPY-SYNTAX",
        "--output",
        "json",
    ]
    if from_file:
        command.insert(1, source)
    else:
        command.extend(["--expression", source])
    process = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if process.returncode != 0:
        print(process.stdout)
        raise RuntimeError(f"kast failed with exit {process.returncode}: {command}")
    return json.loads(process.stdout), command


spec_text = (ROOT / "spec.k").read_text()
start = spec_text.index("Module(")
claim_program = balanced_constructor(spec_text, start)
# `.Stmts` is K's internal spelling of the empty List{Stmt,""} unit.  The
# program parser accepts the equivalent concrete spelling as an empty field.
normalized_claim_program = claim_program.replace(".Stmts", "")
if claim_program.count(".Stmts") != 1:
    raise RuntimeError("expected exactly one explicit empty Stmts constructor")

solution_ast, solution_command = parse_kast("solution.mpy", from_file=True)
claim_ast, claim_command = parse_kast(normalized_claim_program, from_file=False)

solution_canonical = json.dumps(solution_ast, sort_keys=True, separators=(",", ":"))
claim_canonical = json.dumps(claim_ast, sort_keys=True, separators=(",", ":"))

print(f"solution_command={solution_command!r}")
print(f"claim_command={claim_command!r}")
print(f"claim_program_source={claim_program}")
print("normalization=.Stmts replaced by equivalent empty List{Stmt,\"\"} field")
print(
    "solution_kast_sha256="
    + hashlib.sha256(solution_canonical.encode()).hexdigest()
)
print(
    "claim_program_kast_sha256="
    + hashlib.sha256(claim_canonical.encode()).hexdigest()
)
print(f"constructor_level_identity={solution_ast == claim_ast}")

sys.exit(0 if solution_ast == claim_ast else 1)
