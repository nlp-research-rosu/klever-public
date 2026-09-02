#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and solutionPgm."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


SCRATCH = Path("/tmp/audit-work/112-reverse-delete")
DEFINITION = SCRATCH / "audit-verification-kompiled"


def extract_balanced_term(source: str, marker: str) -> str:
    start = source.index(marker)
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quoted:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise RuntimeError("unbalanced constructor term")


def kast(term: str) -> dict:
    command = [
        "kast",
        "--expression",
        term,
        "--definition",
        str(DEFINITION),
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    print("COMMAND:", " ".join(command[:2] + ["<TERM>"] + command[3:]))
    print("EXIT:", completed.returncode)
    if completed.returncode:
        print(completed.stdout)
        raise RuntimeError("kast failed")
    return json.loads(completed.stdout)


def main() -> int:
    submitted = (SCRATCH / "solution.mpy").read_text()
    verification = (SCRATCH / "verification.k").read_text()
    proof_term = extract_balanced_term(
        verification[verification.index("rule solutionPgm =>") :], "Module("
    )
    # `.Stmts` is K's generated unit label for the empty `List{Stmt, ""}`.
    # The program parser spells the same unit as an empty list position.
    unit_count = proof_term.count(".Stmts")
    normalized_proof_term = proof_term.replace(".Stmts", "")
    print(f"normalized_generated_empty_stmts_units={unit_count}")
    submitted_ast = kast(submitted)
    proof_ast = kast(normalized_proof_term)
    submitted_json = json.dumps(submitted_ast, sort_keys=True, separators=(",", ":"))
    proof_json = json.dumps(proof_ast, sort_keys=True, separators=(",", ":"))
    print(
        "submitted_kast_sha256="
        + hashlib.sha256(submitted_json.encode()).hexdigest()
    )
    print("proof_kast_sha256=" + hashlib.sha256(proof_json.encode()).hexdigest())
    print(f"constructor_terms_equal={submitted_ast == proof_ast}")
    return int(submitted_ast != proof_ast)


if __name__ == "__main__":
    raise SystemExit(main())
