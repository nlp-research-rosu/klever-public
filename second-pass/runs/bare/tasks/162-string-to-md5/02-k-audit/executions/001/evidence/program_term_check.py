#!/usr/bin/env python3
"""Mechanical constructor-token comparison of solution.mpy and proof macros."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path("/tmp/audit-work/reconstruction")


TOKEN = re.compile(
    r'''
    "(?:\\.|[^"\\])*"       # K string token
    | \.[A-Za-z][A-Za-z0-9]* # dot constructor such as .Stmts
    | [A-Za-z#][A-Za-z0-9#]* # constructor/identifier
    | [(),]                   # punctuation relevant to this term
    ''',
    re.VERBOSE,
)


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def rule_rhs(source: str, name: str, following: str) -> list[str]:
    match = re.search(
        rf"\brule\s+{re.escape(name)}\s*=>\s*(.*?)\n\s*{re.escape(following)}",
        source,
        re.DOTALL,
    )
    if match is None:
        raise ValueError(f"cannot extract rule for {name}")
    return tokens(match.group(1))


def main() -> int:
    actual = tokens((ROOT / "solution.mpy").read_text(encoding="utf-8"))
    verification = (ROOT / "verification.k").read_text(encoding="utf-8")
    body = rule_rhs(verification, "solutionBody", "syntax Program")
    program = rule_rhs(verification, "solutionProgram", "// Mathematical result")

    if not body or body[-1] != ".Stmts":
        raise ValueError("solutionBody does not end in explicit .Stmts")
    body_without_unit = body[:-1]
    occurrences = [index for index, token in enumerate(program) if token == "solutionBody"]
    if len(occurrences) != 1:
        raise ValueError(f"unexpected solutionBody occurrences: {occurrences}")
    expanded = (
        program[: occurrences[0]]
        + body_without_unit
        + program[occurrences[0] + 1 :]
    )

    print(f"actual constructor-token count: {len(actual)}")
    print(f"expanded proof constructor-token count: {len(expanded)}")
    print(f"solutionBody token count including list unit: {len(body)}")
    print("actual:", " ".join(actual))
    print("expanded:", " ".join(expanded))
    equal = actual == expanded
    print(f"CONSTRUCTOR_IDENTITY: {'yes' if equal else 'no'}")
    if not equal:
        for index, pair in enumerate(zip(actual, expanded)):
            if pair[0] != pair[1]:
                print(
                    f"first mismatch index={index} actual={pair[0]!r} "
                    f"expanded={pair[1]!r}"
                )
                break
    return 0 if equal else 1


if __name__ == "__main__":
    sys.exit(main())
