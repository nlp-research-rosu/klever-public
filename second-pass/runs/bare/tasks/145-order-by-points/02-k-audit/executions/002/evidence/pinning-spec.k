requires "verification.k"

module PINNING-SPEC
  imports VERIFICATION

  // The RHS is the trusted-regenerated solution.mpy constructor tree.
  claim [label(pins-regenerated-term)]:
        <py>
          <k>
            solutionProgram
            =>
            Module(
              FuncDef(
                "order_by_points", Params("nums"),
                Return(
                  Call(
                    Name("sorted"),
                    Name("nums"),
                    KwArg(
                      "key",
                      Lambda(
                        Params("n"),
                        CellVars(.Ids),
                        FreeVars(.Ids),
                        BinOp(
                          "-",
                          Call(
                            Name("sum"),
                            Call(
                              Name("map"),
                              Name("int"),
                              Call(
                                Name("str"),
                                Call(Name("abs"), Name("n"))))),
                          IfExp(
                            Compare(Name("n"), CmpOp("<", Int(0))),
                            BinOp(
                              "*",
                              Int(2),
                              Call(
                                Name("int"),
                                Subscript(
                                  Call(
                                    Name("str"),
                                    Call(Name("abs"), Name("n"))),
                                  Int(0)))),
                            Int(0)))))))))
          </k>
          <program> solutionProgram </program>
          <input> ListExpr(.Exprs) </input>
          <output> NoValue </output>
        </py>
endmodule
