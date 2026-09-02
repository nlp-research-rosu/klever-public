#!/usr/bin/env python3
"""Generate a K claim comparing solutionProgram with regenerated solution.mpy."""

from pathlib import Path


program = Path("/tmp/audit-work/candidate/solution.regenerated.mpy").read_text().strip()
# The standalone program parser accepts an omitted empty List{Stmt,""} item as
# `,)`; inside a claim K requires the canonical empty-list token.
empty_else = ',\n      )\n    Return('
assert empty_else in program
program = program.replace(empty_else, ',\n      .Stmts)\n    Return(', 1)
print('requires "verification.k"')
print()
print("module IDENTITY-SPEC")
print("  imports VERIFICATION")
print()
print("  claim solutionProgram =>")
for line in program.splitlines():
    print(f"    {line}")
print("endmodule")
