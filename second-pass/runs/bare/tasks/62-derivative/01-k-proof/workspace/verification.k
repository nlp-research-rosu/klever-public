requires "semantic.k"

module VERIFICATION
  imports MPY

  // This macro is deliberately the exact constructor tree emitted in
  // solution.mpy. Keeping it here makes the proof talk about the translated
  // program rather than a hand-written mathematical stand-in.
  syntax Pgm ::= "solutionProgram" [macro]
  syntax Stmts ::= "solutionFunctions" [macro]
  syntax Map ::= "solutionFuns" [macro]

  rule solutionProgram => Module(solutionFunctions)
  rule solutionFuns => #collect(solutionFunctions)
  rule solutionFunctions =>
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
              BinOp("*", Name("degree"),
                Subscript(Name("xs"), Int(0)))),
            Call(
              Name("derivative_helper"),
              Subscript(Name("xs"), Slice(Int(1), NoBound, NoBound)),
              BinOp("+", Name("degree"), Int(1)))))))

  // Mathematical model over runtime coefficient sequences. For integer
  // coefficients, #bin("*", IntV(N), C) is exactly N *Int C by semantic.k.
  // Leaving it in this factored form also describes Python's stuck/error
  // behavior outside the supported numeric fragment without assuming a type.
  syntax Values ::= "#differentiate" "(" Int "," Values ")" [function]

  rule #differentiate(_N, .Values) => .Values
  rule #differentiate(N, (C, CS))
    => (#bin("*", IntV(N), C), #differentiate(N +Int 1, CS))
endmodule
