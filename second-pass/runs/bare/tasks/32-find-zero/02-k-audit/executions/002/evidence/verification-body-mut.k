requires "semantic.k"

module VERIFICATION-BODY-MUT
  imports SEMANTIC

  syntax Program ::= "solutionBodyMut" [macro]
  rule solutionBodyMut =>
    Module(
      FuncDef("evaluate_polynomial", Params("xs", "x"),
        Assign(Name("value"), Int(0))
        Assign(Name("power"), Int(1))
        For(Name("coefficient"), Name("xs"),
          Assign(
            Name("value"),
            BinOp(
              "+",
              Name("value"),
              BinOp("*", Name("coefficient"), Name("power"))))
          Assign(Name("power"), BinOp("*", Name("power"), Name("x"))))
        Return(Name("value")))
      FuncDef("find_zero", Params("xs"),
        Assign(Name("left"), UnaryOp("-", Int(1)))
        Assign(Name("right"), Int(1))
        While(Compare(
          BinOp(
            "*",
            Call(Name("evaluate_polynomial"), Name("xs"), Name("left")),
            Call(Name("evaluate_polynomial"), Name("xs"), Name("right"))),
          CmpOp(">", Int(0))),
          Assign(Name("left"), BinOp("*", Name("left"), Int(2)))
          Assign(Name("right"), BinOp("*", Name("right"), Int(2))))
        While(Compare(
          BinOp("-", Name("right"), Name("left")),
          CmpOp(">", BinOp("/", Int(1), Int(10000000000)))),
          Assign(
            Name("middle"),
            BinOp("/", BinOp("+", Name("left"), Name("right")), Int(2)))
          If(Compare(
            BinOp(
              "*",
              Call(Name("evaluate_polynomial"), Name("xs"), Name("middle")),
              Call(Name("evaluate_polynomial"), Name("xs"), Name("left"))),
            CmpOp(">", Int(0))),
            Assign(Name("left"), Name("middle")),
            Assign(Name("right"), Name("middle"))))
        // Material mutation: the executed function body returns 42.
        Return(Int(42))))

  syntax Val ::= polyValueMut(List, Val) [function]
               | absRatMut(Val) [function, total]
  syntax Bool ::= leRatMut(Val, Val) [function, total]

  rule polyValueMut(.List, _X) => rat(0, 1) [simplification]
  rule polyValueMut(ListItem(C:Val) REST, X)
    => addRat(C, mulRat(X, polyValueMut(REST, X))) [simplification]
  rule absRatMut(rat(N, D)) => rat(0 -Int N, D)
    requires N <Int 0 [simplification]
  rule absRatMut(rat(N, D)) => rat(N, D)
    requires N >=Int 0 [simplification]
  rule leRatMut(rat(A, B), rat(C, D)) => A *Int D <=Int C *Int B
    [simplification]

  syntax Expr ::= "VerifyRootMut" "(" List "," Expr "," Val ")" [strict(2)]
  rule VerifyRootMut(COEFFS, ROOT:Val, TOLERANCE)
    => bool(leRatMut(absRatMut(polyValueMut(COEFFS, ROOT)), TOLERANCE))
endmodule
