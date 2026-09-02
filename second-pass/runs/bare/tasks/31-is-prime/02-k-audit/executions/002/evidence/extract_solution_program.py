#!/usr/bin/env python3
"""Extract the literal RHS of rule solutionProgram() from verification.k."""

from __future__ import annotations

import sys
from pathlib import Path
import re


def extract(source: str) -> str:
    marker = "rule solutionProgram() =>"
    marker_at = source.find(marker)
    if marker_at < 0:
        raise ValueError(f"missing {marker!r}")
    start = source.find("Module(", marker_at + len(marker))
    if start < 0:
        raise ValueError("missing Module( after solutionProgram rule")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
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
                return source[start : index + 1] + "\n"
    raise ValueError("unbalanced solutionProgram RHS")


def main() -> int:
    if len(sys.argv) != 3:
        raise SystemExit("usage: extract_solution_program.py verification.k output.mpy")
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    rhs = extract(source)
    # K rules spell the empty generated List{Stmt,""} as `.Stmts`; the
    # external program parser spells that same collection unit as an omitted
    # block. This is the sole source-to-program normalization performed here.
    rhs = re.sub(r"(?<![A-Za-z0-9_])\.Stmts(?![A-Za-z0-9_])", "", rhs)
    Path(sys.argv[2]).write_text(rhs, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
