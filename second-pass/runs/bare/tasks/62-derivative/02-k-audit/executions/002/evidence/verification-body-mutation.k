requires "verification.k"

module VERIFICATION-BODY-MUTATION
  imports VERIFICATION

  // Reviewer mutation: the helper body now adds degree to a coefficient
  // instead of multiplying. This is a real constructor-level body change.
  syntax Pgm ::= "bodyMutatedProgram" [macro]
  syntax Stmts ::= "bodyMutatedFunctions" [macro]
  syntax Map ::= "bodyMutatedFuns" [macro]

  rule bodyMutatedProgram => Module(bodyMutatedFunctions)
  rule bodyMutatedFuns => #collect(bodyMutatedFunctions)
  rule bodyMutatedFunctions =>
    FuncDef("derivative", Params("xs"),
      Return(
        Call(
          Name("derivative_helper"),
          Subscript(Name("xs"), Slice(Int(1), NoBound, NoBound)),
          Int(1))))
    FuncDef("derivative_helper", Params("xs", "degree"),
      If(Compare(Name("xs"), CmpOp("==", ListExpr(.Exprs))),
        Return(ListExpr(.Exprs)),
        Return(
          BinOp("+",
            ListExpr(
              BinOp("+", Name("degree"),
                Subscript(Name("xs"), Int(0)))),
            Call(
              Name("derivative_helper"),
              Subscript(Name("xs"), Slice(Int(1), NoBound, NoBound)),
              BinOp("+", Name("degree"), Int(1)))))))
endmodule
