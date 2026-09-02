#!/usr/bin/env python3
"""Mechanical constructor-token comparison of solution.mpy and claim aliases."""

from __future__ import annotations

import re
import sys
from pathlib import Path


WORK = Path("/tmp/audit-work/49-modp")
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|=>|[A-Za-z_#][A-Za-z0-9_#-]*|-?[0-9]+|[(),.]')


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text)


def between(text: str, start: str, end: str) -> str:
    if text.count(start) != 1:
        raise AssertionError(f"expected exactly one marker {start!r}")
    tail = text.split(start, 1)[1]
    if tail.count(end) < 1:
        raise AssertionError(f"missing end marker {end!r}")
    return tail.split(end, 1)[0]


def main() -> int:
    verification = (WORK / "verification.k").read_text(encoding="utf-8")
    generated = (WORK / "regenerated-solution.mpy").read_text(encoding="utf-8")

    body_rhs = between(
        verification,
        "rule modpBody\n    =>",
        "\n\n  syntax Module",
    )
    program_rhs = between(
        verification,
        "rule modpProgram\n    =>",
        "\n\n  // Mathematical contract",
    )

    body_tokens = tokens(body_rhs)
    program_tokens = tokens(program_rhs)
    occurrences = program_tokens.count("modpBody")
    if occurrences != 1:
        raise AssertionError(f"expected one modpBody use, found {occurrences}")
    index = program_tokens.index("modpBody")
    expanded = program_tokens[:index] + body_tokens + program_tokens[index + 1:]
    generated_tokens = tokens(generated)

    print(f"BODY_ALIAS_TOKENS {len(body_tokens)}")
    print(f"PROGRAM_ALIAS_TOKENS_PRE_EXPANSION {len(program_tokens)}")
    print(f"EXPANDED_PROGRAM_TOKENS {len(expanded)}")
    print(f"REGENERATED_SOLUTION_TOKENS {len(generated_tokens)}")
    print(f"CONSTRUCTOR_TOKEN_IDENTITY {expanded == generated_tokens}")
    if expanded != generated_tokens:
        for offset, pair in enumerate(zip(expanded, generated_tokens)):
            if pair[0] != pair[1]:
                print(f"FIRST_DIFFERENCE index={offset} alias={pair[0]!r} "
                      f"generated={pair[1]!r}")
                break
        print("ALIAS_EXPANDED", expanded)
        print("GENERATED", generated_tokens)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
