requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  claim <k> solutionProgram =>
    Module(
      FuncDef("compare", Params("game", "guess"),
        If(Compare(Name("game"), CmpOp("==", ListExpr(.Exprs))),
          Return(ListExpr(.Exprs)),
          .Stmts)
        Assign(
          Name("difference"),
          BinOp(
            "-",
            Subscript(Name("game"), Int(0)),
            Subscript(Name("guess"), Int(0))))
        If(Compare(Name("difference"), CmpOp("<", Int(0))),
          Assign(Name("difference"), UnaryOp("-", Name("difference"))),
          .Stmts)
        Return(
          BinOp(
            "+",
            ListExpr(Name("difference")),
            Call(
              Name("compare"),
              Subscript(Name("game"), Slice(Int(1), NoBound, NoBound)),
              Subscript(Name("guess"), Slice(Int(1), NoBound, NoBound)))))))
        </k>
endmodule
