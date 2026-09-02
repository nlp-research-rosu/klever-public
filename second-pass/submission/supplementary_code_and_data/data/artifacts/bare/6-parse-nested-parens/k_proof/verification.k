requires "semantic.k"

module MPY-VERIFICATION
  imports MPY-SEMANTICS

  // A proof-facing name for the exact constructor tree in solution.mpy.  This
  // is a macro, not an implementation shortcut: after parsing, every claim
  // contains the same Module term that krun reads from solution.mpy.
  syntax Program ::= "solutionProgram" [function]
  rule solutionProgram =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("parse_nested_parens", Params("paren_string"),
        Assign(Name("result"), ListExpr(.Exprs))
        Assign(
          Name("groups"),
          Call(Attribute(Name("paren_string"), "split"), Str(" ")))
        For(Name("group"), Name("groups"),
          Assign(Name("depth"), Int(0))
          Assign(Name("maximum"), Int(0))
          For(Name("character"), Name("group"),
            If(Compare(Name("character"), CmpOp("==", Str("("))),
              AugAssign(Name("depth"), "+", Int(1))
              If(Compare(Name("depth"), CmpOp(">", Name("maximum"))),
                Assign(Name("maximum"), Name("depth")),
                .Stmts),
              AugAssign(Name("depth"), "-", Int(1))))
          Expr(Call(Attribute(Name("result"), "append"), Name("maximum"))))
        Return(Name("result"))))
endmodule
