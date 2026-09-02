requires "semantic.k"

module VERIFICATION
  imports SEMANTIC

  // This constant is the exact constructor tree emitted in solution.mpy.
  // Keeping it as a macro lets both krun and kprove execute the submitted AST.
  syntax Program ::= "solution" [macro]
  rule solution =>
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
        Return(BinOp("/", BinOp("+", Name("left"), Name("right")), Int(2)))))

  // Independent postcondition machinery.  Coefficients are in ascending order,
  // so this is Horner evaluation from the head: c0 + x * (c1 + x * ...).
  syntax Val ::= polyValue(List, Val) [function]
               | absRat(Val) [function, total]
  syntax Bool ::= leRat(Val, Val) [function, total]

  rule polyValue(.List, _X) => rat(0, 1) [simplification]
  rule polyValue(ListItem(C:Val) REST, X)
    => addRat(C, mulRat(X, polyValue(REST, X))) [simplification]

  rule absRat(rat(N, D)) => rat(0 -Int N, D)
    requires N <Int 0 [simplification]
  rule absRat(rat(N, D)) => rat(N, D)
    requires N >=Int 0 [simplification]
  rule leRat(rat(A, B), rat(C, D)) => A *Int D <=Int C *Int B
    [simplification]

  syntax Expr ::= "VerifyRoot" "(" List "," Expr "," Val ")" [strict(2)]
  rule VerifyRoot(COEFFS, ROOT:Val, TOLERANCE)
    => bool(leRat(absRat(polyValue(COEFFS, ROOT)), TOLERANCE))
endmodule
