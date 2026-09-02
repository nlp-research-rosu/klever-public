#!/usr/bin/env python3
"""Extract the Module(...) term executed by the entry claim."""

from __future__ import annotations

import sys
from pathlib import Path


def balanced_term(text: str, start: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    for position in range(start, len(text)):
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
                return text[start : position + 1]
    raise ValueError("unbalanced Module term")


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} SPEC OUTPUT", file=sys.stderr)
        return 64
    source = Path(sys.argv[1]).read_text()
    markers = [pos for pos in range(len(source)) if source.startswith("Module(", pos)]
    if len(markers) != 1:
        raise ValueError(f"expected exactly one Module term, found {len(markers)}")
    term = balanced_term(source, markers[0])
    Path(sys.argv[2]).write_text(term + "\n")
    print(f"extracted_chars={len(term)} module_terms={len(markers)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
