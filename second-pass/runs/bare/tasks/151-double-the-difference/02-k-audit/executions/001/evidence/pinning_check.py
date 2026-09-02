#!/usr/bin/env python3
"""Mechanical constructor-level comparison of solution.mpy and proof abbreviations."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re


WORK = Path("/tmp/audit-work/candidate-src")


def compact(term: str) -> str:
    term = re.sub(r"//[^\n]*", "", term)
    term = term.replace(".Stmts", "")
    return re.sub(r"\s+", "", term)


def main() -> int:
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    submitted = (WORK / "solution.mpy").read_text(encoding="utf-8")

    loop_match = re.search(
        r"\brule\s+loopBody\s*=>\s*(.*?)\n\s*syntax\s+Module\b",
        verification,
        flags=re.DOTALL,
    )
    program_match = re.search(
        r"\brule\s+solutionProgram\s*=>\s*(.*?)\n\s*//\s*Mathematical",
        verification,
        flags=re.DOTALL,
    )
    if loop_match is None or program_match is None:
        raise AssertionError("could not extract proof abbreviations")

    loop_rhs = loop_match.group(1).strip()
    program_rhs = program_match.group(1).strip()
    occurrences = len(re.findall(r"\bloopBody\b", program_rhs))
    if occurrences != 1:
        raise AssertionError(
            f"expected one loopBody occurrence in solutionProgram, saw {occurrences}"
        )
    expanded = re.sub(r"\bloopBody\b", loop_rhs, program_rhs)

    submitted_compact = compact(submitted)
    expanded_compact = compact(expanded)
    submitted_hash = hashlib.sha256(submitted_compact.encode()).hexdigest()
    expanded_hash = hashlib.sha256(expanded_compact.encode()).hexdigest()

    print(f"LOOPBODY_OCCURRENCES_IN_SOLUTION_PROGRAM={occurrences}")
    print(f"SUBMITTED_NORMALIZED_LENGTH={len(submitted_compact)}")
    print(f"EXPANDED_NORMALIZED_LENGTH={len(expanded_compact)}")
    print(f"SUBMITTED_NORMALIZED_SHA256={submitted_hash}")
    print(f"EXPANDED_NORMALIZED_SHA256={expanded_hash}")
    print(f"CONSTRUCTOR_LEVEL_IDENTICAL={submitted_compact == expanded_compact}")
    if submitted_compact != expanded_compact:
        print(f"SUBMITTED={submitted_compact}")
        print(f"EXPANDED={expanded_compact}")
        raise AssertionError("proof program differs from submitted solution.mpy")
    print("PINNING_CHECK=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
