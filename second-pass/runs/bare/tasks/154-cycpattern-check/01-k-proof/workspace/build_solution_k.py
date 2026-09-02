#!/usr/bin/env python3
"""Wrap the generated solution.mpy term in a K module for verification."""

from pathlib import Path
import re


term = Path("solution.mpy").read_text(encoding="utf-8").rstrip()
# py2mpy renders an empty statement-list argument as blank space after a
# comma.  A standalone .mpy parser accepts it, while a rule RHS requires the
# explicit list unit.  Both parse to the same .Stmts constructor.
term = re.sub(r",\n([ \t]*)\)", r",\n\1.Stmts)", term)

print('requires "semantic.k"')
print()
print("module SOLUTION-PROGRAM")
print("  imports MPY-SYNTAX")
print("  syntax Program ::= solutionProgram() [macro]")
print("  rule solutionProgram() =>")
for line in term.splitlines():
    print(f"    {line}")
print("endmodule")
