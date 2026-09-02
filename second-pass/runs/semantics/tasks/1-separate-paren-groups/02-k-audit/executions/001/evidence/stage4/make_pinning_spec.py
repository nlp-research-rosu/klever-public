#!/usr/bin/env python3
"""Generate a K claim that loads the submitted solution.mpy as a Module."""

from __future__ import annotations

import hashlib
from pathlib import Path


program_bytes = Path("/candidate/solution.mpy").read_bytes()
expected_digest = "a64520e2af51bed55082d485b79af9013718e530b6eb464db44cd90ff0a39144"
if hashlib.sha256(program_bytes).hexdigest() != expected_digest:
    raise SystemExit("submitted solution.mpy changed after provenance check")

# The external program parser accepts omitted empty-list terminators such as
# ListExpr().  K's inner claim parser requires those terminators explicitly.
# This is the normalized spelling of the byte-checked submitted Module AST.
normalized_program = '''Module(
  ImportFrom("typing", ("List", .ParamNames))
  FuncDef("separate_paren_groups", Params(("paren_string", .ParamNames)),
    Assign(Name("groups"), ListExpr(.Exprs))
    Assign(Name("current"), Str(""))
    Assign(Name("depth"), Int(0))
    For(Name("character"), Name("paren_string"),
      If(Compare(Name("character"), CmpOp("==", Str(" "))),
        Continue .Stmts,
        .Stmts)
      AugAssign(Name("current"), "+", Name("character"))
      If(Compare(Name("character"), CmpOp("==", Str("("))),
        AugAssign(Name("depth"), "+", Int(1)) .Stmts,
        AugAssign(Name("depth"), "-", Int(1)) .Stmts)
      If(Compare(Name("depth"), CmpOp("==", Int(0))),
        Expr(Call(Attribute(Name("groups"), "append"),
                  (Name("current"), .Exprs)))
        Assign(Name("current"), Str(""))
        .Stmts,
        .Stmts)
      .Stmts)
    Return(Name("groups"))
    .Stmts)
  .Stmts)'''

print('requires "verification.k"')
print()
print("module PINNING-SPEC")
print("  imports VERIFICATION")
print()
print("  claim [submitted-module-loads-exact-closure]:")
print("    <k>")
print("      #loadAll(")
for line in normalized_program.splitlines():
    print("        " + line)
print("      )")
print("      => .K")
print("    </k>")
print("    <env> 0 </env>")
print("    <scopes>")
print("      ( -1 |-> builtinsScope")
print("        0 |-> scope(.Map, parent(-1)) )")
print("      =>")
print("      ( -1 |-> builtinsScope")
print('        0 |-> scope("separate_paren_groups" |-> solutionClosure,')
print("                     parent(-1)) )")
print("    </scopes>")
print()
print("endmodule")
