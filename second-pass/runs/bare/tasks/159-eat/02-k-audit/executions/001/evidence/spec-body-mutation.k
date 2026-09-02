requires "/tmp/audit-work/159-eat/candidate-src/verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim <mpy>
          <k>
            run(
              Module(
                FuncDef("eat", Params("number", "need", "remaining"),
                  If(Compare(Name("need"), CmpOp("<=", Name("remaining"))),
                    Return(ListExpr(
                      BinOp("+",
                        BinOp("+", Name("number"), Name("need")),
                        Int(1)),
                      BinOp("-", Name("remaining"), Name("need"))
                    )),
                    .Stmts
                  )
                  Return(ListExpr(
                    BinOp("+", Name("number"), Name("remaining")),
                    Int(0)
                  ))
                )
              ),
              args(5, 6, 10)
            )
            => result(11, 4)
          </k>
        </mpy>
endmodule
