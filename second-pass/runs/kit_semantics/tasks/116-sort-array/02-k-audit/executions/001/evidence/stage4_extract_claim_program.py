#!/usr/bin/env python3
"""Extract the #loadAll argument from SPEC.sort-array for parser-level comparison."""

from __future__ import annotations

import re
from pathlib import Path


SPEC = Path("/tmp/audit-work/116-sort-array/spec.k")
OUTPUT = Path("/audit-output/evidence/stage4-claimed-program.mpy")
SURFACE_OUTPUT = Path(
    "/audit-output/evidence/stage4-claimed-program-surface-normalized.mpy"
)


def find_matching_paren(text: str, open_index: int) -> int:
    depth = 0
    in_string = False
    escaped = False
    for index in range(open_index, len(text)):
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
                return index
    raise ValueError("unbalanced #loadAll argument")


def main() -> int:
    source = SPEC.read_text(encoding="utf-8")
    claim_start = source.index("claim [sort-array]:")
    load_start = source.index("#loadAll(", claim_start)
    open_index = load_start + len("#loadAll")
    close_index = find_matching_paren(source, open_index)
    argument = source[open_index + 1 : close_index].strip() + "\n"
    if not argument.startswith("Module("):
        raise ValueError("sort-array #loadAll argument is not a Module term")
    OUTPUT.write_text(argument, encoding="utf-8")
    surface = argument
    replacements = (
        (r",\s*\.ParamNames", ""),
        (r"\.ParamNames", ""),
        (r",\s*\.Exprs", ""),
        (r"\.Exprs", ""),
        (r"\.Stmts", ""),
    )
    for pattern, replacement in replacements:
        surface, count = re.subn(pattern, replacement, surface)
        print(
            f"NORMALIZATION pattern={pattern!r} replacement={replacement!r} "
            f"count={count}"
        )
    SURFACE_OUTPUT.write_text(surface, encoding="utf-8")
    print(f"SPEC={SPEC}")
    print(f"CLAIM_OFFSET={claim_start}")
    print(f"LOAD_OFFSET={load_start}")
    print(f"ARGUMENT_BYTES={len(argument.encode('utf-8'))}")
    print(f"OUTPUT={OUTPUT}")
    print(f"SURFACE_OUTPUT={SURFACE_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
