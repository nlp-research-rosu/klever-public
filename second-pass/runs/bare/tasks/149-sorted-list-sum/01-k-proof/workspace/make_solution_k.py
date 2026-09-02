#!/usr/bin/env python3
"""Generate a K constant from the exact py2mpy output used by the proof."""

import pathlib
import re


term = pathlib.Path("solution.mpy").read_text(encoding="utf-8").strip()

# Empty constructor lists are accepted by the runtime parser (`ListExpr()` and
# a blank final Stmts argument), while K definition source spells their units.
term = term.replace("ListExpr()", "ListExpr(.Exprs)")
term = term.replace("CellVars()", "CellVars(.Strings)")
term = term.replace("FreeVars()", "FreeVars(.Strings)")
term = re.sub(r",\n(?P<indent>[ ]*)\)", r",\n\g<indent>.Stmts)", term)
term = "\n".join("    " + line for line in term.splitlines())

print('requires "semantic.k"')
print()
print("module SOLUTION-PROGRAM")
print("  imports MPY-SEMANTIC")
print('  syntax Program ::= "solutionProgram" [function]')
print("  rule solutionProgram =>")
print(term)
print("endmodule")
