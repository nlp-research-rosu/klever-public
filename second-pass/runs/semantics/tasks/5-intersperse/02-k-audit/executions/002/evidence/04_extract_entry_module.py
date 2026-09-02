#!/usr/bin/env python3
"""Extract the Module(...) argument executed by the entry claim's #loadAll."""

from __future__ import annotations

import sys
from pathlib import Path


text = Path(sys.argv[1]).read_text(encoding="utf-8")
marker = "#loadAll(Module("
marker_at = text.index(marker)
start = marker_at + len("#loadAll(")

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
            # The K claim parser accepts named empty-list units. The standalone
            # MPY parser spells the same units by omitting list elements.
            term = text[start : index + 1]
            term = term.replace(".Exprs", "").replace(".Stmts", "")
            sys.stdout.write(term + "\n")
            raise SystemExit(0)

raise RuntimeError("unterminated Module term")
