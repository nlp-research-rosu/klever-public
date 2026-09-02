requires "/tmp/audit-work/verification.k"

module REVIEWER-BODY-PINNING-SPEC
  imports PAIRS-VERIFICATION

  // The RHS is copied constructor-for-constructor from the trusted regeneration
  // of solution.mpy. This claim checks the proof-local alias that every entry
  // theorem actually invokes.
  claim [pairs-body-is-submitted-body]:
    <k>
      pairsBody
      =>
      Assign(Name("seen"), ListExpr(.Exprs))
      Assign(Name("value"), Int(0))
      For(Name("value"), Name("l"),
        If(Compare(UnaryOp("-", Name("value")), CmpOp("in", Name("seen"))),
          Return(Bool(true)),
          .Stmts)
        Expr(Call(Attribute(Name("seen"), "append"),
                  (Name("value"), .Exprs))))
      Return(Bool(false))
    </k>
endmodule
