requires "verification.k"

module EAT-PINNING-SPEC
  imports EAT-VERIFICATION

  claim <k> eatClosure
          => closureVal(("number", "need", "remaining"),
                 If(Compare(Name("need"), CmpOp("<=", Name("remaining"))), Return(ListExpr(BinOp("+", Name("number"), Name("need")), BinOp("-", Name("remaining"), Name("need")))), .Stmts) Return(ListExpr(BinOp("+", Name("number"), Name("remaining")), Int(0))),
                 0)
        </k>
endmodule
