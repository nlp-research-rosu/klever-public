#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the SolutionModule rule RHS."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/25-factorize")
VERIFICATION = WORK / "verification.k"
SUBMITTED = WORK / "solution.mpy"
EXTRACTED_K_TERM = Path(
    "/audit-output/evidence/extracted-solution-module-k-term.txt"
)
EXTRACTED_CONCRETE = Path(
    "/audit-output/evidence/extracted-solution-module.mpy"
)
DEFINITION = WORK / "fresh-verification-kompiled"


def extract_solution_module_rhs(text: str) -> str:
    marker = "rule SolutionModule() =>"
    start = text.index(marker) + len(marker)
    while text[start].isspace():
        start += 1
    if not text.startswith("Module(", start):
        raise AssertionError("SolutionModule RHS does not begin with Module(")
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
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
                return text[start : index + 1] + "\n"
    raise AssertionError("unbalanced SolutionModule RHS")


def kast(path: Path) -> tuple[dict[str, object], str]:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Module",
        "--output",
        "json",
    ]
    print("$ " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"EXIT STATUS: {result.returncode}")
    if result.stderr:
        print(result.stderr.rstrip())
    if result.returncode != 0:
        raise RuntimeError(f"kast failed for {path}")
    return json.loads(result.stdout), result.stdout


def main() -> int:
    extracted_text = extract_solution_module_rhs(
        VERIFICATION.read_text(encoding="utf-8")
    )
    EXTRACTED_K_TERM.write_text(extracted_text, encoding="utf-8")
    expr_units = extracted_text.count(".Exprs")
    stmt_units = extracted_text.count(".Stmts")
    concrete_text = extracted_text.replace(".Exprs", "").replace(".Stmts", "")
    EXTRACTED_CONCRETE.write_text(concrete_text, encoding="utf-8")
    print(
        "EXTRACTED raw SolutionModule RHS from verification.k to "
        f"{EXTRACTED_K_TERM} bytes={len(extracted_text.encode())}"
    )
    print(
        "NORMALIZED only explicit associative-list unit tokens for concrete "
        f"parsing: .Exprs count={expr_units}, .Stmts count={stmt_units}; "
        f"wrote {EXTRACTED_CONCRETE}"
    )

    submitted_ast, submitted_json = kast(SUBMITTED)
    extracted_ast, extracted_json = kast(EXTRACTED_CONCRETE)
    equal = submitted_ast == extracted_ast
    print(f"SUBMITTED_KAST_JSON_BYTES={len(submitted_json.encode())}")
    print(f"EXTRACTED_KAST_JSON_BYTES={len(extracted_json.encode())}")
    print(f"CONSTRUCTOR_AST_EQUAL={equal}")
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
