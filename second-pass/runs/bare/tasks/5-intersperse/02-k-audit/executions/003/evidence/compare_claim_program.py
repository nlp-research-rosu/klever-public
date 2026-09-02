#!/usr/bin/env python3
"""Mechanically compare the regenerated Module term with the claim's Module term."""

from __future__ import annotations

import re
import sys
from pathlib import Path


TOKEN = re.compile(
    r'"(?:[^"\\]|\\.)*"|-?[0-9]+|[A-Za-z_.][A-Za-z0-9_.-]*|~>|=>|[(),:\[\]]'
)


def tokens(path: str) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    # Remove line comments before tokenizing K; solution.mpy contains none.
    text = re.sub(r"//.*", "", text)
    return TOKEN.findall(text)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SOLUTION_MPY SPEC_K", file=sys.stderr)
        return 64
    program = tokens(sys.argv[1])
    spec = tokens(sys.argv[2])
    raw_positions = [
        index
        for index in range(len(spec) - len(program) + 1)
        if spec[index : index + len(program)] == program
    ]
    # py2mpy renders an empty List{Stmt,""} as whitespace, while hand-written K
    # may spell the same list unit explicitly as .Stmts.
    normalized_spec = [token for token in spec if token != ".Stmts"]
    normalized_positions = [
        index
        for index in range(len(normalized_spec) - len(program) + 1)
        if normalized_spec[index : index + len(program)] == program
    ]
    print(f"PROGRAM_TOKENS {len(program)}")
    print(f"SPEC_TOKENS {len(spec)}")
    print(f"RAW_CONTIGUOUS_MATCHES {raw_positions}")
    print(f"AFTER_EMPTY_STMTS_UNIT_NORMALIZATION {normalized_positions}")
    entry_binding_present = '"intersperse"' in spec
    print(f"ENTRY_BINDING_PRESENT {entry_binding_present}")
    print(f"SYMBOLIC_ARGUMENTS_PRESENT {all(item in spec for item in ('IS', 'D', 'KONT'))}")
    return 0 if len(normalized_positions) == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
