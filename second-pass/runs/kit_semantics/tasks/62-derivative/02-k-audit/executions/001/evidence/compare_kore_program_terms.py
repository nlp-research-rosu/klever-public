#!/usr/bin/env python3
"""Compare the parsed submitted Module term with the Module inside the K claim."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


PREFIX = "LblModule'LParUndsRParUnds'MPY-SYNTAX'Unds'Module'Unds'Stmts{}"


def extract(text: str) -> list[str]:
    terms: list[str] = []
    offset = 0
    while True:
        start = text.find(PREFIX, offset)
        if start < 0:
            return terms
        open_paren = start + len(PREFIX)
        if open_paren >= len(text) or text[open_paren] != "(":
            raise ValueError("Module label not followed by an application")
        depth = 0
        in_string = False
        escaped = False
        for position in range(open_paren, len(text)):
            char = text[position]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    terms.append(text[start : position + 1])
                    offset = position + 1
                    break
        else:
            raise ValueError("unbalanced KORE Module application")


def normalize(text: str) -> str:
    # KORE pretty-print whitespace is insignificant outside quoted strings.
    pieces = re.split(r'("(?:\\.|[^"\\])*")', text)
    return "".join(
        piece if index % 2 else re.sub(r"\s+", "", piece)
        for index, piece in enumerate(pieces)
    )


def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} TRANSLATED_KORE SPEC_KORE", file=sys.stderr)
        return 64
    translated = extract(Path(sys.argv[1]).read_text())
    claimed = extract(Path(sys.argv[2]).read_text())
    print(f"translated_module_terms={len(translated)} claimed_module_terms={len(claimed)}")
    if len(translated) != 1 or len(claimed) != 1:
        return 1
    left = normalize(translated[0])
    right = normalize(claimed[0])
    print(f"translated_term_sha256={digest(left)}")
    print(f"claimed_term_sha256={digest(right)}")
    print(f"constructor_identity={left == right}")
    return 0 if left == right else 1


if __name__ == "__main__":
    sys.exit(main())
