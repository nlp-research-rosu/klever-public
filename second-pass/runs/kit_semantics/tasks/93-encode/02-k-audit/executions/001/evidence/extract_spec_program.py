#!/usr/bin/env python3
"""Extract the balanced Module(...) argument of SPEC's #loadAll call."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def balanced_argument(text: str, marker: str) -> str:
    marker_index = text.index(marker)
    start = marker_index + len(marker)
    depth = 1
    quote: str | None = None
    escaped = False
    for index in range(start, len(text)):
        character = text[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == quote:
                quote = None
            continue
        if character in {'"', "'"}:
            quote = character
        elif character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth == 0:
                return text[start:index].strip()
    raise ValueError(f"unbalanced argument after {marker!r}")


if len(sys.argv) not in {2, 3}:
    raise SystemExit(
        "usage: extract_spec_program.py SPEC.k [--normalize-program-units]"
    )

spec_text = Path(sys.argv[1]).read_text(encoding="utf-8")
program = balanced_argument(spec_text, "#loadAll(")
assert program.startswith("Module(")
assert program.endswith(")")
if len(sys.argv) == 3:
    assert sys.argv[2] == "--normalize-program-units"
    # In rule syntax `.Exprs` is the explicit unit of the variadic Exprs
    # production. In program syntax the same unit is represented by omission.
    program, replacement_count = re.subn(r",\s*\.Exprs\s*\)", ",\n)", program)
    assert replacement_count == 1
sys.stdout.write(program)
sys.stdout.write("\n")
