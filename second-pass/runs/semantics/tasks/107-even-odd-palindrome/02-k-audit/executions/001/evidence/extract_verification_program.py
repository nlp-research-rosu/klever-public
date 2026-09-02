#!/usr/bin/env python3
"""Extract the proof's duplicated program AST for parser-level identity checking."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path


verification = Path("/tmp/audit-work/reconstruction/verification.k").read_text()

body_match = re.search(
    r"  rule solutionBody =>\n(?P<body>.*?)\n\n  syntax Module ::=",
    verification,
    flags=re.DOTALL,
)
if body_match is None:
    raise SystemExit("could not isolate solutionBody rule")
body = textwrap.dedent(body_match.group("body")).rstrip()
body_surface = body.replace(".Stmts", "")

module_match = re.search(
    r"  rule solutionModule =>\s*"
    r'Module\(\s*FuncDef\(\s*"even_odd_palindrome"\s*,\s*'
    r'Params\(\s*"n"\s*\)\s*,\s*solutionBody\s*\)\s*\)',
    verification,
    flags=re.DOTALL,
)
if module_match is None:
    raise SystemExit("solutionModule does not wrap solutionBody at the required binding")

expanded = (
    "Module(\n"
    '  FuncDef("even_odd_palindrome", Params("n"),\n'
    + textwrap.indent(body_surface, "    ")
    + "))\n"
)

Path("/audit-output/evidence/verification-expanded.mpy").write_text(expanded)
Path("/tmp/audit-work/reconstruction/verification-expanded.mpy").write_text(expanded)
print("solutionModule wrapper: exact function name, parameter, and solutionBody binding")
print("solutionBody source lines:", len(body.splitlines()))
print("internal empty .Stmts terms rendered as surface empty statement lists")
