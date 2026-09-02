#!/usr/bin/env python3
"""Compare semantic.k's declared whitespace characters with this CPython."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


def cps(chars: set[str]) -> str:
    return " ".join(f"U+{ord(char):04X}" for char in sorted(chars))


def main() -> None:
    print("COMMAND: python3 /audit-output/evidence/whitespace_set_check.py")
    text = Path("/tmp/audit-work/candidate/semantic.k").read_text()
    start = text.index("rule isWhitespace")
    end = text.index("syntax List", start)
    region = text[start:end]
    match = re.search(
        r'findString\(\s*("(?:[^"\\]|\\.)*")', region, flags=re.DOTALL
    )
    assert match is not None
    literal = ast.literal_eval(match.group(1))
    declared = set(literal)
    cpython = {chr(codepoint) for codepoint in range(sys.maxunicode + 1)
               if chr(codepoint).isspace()}
    print(f"PYTHON_VERSION: {sys.version.split()[0]}")
    print(f"DECLARED_COUNT: {len(declared)}")
    print(f"CPYTHON_ISSPACE_COUNT: {len(cpython)}")
    print(f"MISSING: {cps(cpython - declared)}")
    print(f"ADDITIONAL: {cps(declared - cpython)}")
    print(f"EXACT_SET_MATCH: {declared == cpython}")
    raise SystemExit(0 if declared == cpython else 1)


if __name__ == "__main__":
    main()
