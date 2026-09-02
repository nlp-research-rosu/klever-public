#!/usr/bin/env python3
"""Mechanically compare the submitted .mpy term with the proof's program term."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/anti-shuffle")
DEFINITION = WORK / "audit-verification-kompiled"


def parse_term(term: str) -> object:
    command = [
        "kast",
        "--expression",
        term,
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION",
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    result = subprocess.run(
        command,
        cwd=WORK,
        check=False,
        capture_output=True,
        text=True,
    )
    print("COMMAND:", subprocess.list2cmdline(command))
    print(f"EXIT_STATUS: {result.returncode}")
    if result.stderr:
        print("STDERR:", result.stderr)
    if result.returncode:
        raise RuntimeError("kast failed")
    return json.loads(result.stdout)


def main() -> int:
    submitted_text = (WORK / "solution.mpy").read_text(encoding="utf-8")
    verification_text = (WORK / "verification.k").read_text(encoding="utf-8")
    start_marker = "rule solutionFunctions =>"
    end_marker = "  // Mathematical reference:"
    start = verification_text.index(start_marker) + len(start_marker)
    end = verification_text.index(end_marker, start)
    function_rhs = verification_text[start:end].strip()
    # `.Stmts` is the internal unit of the List{Stmt,""} production.  In the
    # external .mpy grammar the same unit is written by leaving that list blank.
    function_rhs = function_rhs.replace(".Stmts", "")
    proof_program_text = f"Module(\n{function_rhs})"

    submitted_ast = parse_term(submitted_text)
    proof_ast = parse_term(proof_program_text)
    equal = submitted_ast == proof_ast
    print(f"constructor_ast_equal={equal}")
    print(f"submitted_chars={len(submitted_text)}")
    print(f"extracted_proof_program_chars={len(proof_program_text)}")
    print(
        "proof_program_function_order="
        + ",".join(
            name
            for name in ("insert_char", "process_words", "anti_shuffle")
            if f'FuncDef("{name}"' in proof_program_text
        )
    )
    return 0 if equal else 1


if __name__ == "__main__":
    raise SystemExit(main())
