#!/usr/bin/env python3
"""Extract the entry claim's balanced Module(...) program term."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    spec = Path("/tmp/audit-work/rebuild/spec.k").read_text(encoding="utf-8")
    entry = spec.index("claim [entry-reaches-loop]:")
    start = spec.index("Module(", entry)
    depth = 0
    in_string = False
    escaped = False
    end = None
    for index, character in enumerate(spec[start:], start):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                end = index + 1
                break
    if end is None:
        raise SystemExit("unterminated Module term")
    # `.Stmts` is the explicit K empty-list token accepted in rule syntax.
    # Program syntax renders the same empty list with zero concrete tokens.
    normalized = spec[start:end].replace(".Stmts", "")
    sys.stdout.write(normalized + "\n")


if __name__ == "__main__":
    main()
