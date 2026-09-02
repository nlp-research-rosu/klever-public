#!/usr/bin/env python3
"""Constructor-level comparison of solution.mpy and solutionProgram's RHS."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


VERIFICATION = Path("/candidate/verification.k")
SUBMITTED = Path("/candidate/solution.mpy")
REGENERATED = Path("/tmp/audit-work/regenerated-solution.mpy")
DEFINITION = Path("/tmp/audit-work/build/verification-haskell-kompiled")


def extract_balanced_module(source: str) -> str:
    marker = "rule solutionProgram =>"
    marker_at = source.index(marker)
    start = source.index("Module(", marker_at + len(marker))
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(source)):
        character = source[index]
        if quoted:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                quoted = False
            continue
        if character == '"':
            quoted = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return source[start : index + 1]
    raise RuntimeError("unterminated solutionProgram Module term")


def parse_file(path: Path) -> dict:
    command = [
        "kast",
        str(path),
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    print("COMMAND: " + " ".join(command))
    print(f"EXIT_STATUS: {result.returncode}")
    return json.loads(result.stdout)["term"]


def parse_expression(expression: str) -> dict:
    # Rule syntax denotes an empty user list as `.Stmts`; the concrete Pgm
    # parser denotes the same zero-element list by an empty position.
    expression = expression.replace(".Stmts", "")
    command = [
        "kast",
        "--expression",
        expression,
        "--definition",
        str(DEFINITION),
        "--module",
        "MPY-SYNTAX",
        "--sort",
        "Pgm",
        "--output",
        "json",
    ]
    result = subprocess.run(command, check=True, text=True, capture_output=True)
    printable = command.copy()
    printable[2] = f"<solutionProgram RHS: {len(expression)} chars>"
    print("COMMAND: " + " ".join(printable))
    print(f"EXIT_STATUS: {result.returncode}")
    return json.loads(result.stdout)["term"]


def main() -> int:
    source = VERIFICATION.read_text()
    literal = extract_balanced_module(source)
    submitted_ast = parse_file(SUBMITTED)
    regenerated_ast = parse_file(REGENERATED)
    embedded_ast = parse_expression(literal)

    submitted_bytes = SUBMITTED.read_bytes()
    regenerated_bytes = REGENERATED.read_bytes()
    byte_equal = submitted_bytes == regenerated_bytes
    submitted_embedded_equal = submitted_ast == embedded_ast
    regenerated_embedded_equal = regenerated_ast == embedded_ast

    compact = " ".join(source.split())
    verify_chain = (
        'rule <k> verify(ARGS) => call("has_close_elements", ARGS, solutionFunctions) ... </k>'
        in compact
        and "rule solutionFunctions => functionsOf(solutionProgram)" in compact
        and "rule functionsOf(Module(SS)) => collect(SS)" in compact
    )

    print(f"submitted_sha256={hashlib.sha256(submitted_bytes).hexdigest()}")
    print(f"regenerated_sha256={hashlib.sha256(regenerated_bytes).hexdigest()}")
    print(f"translator_byte_identity={byte_equal}")
    print(f"submitted_ast_equals_embedded_ast={submitted_embedded_equal}")
    print(f"regenerated_ast_equals_embedded_ast={regenerated_embedded_equal}")
    print(f"verify_to_solutionProgram_chain_present={verify_chain}")
    return 0 if all(
        [
            byte_equal,
            submitted_embedded_equal,
            regenerated_embedded_equal,
            verify_chain,
        ]
    ) else 1


if __name__ == "__main__":
    raise SystemExit(main())
