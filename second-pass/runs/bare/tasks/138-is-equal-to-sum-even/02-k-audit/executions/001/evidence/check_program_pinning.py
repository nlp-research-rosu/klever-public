#!/usr/bin/env python3
"""Compare every program-bearing submitted claim with submitted solution.mpy."""

from __future__ import annotations

import re
from pathlib import Path


PROGRAM_PATH = Path("/tmp/audit-work/review-138/candidate-src/solution.mpy")
SPEC_PATH = Path("/tmp/audit-work/review-138/candidate-src/spec.k")


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def extract_balanced_modules(text: str) -> list[str]:
    modules: list[str] = []
    start = 0
    while True:
        start = text.find("Module(", start)
        if start < 0:
            return modules
        depth = 0
        end = start
        while end < len(text):
            char = text[end]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    modules.append(text[start : end + 1])
                    start = end + 1
                    break
            end += 1
        else:
            raise RuntimeError(f"unbalanced Module term at offset {start}")


def main() -> None:
    submitted_program = PROGRAM_PATH.read_text(encoding="utf-8")
    submitted_spec = SPEC_PATH.read_text(encoding="utf-8")
    embedded_programs = extract_balanced_modules(submitted_spec)

    print(f"PROGRAM_PATH={PROGRAM_PATH}")
    print(f"SPEC_PATH={SPEC_PATH}")
    print(f"PROGRAM_NORMALIZED={normalize(submitted_program)}")
    print(f"PROGRAM_BEARING_CLAIM_COUNT={len(embedded_programs)}")
    comparisons = []
    for index, program in enumerate(embedded_programs, 1):
        identical = normalize(program) == normalize(submitted_program)
        comparisons.append(identical)
        print(f"CLAIM_PROGRAM_{index}_IDENTICAL={identical}")
        print(f"CLAIM_PROGRAM_{index}_NORMALIZED={normalize(program)}")

    if len(embedded_programs) != 5 or not all(comparisons):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
