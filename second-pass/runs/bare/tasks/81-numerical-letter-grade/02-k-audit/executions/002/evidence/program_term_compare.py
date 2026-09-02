#!/usr/bin/env python3
"""Expand proof-local constructor names and compare them to submitted MPy."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


PROOF_DIR = Path("/tmp/audit-work/reconstruction")


def expression_rhs(source: str, marker: str) -> str:
    marker_at = source.index(marker)
    start = marker_at + len(marker)
    while source[start].isspace():
        start += 1
    depth = 0
    saw_open = False
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        character = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
            saw_open = True
        elif character == ")":
            depth -= 1
            if saw_open and depth == 0:
                return source[start : index + 1]
    raise ValueError(f"unbalanced RHS following {marker!r}")


def kast(term_file: Path) -> bytes:
    result = subprocess.run(
        [
            "kast",
            str(term_file),
            "--definition",
            str(PROOF_DIR / "verification-kompiled"),
            "--module",
            "VERIFICATION",
            "--sort",
            "Module",
            "--output",
            "kore",
        ],
        cwd=PROOF_DIR,
        check=False,
        capture_output=True,
    )
    print(f"COMMAND: {' '.join(result.args)}")
    print(f"EXIT_STATUS: {result.returncode}")
    if result.stderr:
        print(result.stderr.decode(errors="replace"))
    if result.returncode:
        raise RuntimeError(f"kast failed for {term_file}")
    return result.stdout


verification = (PROOF_DIR / "verification.k").read_text(encoding="utf-8")
grading_body = expression_rhs(verification, "rule gradingBody =>")
solution_program = expression_rhs(verification, "rule solutionProgram =>")
if solution_program.count("gradingBody") != 1:
    raise AssertionError("solutionProgram does not contain exactly one gradingBody")
expanded_program = solution_program.replace("gradingBody", grading_body)
# `.Exprs` is K's internal empty-list item used in rules; the external concrete
# MPy grammar spells the same empty list by placing no text between parentheses.
expanded_program = expanded_program.replace(".Exprs", "")

expanded_path = Path("/tmp/audit-work/expanded-solutionProgram.mpy")
expanded_path.write_text(expanded_program + "\n", encoding="utf-8")

submitted_kore = kast(PROOF_DIR / "solution.mpy")
expanded_kore = kast(expanded_path)
Path("/tmp/audit-work/submitted-solution.kore").write_bytes(submitted_kore)
Path("/tmp/audit-work/expanded-solutionProgram.kore").write_bytes(expanded_kore)

submitted_hash = hashlib.sha256(submitted_kore).hexdigest()
expanded_hash = hashlib.sha256(expanded_kore).hexdigest()
print(f"submitted_KORE_sha256={submitted_hash}")
print(f"expanded_solutionProgram_KORE_sha256={expanded_hash}")
print(f"constructor_level_equal={submitted_kore == expanded_kore}")
if submitted_kore != expanded_kore:
    raise AssertionError("proof solutionProgram differs from submitted solution.mpy")
print("PROGRAM_TERM_COMPARE: PASS")
