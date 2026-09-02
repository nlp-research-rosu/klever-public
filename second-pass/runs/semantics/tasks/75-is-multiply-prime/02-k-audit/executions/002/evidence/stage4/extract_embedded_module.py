#!/usr/bin/env python3
"""Extract the exact Module(...) argument passed to #loadAll in verification.k."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument(
    "source",
    nargs="?",
    default="/tmp/audit-work/75-is-multiply-prime/verification.k",
)
parser.add_argument(
    "--external-program-syntax",
    action="store_true",
    help="render internal .Stmts list units as the external empty-list spelling",
)
arguments = parser.parse_args()
source_path = Path(arguments.source)
source = source_path.read_text()
anchor = "=> #loadAll("
anchor_index = source.index(anchor)
start = source.index("Module(", anchor_index + len(anchor))

depth = 0
in_string = False
escaped = False
end = None
for index in range(start, len(source)):
    character = source[index]
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
    raise RuntimeError("unterminated Module(...) term")

prefix = source[:start]
start_line = prefix.count("\n") + 1
end_line = source[:end].count("\n") + 1
print(f"EXTRACTED_SOURCE_LINES={start_line}-{end_line}", file=sys.stderr)
term = source[start:end]
if arguments.external_program_syntax:
    unit_count = term.count(".Stmts")
    if unit_count != 1:
        raise RuntimeError(f"expected one explicit .Stmts unit, found {unit_count}")
    term = term.replace(".Stmts", "")
    print("NORMALIZED_EXPLICIT_EMPTY_STMTS_UNIT=1", file=sys.stderr)
print(term)
