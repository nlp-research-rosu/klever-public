requires "verification.k"

module PINNING
  imports VERIFICATION

  // Reviewer-authored constructor-level identity check: the proof shorthand
  // must reduce to the complete submitted solution.mpy module term.
  claim
    <k> solutionModule =>
    Module(
      ImportFrom("typing", "List")
      FuncDef("parse_nested_parens", Params("paren_string"),
        Assign(Name("depths"), ListExpr(.Exprs))
        Assign(Name("depth"), Int(0))
        Assign(Name("deepest"), Int(0))
        Assign(Name("char"), Str(""))
        For(Name("char"), Name("paren_string"),
          If(Compare(Name("char"), CmpOp("==", Str("("))),
            AugAssign(Name("depth"), "+", Int(1))
            If(Compare(Name("depth"), CmpOp(">", Name("deepest"))),
              Assign(Name("deepest"), Name("depth")),
              .Stmts),
            If(Compare(Name("char"), CmpOp("==", Str(")"))),
              AugAssign(Name("depth"), "-", Int(1)),
              If(Compare(Name("deepest"), CmpOp(">", Int(0))),
                Expr(
                  Call(Attribute(Name("depths"), "append"), Name("deepest")))
                Assign(Name("deepest"), Int(0)),
                .Stmts))))
        If(Compare(Name("deepest"), CmpOp(">", Int(0))),
          Expr(Call(Attribute(Name("depths"), "append"), Name("deepest"))),
          .Stmts)
        Return(Name("depths")))) </k>
endmodule
