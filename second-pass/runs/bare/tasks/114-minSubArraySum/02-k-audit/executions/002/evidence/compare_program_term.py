#!/usr/bin/env python3
"""Mechanically compare the submitted Program term with solutionProgram's RHS."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

VERIFICATION = Path("/tmp/audit-work/source/verification.k")
SUBMITTED = Path("/candidate/solution.mpy")
EXTRACTED = Path("/tmp/audit-work/source/solutionProgram-rhs.mpy")
DEFINITION = Path("/tmp/audit-work/build/verification-kompiled")


def extract_balanced_term(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    start = text.index("Module", start)
    opening = text.index("(", start)
    depth = 0
    in_string = False
    escaped = False
    for index in range(opening, len(text)):
        character = text[index]
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
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start : index + 1].strip() + "\n"
    raise ValueError("unbalanced solutionProgram RHS")


def parse(path: Path) -> tuple[int, str, object | None]:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Program",
        "--output",
        "json",
    ]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    parsed = json.loads(completed.stdout) if completed.returncode == 0 else None
    print(f"command={command!r}")
    print(f"exit_status={completed.returncode}")
    print(f"stderr={completed.stderr!r}")
    return completed.returncode, completed.stdout, parsed


def main() -> int:
    term = extract_balanced_term(
        VERIFICATION.read_text(encoding="utf-8"), "rule solutionProgram =>"
    )
    empty_stmt_markers = term.count(".Stmts")
    term = term.replace(".Stmts", "")
    EXTRACTED.write_text(term, encoding="utf-8")
    print(f"normalized_empty_Stmts_markers={empty_stmt_markers}")
    print(f"submitted_sha256={hashlib.sha256(SUBMITTED.read_bytes()).hexdigest()}")
    print(f"extracted_text_sha256={hashlib.sha256(term.encode()).hexdigest()}")
    submitted_status, submitted_json, submitted = parse(SUBMITTED)
    extracted_status, extracted_json, extracted = parse(EXTRACTED)
    print(f"submitted_kast_sha256={hashlib.sha256(submitted_json.encode()).hexdigest()}")
    print(f"extracted_kast_sha256={hashlib.sha256(extracted_json.encode()).hexdigest()}")
    print(f"constructor_level_identity={submitted == extracted}")
    return (
        0
        if submitted_status == 0 and extracted_status == 0 and submitted == extracted
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
