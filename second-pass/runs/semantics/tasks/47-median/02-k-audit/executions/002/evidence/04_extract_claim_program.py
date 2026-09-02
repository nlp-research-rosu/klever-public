#!/usr/bin/env python3
"""Extract a #loadAll argument from spec.k using balanced delimiters."""

from __future__ import annotations

import sys
from pathlib import Path


def extract_calls(text: str, marker: str) -> list[str]:
    calls: list[str] = []
    offset = 0
    while True:
        start = text.find(marker, offset)
        if start < 0:
            return calls
        cursor = start + len(marker)
        depth = 1
        in_string = False
        escaped = False
        while cursor < len(text) and depth:
            char = text[cursor]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
            elif char == '"':
                in_string = True
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            cursor += 1
        if depth:
            raise ValueError("unbalanced #loadAll call")
        calls.append(text[start + len(marker) : cursor - 1])
        offset = cursor


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} INDEX", file=sys.stderr)
        return 2
    index = int(sys.argv[1])
    text = Path("/tmp/audit-work/reconstruction/spec.k").read_text()
    calls = extract_calls(text, "#loadAll(")
    print(f"EXTRACTED_CALLS={len(calls)}", file=sys.stderr)
    if len(calls) != 2:
        print("expected exactly two entry programs", file=sys.stderr)
        return 3
    if index < 0 or index >= len(calls):
        print("index out of range", file=sys.stderr)
        return 4
    # `.Stmts` is K's internal list unit used inside spec.k.  The external
    # MPY parser denotes the same empty list by an empty argument position.
    normalized = calls[index].replace(".Stmts", "")
    print(normalized)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
