requires "reference-semantics/semantics.k"

module AUDIT-VERIFICATION-NO-BRIDGES
  imports MPY

  syntax Stmts ::= "polyBody" [macro]
  rule polyBody =>
    Return(
      Call(
        Name("sum"),
        ListComp(
          BinOp(
            "*",
            Name("coeff"),
            Call(Attribute(Name("math"), "pow"), Name("x"), Name("i"))),
          CompFor(
            TupleExpr(Name("i"), Name("coeff")),
            Call(Name("enumerate"), Name("xs")),
            Bool(true)))))

  syntax Stmt ::= "bracketLoop" [macro]
  rule bracketLoop =>
    While(
      Compare(
        BinOp(
          "*",
          Call(Name("poly"), Name("xs"), Name("begin")),
          Call(Name("poly"), Name("xs"), Name("end"))),
        CmpOp(">", Int(0))),
      AugAssign(Name("begin"), "*", Int(2))
      AugAssign(Name("end"), "*", Int(2)))

  syntax Stmt ::= "bisectLoop" [macro]
  rule bisectLoop =>
    While(
      Compare(
        BinOp("-", Name("end"), Name("begin")),
        CmpOp(">", Float(1e-10))),
      Assign(
        Name("center"),
        BinOp("/", BinOp("+", Name("begin"), Name("end")), Int(2)))
      If(
        Compare(
          BinOp(
            "*",
            Call(Name("poly"), Name("xs"), Name("center")),
            Call(Name("poly"), Name("xs"), Name("begin"))),
          CmpOp(">", Int(0))),
        Assign(Name("begin"), Name("center")),
        Assign(Name("end"), Name("center"))))

  syntax Stmts ::= "findZeroBody" [macro]
  rule findZeroBody =>
    Assign(Name("begin"), UnaryOp("-", Int(1)))
    Assign(Name("end"), Int(1))
    bracketLoop
    bisectLoop
    Return(Name("begin"))

  syntax Bool ::= validPolynomial(ValSeq)
    [function, total, symbol(validPolynomial), no-evaluators]
  syntax Val ::= bracketLow(ValSeq)
               | bracketHigh(ValSeq)
               | bisectLow(ValSeq, Val, Val)
               | bisectHigh(ValSeq, Val, Val)
  syntax Bool ::= approximatesZero(ValSeq, Val) [function]
  rule approximatesZero(
         VS:ValSeq,
         bisectLow(VS, bracketLow(VS), bracketHigh(VS))) => true
    requires validPolynomial(VS)
  syntax KItem ::= #checkApprox(ValSeq)
  rule <k> V:Val ~> #checkApprox(VS:ValSeq)
        => approximatesZero(VS, V) ... </k>
endmodule
