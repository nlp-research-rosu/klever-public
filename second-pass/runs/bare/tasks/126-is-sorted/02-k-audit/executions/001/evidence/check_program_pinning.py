#!/usr/bin/env python3
"""Check that the entry claim embeds the exact submitted Module constructor."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
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
                return text[start : index + 1]
    raise ValueError("unbalanced constructor term")


def remove_unquoted_whitespace(text: str) -> str:
    output: list[str] = []
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} solution.mpy spec.k", file=sys.stderr)
        return 2
    program_text = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    spec_text = Path(sys.argv[2]).read_text(encoding="utf-8")
    spec_start = spec_text.index("Module(", spec_text.index("Run("))
    embedded = balanced_term(spec_text, spec_start)
    program_start = program_text.index("Module(")
    submitted = balanced_term(program_text, program_start)
    if remove_unquoted_whitespace(program_text) != remove_unquoted_whitespace(submitted):
        print("ERROR=submitted MPY has material text outside Module term")
        return 1
    normalized_submitted = remove_unquoted_whitespace(submitted)
    normalized_embedded = remove_unquoted_whitespace(embedded)
    print(f"SUBMITTED_NORMALIZED_CHARS={len(normalized_submitted)}")
    print(f"EMBEDDED_NORMALIZED_CHARS={len(normalized_embedded)}")
    print(
        "SUBMITTED_NORMALIZED_SHA256="
        + hashlib.sha256(normalized_submitted.encode()).hexdigest()
    )
    print(
        "EMBEDDED_NORMALIZED_SHA256="
        + hashlib.sha256(normalized_embedded.encode()).hexdigest()
    )
    print(f"EXACT_CONSTRUCTOR_MATCH={normalized_submitted == normalized_embedded}")
    return 0 if normalized_submitted == normalized_embedded else 1


if __name__ == "__main__":
    raise SystemExit(main())
