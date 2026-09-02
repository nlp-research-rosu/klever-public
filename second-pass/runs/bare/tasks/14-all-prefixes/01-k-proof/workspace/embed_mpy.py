#!/usr/bin/env python3
"""Embed the freshly translated program as the K proof target."""

from pathlib import Path


term = Path("solution.mpy").read_text(encoding="utf-8").strip()
indented = "\n".join("    " + line for line in term.splitlines())
print('module SOLUTION-PROGRAM')
print('  imports MPY')
print('  syntax Program ::= "solutionProgram" [function]')
print('  rule solutionProgram =>')
print(indented)
print('endmodule')
