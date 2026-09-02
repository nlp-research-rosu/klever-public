#!/usr/bin/env python3
"""Check the generated semantics' one-character whitespace table exhaustively."""

from __future__ import annotations

import ast
import re
from pathlib import Path


SEMANTICS = Path("/tmp/audit-work/fresh/candidate/semantic.k")


def codepoints(values: set[str]) -> list[str]:
    return [f"U+{ord(value):04X}" for value in sorted(values, key=ord)]


def main() -> int:
    source = SEMANTICS.read_text(encoding="utf-8")
    block_match = re.search(
        r"rule\s+isWhitespace\(C\).*?findString\(\s*"
        r'("(?:\\.|[^"\\])*")\s*,\s*C\s*,\s*0\s*\)',
        source,
        re.DOTALL,
    )
    if block_match is None:
        print("ERROR: could not locate isWhitespace table")
        return 2
    literal = ast.literal_eval(block_match.group(1))
    actual = set(literal)
    expected = {
        chr(codepoint)
        for codepoint in range(0x110000)
        if chr(codepoint).isspace()
    }
    print("SEMANTICS:", SEMANTICS)
    print("TABLE_LENGTH:", len(literal))
    print("TABLE_UNIQUE_COUNT:", len(actual))
    print("PYTHON_ISSPACE_COUNT:", len(expected))
    print("TABLE_CODEPOINTS:", " ".join(codepoints(actual)))
    print("PYTHON_CODEPOINTS:", " ".join(codepoints(expected)))
    print("MISSING:", " ".join(codepoints(expected - actual)))
    print("ADDITIONAL:", " ".join(codepoints(actual - expected)))
    print("DUPLICATES:", len(literal) - len(actual))
    return 0 if actual == expected and len(literal) == len(actual) else 1


if __name__ == "__main__":
    raise SystemExit(main())
