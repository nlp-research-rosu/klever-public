requires "verification.k"

module PROGRAM-PIN
  imports VERIFICATION

  claim
    <k> boot(solutionProgram) =>
      boot(
        Module(
          FuncDef("prod_signs", Params("arr"),
            If(Compare(Name("arr"), CmpOp("==", ListExpr(.Exprs))),
              Return(NoneVal),
              .Stmts)
            Assign(Name("total"), Int(0))
            Assign(Name("sign"), Int(1))
            Assign(Name("x"), Int(0))
            For(Name("x"), Name("arr"),
              If(Compare(Name("x"), CmpOp("<", Int(0))),
                Assign(Name("total"), BinOp("-", Name("total"), Name("x")))
                Assign(Name("sign"), UnaryOp("-", Name("sign"))),
                Assign(Name("total"), BinOp("+", Name("total"), Name("x")))
                If(Compare(Name("x"), CmpOp("==", Int(0))),
                  Assign(Name("sign"), Int(0)),
                  .Stmts)))
            Return(BinOp("*", Name("total"), Name("sign"))))))
    </k>
endmodule
