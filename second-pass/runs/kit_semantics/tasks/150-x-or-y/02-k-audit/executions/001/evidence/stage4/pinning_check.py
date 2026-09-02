#!/usr/bin/env python3
"""Mechanically compare the executed #loadAll module with solution.mpy."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/reconstruction")
SPEC = WORK / "spec.k"
SOLUTION = WORK / "solution.mpy"
EXTRACTED = WORK / "spec-executed-module.mpy"
DEFINITION = WORK / "verification-audit-kompiled"


def balanced_argument(text: str, marker: str) -> str:
    start = text.index(marker) + len(marker)
    depth = 1
    in_string = False
    escaped = False
    for offset, character in enumerate(text[start:], start):
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
                return text[start:offset].strip() + "\n"
    raise ValueError(f"unterminated {marker}")


def parse_module(path: Path, output: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "VERIFICATION-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
        "--output-file",
        str(output),
    ]
    print("COMMAND " + " ".join(command))
    completed = subprocess.run(command, check=False)
    print(f"EXIT {completed.returncode}")
    if completed.returncode:
        raise SystemExit(completed.returncode)
    return json.loads(output.read_text())["term"]


spec_text = SPEC.read_text()
executed_module = balanced_argument(spec_text, "#loadAll(")
# `.Stmts` is the declared identity of the Stmts list. The program parser uses
# an omitted list tail for that same constructor, so remove only this identity.
identity_count = executed_module.count(" .Stmts")
normalized_executed_module = executed_module.replace(" .Stmts", "")
EXTRACTED.write_text(normalized_executed_module)
print(f"extracted_path={EXTRACTED}")
print(f"extracted_sha256={hashlib.sha256(executed_module.encode()).hexdigest()}")
print(f"removed_stmts_identity_count={identity_count}")
print(
    "normalized_extracted_sha256="
    f"{hashlib.sha256(normalized_executed_module.encode()).hexdigest()}"
)
print(f"submitted_sha256={hashlib.sha256(SOLUTION.read_bytes()).hexdigest()}")

solution_term = parse_module(SOLUTION, WORK / "solution.kast.json")
executed_term = parse_module(EXTRACTED, WORK / "spec-executed-module.kast.json")
equal = solution_term == executed_term
normalized = json.dumps(solution_term, sort_keys=True, separators=(",", ":")).encode()
print(f"constructor_terms_equal={equal}")
print(f"constructor_term_sha256={hashlib.sha256(normalized).hexdigest()}")
raise SystemExit(0 if equal else 1)
