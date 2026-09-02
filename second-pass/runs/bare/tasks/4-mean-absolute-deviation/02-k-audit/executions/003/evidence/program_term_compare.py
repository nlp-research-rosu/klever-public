#!/usr/bin/env python3
"""Mechanically compare the parsed submitted MPY with solutionProgram's RHS."""

from __future__ import annotations

import hashlib
from pathlib import Path
import shlex
import subprocess


ROOT = Path("/tmp/audit-work/4-mad-audit/candidate")
DEFINITION = ROOT / "verification-audit-kompiled"
PARSED_DEFINITION = DEFINITION / "parsed.txt"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    command = [
        "kast",
        "solution.mpy",
        "--definition",
        "verification-audit-kompiled",
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "ModuleAst",
        "--output",
        "kast",
    ]
    print("command:", shlex.join(command))
    parsed_program = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.strip()

    matching_lines = [
        line.strip()
        for line in PARSED_DEFINITION.read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("rule `solutionProgram_VERIFICATION_ModuleAst`")
    ]
    if len(matching_lines) != 1:
        print(f"unexpected solutionProgram rules: {len(matching_lines)}")
        return 2
    rule = matching_lines[0]
    lhs_rhs, separator, _conditions = rule.partition(" requires ")
    if not separator:
        print("could not isolate solutionProgram rule conditions")
        return 2
    _lhs, rewrite_separator, rhs = lhs_rhs.partition("=>")
    if not rewrite_separator:
        print("could not isolate solutionProgram RHS")
        return 2
    rhs = rhs.strip()

    same = parsed_program == rhs
    print(f"submitted_parsed_sha256={digest(parsed_program)}")
    print(f"solutionProgram_rhs_sha256={digest(rhs)}")
    print(f"constructor_terms_byte_equal={same}")
    print(f"submitted_term_length={len(parsed_program)} rhs_length={len(rhs)}")
    return 0 if same else 1


if __name__ == "__main__":
    raise SystemExit(main())
