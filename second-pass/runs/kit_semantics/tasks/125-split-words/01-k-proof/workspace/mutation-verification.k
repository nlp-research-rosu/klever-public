requires "verification.k"

module MUTATION-VERIFICATION
  imports VERIFICATION

  // Material body mutation: preserve delimiter handling, but replace the
  // no-delimiter count computation by the constant zero.
  syntax Stmts ::= "mutatedSplitWordsBody" [function, total]
  rule mutatedSplitWordsBody =>
    Assign(Name("parts"), Call(Attribute(Name("txt"), "split"), .Exprs))
    If(
      BoolOp(
        "and",
        Name("txt"),
        Compare(Name("parts"), CmpOp("!=", ListExpr(Name("txt"), .Exprs))),
        .Exprs
      ),
      Return(Name("parts")) .Stmts,
      .Stmts
    )
    If(
      Compare(Str(","), CmpOp("in", Name("txt"))),
      Return(Call(Attribute(Name("txt"), "split"), Str(","), .Exprs)) .Stmts,
      .Stmts
    )
    Return(Int(0)) .Stmts
endmodule
