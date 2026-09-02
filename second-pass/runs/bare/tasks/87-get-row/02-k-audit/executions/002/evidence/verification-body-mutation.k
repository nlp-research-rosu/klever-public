requires "semantic.k"

module BODY-MUTATION-VERIFICATION
  imports MPY-SEMANTIC

  syntax Program ::= "bodyMutatedProgram" [macro]
  syntax Stmts ::= "getRowBodyMutation" [macro]

  rule bodyMutatedProgram =>
    Module(FuncDef("get_row", Params("lst", "x", .Strings), getRowBodyMutation))

  // Material mutation: advance the row index by 2 rather than by 1.
  rule getRowBodyMutation =>
    Assign(Name("result"), ListExpr(.Exprs))
    Assign(Name("row"), Int(0))
    For(Name("values"), Name("lst"),
      Assign(Name("col"),
        BinOp("-", Call(Name("len"), Name("values"), .Exprs), Int(1)))
      While(Compare(Name("col"), CmpOp(">=", Int(0)), .CmpOps),
        If(Compare(Subscript(Name("values"), Name("col")),
                   CmpOp("==", Name("x")), .CmpOps),
          Assign(Name("result"),
            BinOp("+", Name("result"),
              ListExpr(TupleExpr(Name("row"), Name("col"), .Exprs), .Exprs))),
          .Stmts)
        Assign(Name("col"), BinOp("-", Name("col"), Int(1))))
      Assign(Name("row"), BinOp("+", Name("row"), Int(2))))
    Return(Name("result"))
endmodule
