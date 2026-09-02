#!/usr/bin/env python3
"""Mechanical constructor-token comparison for source-to-claim program pinning."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|[A-Za-z_.][A-Za-z0-9_.-]*|-?[0-9]+|[(),]')


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def main() -> None:
    work = Path("/tmp/audit-work/candidate-src")
    translated = (work / "solution.mpy").read_text()
    verification = (work / "verification.k").read_text()
    spec = (work / "spec.k").read_text()

    match = re.search(
        r"rule\s+solutionModule\(\)\s*=>\s*(Module\(.*?\))\s*\n\s*\n"
        r"\s*syntax\s+Expr\s+::=\s+filterExpression",
        verification,
        re.DOTALL,
    )
    if match is None:
        raise RuntimeError("could not isolate solutionModule RHS")
    translated_tokens = tokens(translated)
    theorem_tokens = tokens(match.group(1))
    translated_digest = hashlib.sha256("\0".join(translated_tokens).encode()).hexdigest()
    theorem_digest = hashlib.sha256("\0".join(theorem_tokens).encode()).hexdigest()

    print(
        "CONSTRUCTOR_TOKEN_COMPARE "
        f"translated_count={len(translated_tokens)} theorem_count={len(theorem_tokens)} "
        f"translated_digest={translated_digest} theorem_digest={theorem_digest} "
        f"equal={translated_tokens == theorem_tokens}"
    )
    if translated_tokens != theorem_tokens:
        for index, (left, right) in enumerate(
            zip(translated_tokens, theorem_tokens, strict=False)
        ):
            if left != right:
                print(f"FIRST_DIFFERENCE index={index} translated={left!r} theorem={right!r}")
                break
        raise SystemExit(1)

    claim_count = len(re.findall(r"(?m)^\s*claim(?:\s|$)", spec))
    entry_count = spec.count("<program> solutionModule() </program>")
    precondition_count = len(
        re.findall(r'(?m)^\s*requires\s+(?!")', spec)
    )
    print(
        f"SPEC_COUNTS claims={claim_count} full_program_entries={entry_count} "
        f"claim_precondition_clauses={precondition_count}"
    )
    if claim_count != 17 or entry_count != 2:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
