requires "verification.k"

module BODY-IDENTITY
  imports VERIFICATION

  // The RHS is the exact trusted-translator output in solution.mpy.  This
  // mechanical claim closes only if the proof aliases expand to that same
  // function binding, parameter list, and constructor-level body.
  claim [submitted-body]:
    Module(
      FuncDef("prime_length", Params("string"), primeBody))
    =>
    Module(
      FuncDef("prime_length", Params(("string", .ParamNames)),
        Assign(Name("n"), Call(Name("len"), (Name("string"), .Exprs)))
        If(Compare(Name("n"), CmpOp("<", Int(2))),
          Return(Bool(false)) .Stmts,
          .Stmts)
        Assign(Name("divisor"), Int(2))
        While(Compare(Name("divisor"), CmpOp("<", Name("n"))),
          If(Compare(
            BinOp("%", Name("n"), Name("divisor")),
            CmpOp("==", Int(0))),
            Return(Bool(false)) .Stmts,
            .Stmts)
          AugAssign(Name("divisor"), "+", Int(1))
          .Stmts)
        Return(Bool(true))
        .Stmts))
endmodule
