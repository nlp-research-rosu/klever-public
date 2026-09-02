#!/usr/bin/env python3
"""Wrap the trusted translation of the body-mutated program in a K macro."""

from pathlib import Path
import re


term = Path("solution-body-mutant.mpy").read_text(encoding="utf-8").rstrip()
term = re.sub(r",\n([ \t]*)\)", r",\n\1.Stmts)", term)

print('requires "semantic.k"')
print()
print("module SOLUTION-PROGRAM-BODY-MUTANT")
print("  imports MPY-SYNTAX")
print("  syntax Program ::= mutatedSolutionProgram() [macro]")
print("  rule mutatedSolutionProgram() =>")
for line in term.splitlines():
    print(f"    {line}")
print("endmodule")
