#!/usr/bin/env python3
"""Extract the balanced Program term from verification.k's solutionProgram rule."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("verification", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--surface",
        action="store_true",
        help="remove internal list-unit spellings so the concrete Program parser accepts it",
    )
    args = parser.parse_args()
    text = args.verification.read_text(encoding="utf-8")
    marker = "rule solutionProgram() =>"
    start = text.index(marker) + len(marker)
    start = text.index("Module(", start)
    depth = 0
    in_string = False
    escaped = False
    end = None
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
                end = index + 1
                break
    if end is None:
        raise RuntimeError("unterminated solutionProgram Module term")
    term = text[start:end]
    if args.surface:
        for internal_unit in (", .Strings", ", .Exprs", ", .CmpOps", " .Stmts"):
            term = term.replace(internal_unit, "")
        for internal_unit in (".Strings", ".Exprs", ".CmpOps", ".Stmts"):
            term = term.replace(internal_unit, "")
    args.output.write_text(term + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
