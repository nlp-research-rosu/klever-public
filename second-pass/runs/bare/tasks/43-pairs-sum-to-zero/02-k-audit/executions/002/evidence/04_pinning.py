#!/usr/bin/env python3
"""Mechanical constructor-level comparison of submitted and claimed programs."""

from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path("/tmp/audit-work/43-pairs-sum-to-zero")
CANDIDATE = ROOT / "candidate"
DEFINITION = ROOT / "proof-kompiled"


def extract_balanced_module(text: str, offset: int) -> tuple[str, int]:
    start = text.index("Module(", offset)
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
                return text[start : index + 1], index + 1
    raise AssertionError("unterminated Module term")


def parse_expression(expression: str) -> bytes:
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            str(DEFINITION),
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Program",
            "--output",
            "kore",
            "--expression",
            expression,
        ],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def parse_file(path: Path) -> bytes:
    completed = subprocess.run(
        [
            "kast",
            str(path),
            "--definition",
            str(DEFINITION),
            "--module",
            "MPY-SYNTAX",
            "--sort",
            "Program",
            "--output",
            "kore",
        ],
        check=True,
        capture_output=True,
    )
    return completed.stdout


def main() -> None:
    submitted = parse_file(CANDIDATE / "solution.mpy")
    spec = (CANDIDATE / "spec.k").read_text()
    k_module, end = extract_balanced_module(spec, spec.index("<k>"))
    program_module, _ = extract_balanced_module(spec, spec.index("<program>", end))
    # `.Stmts` is the internal empty-list spelling accepted in K rules but not
    # by the standalone program scanner.  Omitting it is exactly the
    # translator's concrete-syntax spelling for the same empty/list tail.
    k_normalizations = k_module.count(".Stmts")
    program_normalizations = program_module.count(".Stmts")
    k_module = k_module.replace(".Stmts", "")
    program_module = program_module.replace(".Stmts", "")
    parsed_k_module = parse_expression(k_module)
    parsed_program_module = parse_expression(program_module)

    print(
        "COMMAND: kast candidate/solution.mpy and each balanced Module term "
        "from spec.k as sort Program, output KORE; omit internal .Stmts "
        "empty-list spellings for standalone parsing"
    )
    print(
        "semantically_inert_empty_list_normalizations:",
        k_normalizations,
        program_normalizations,
    )
    for label, value in (
        ("submitted_solution_mpy", submitted),
        ("claim_k_run_module", parsed_k_module),
        ("claim_program_cell_module", parsed_program_module),
    ):
        print(label, "sha256=", hashlib.sha256(value).hexdigest(), "bytes=", len(value))
    print("k_run_module_constructor_identity:", submitted == parsed_k_module)
    print("program_cell_constructor_identity:", submitted == parsed_program_module)
    assert submitted == parsed_k_module
    assert submitted == parsed_program_module
    print("PINNING_EXIT_STATUS: 0")


if __name__ == "__main__":
    main()
