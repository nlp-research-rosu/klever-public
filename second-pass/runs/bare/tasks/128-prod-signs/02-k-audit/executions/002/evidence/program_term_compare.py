#!/usr/bin/env python3
"""Mechanically compare solution.mpy with the claim's expanded program constants."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


WORK = Path("/tmp/audit-work/fresh")
VERIFICATION = WORK / "verification.k"


def extract_rule_rhs(text: str, rule_head: str, following_marker: str) -> str:
    start = text.index(rule_head) + len(rule_head)
    end = text.index(following_marker, start)
    return " ".join(text[start:end].strip().split())


def kast_expression(expression: str, sort: str):
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            "verification-kompiled",
            "--module",
            "VERIFICATION",
            "--sort",
            sort,
            "--expression",
            expression,
            "--output",
            "json",
        ],
        cwd=WORK,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    return json.loads(completed.stdout)


def kast_file(path: Path, sort: str):
    completed = subprocess.run(
        [
            "kast",
            "--definition",
            "verification-kompiled",
            "--module",
            "VERIFICATION",
            "--sort",
            sort,
            "--output",
            "json",
            str(path),
        ],
        cwd=WORK,
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, (completed.stdout, completed.stderr)
    return json.loads(completed.stdout)


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/program_term_compare.py")
    text = VERIFICATION.read_text(encoding="utf-8")
    loop_body = extract_rule_rhs(
        text,
        "rule solutionLoopBody =>",
        "syntax Stmts ::= \"solutionBody\"",
    )
    solution_body = extract_rule_rhs(
        text,
        "rule solutionBody =>",
        "syntax Pgm ::= \"solutionProgram\"",
    )
    solution_program = extract_rule_rhs(
        text,
        "rule solutionProgram =>",
        "endmodule",
    )
    assert solution_program.count("solutionBody") == 1
    assert solution_body.count("solutionLoopBody") == 1
    expanded_body = solution_body.replace("solutionLoopBody", loop_body)
    expanded_program = solution_program.replace("solutionBody", expanded_body)
    # The ordinary program parser spells empty list nonterminals by leaving the
    # corresponding constructor slot empty; spec terms spell the same K units
    # explicitly as .Exprs and .Stmts.
    expanded_program_surface = expanded_program.replace(".Exprs", "").replace(
        ".Stmts", ""
    )

    submitted = kast_file(WORK / "solution.mpy", "Pgm")
    claim_program = kast_expression(expanded_program_surface, "Pgm")
    identical = submitted == claim_program
    print(f"solutionLoopBody_rhs={loop_body}")
    print(f"solutionBody_rhs={solution_body}")
    print(f"solutionProgram_rhs={solution_program}")
    print(f"expanded_constructor_ast_identical={str(identical).lower()}")
    if not identical:
        print(f"submitted_ast={json.dumps(submitted, sort_keys=True)}")
        print(f"claim_ast={json.dumps(claim_program, sort_keys=True)}")
        raise SystemExit(1)
    print("STATUS: PASS")


if __name__ == "__main__":
    main()
