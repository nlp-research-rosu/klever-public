requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY

  // Exact syntactic abbreviations for the two bodies in solution.mpy.
  syntax Stmts ::= "digitSumLoopBody" [macro]
  rule digitSumLoopBody =>
      AugAssign(Name("total"), "+",
        BinOp("%", Name("number"), Int(10)))
      AugAssign(Name("number"), "//", Int(10))

  syntax Stmts ::= "digitSumBody" [macro]
  rule digitSumBody =>
      If(Compare(Name("number"), CmpOp("<", Int(0))),
        Assign(Name("sign"), UnaryOp("-", Int(1)))
        Assign(Name("number"), UnaryOp("-", Name("number"))),
        Assign(Name("sign"), Int(1)))
      Assign(Name("total"), Int(0))
      While(Compare(Name("number"), CmpOp(">=", Int(10))),
        digitSumLoopBody)
      Return(BinOp("+", Name("total"),
        BinOp("*", Name("sign"), Name("number"))))

  syntax Stmts ::= "orderByPointsBody" [macro]
  rule orderByPointsBody =>
      Return(Call(Name("sorted"), Name("nums"),
        KwArg("key", Name("digit_sum"))))

  syntax Module ::= "solutionModule" [macro]
  rule solutionModule =>
      Module(
        FuncDef("digit_sum", Params("number"), digitSumBody)
        FuncDef("order_by_points", Params("nums"), orderByPointsBody))

  // Mathematical summaries used by the claims.
  syntax Int ::= magnitude(Int) [function, total]
               | leadingDigit(Int) [function, total]
               | lowerDigitSum(Int) [function, total]
               | lowerDigitSumAcc(Int, Int) [function, total]
               | signedDigitSum(Int) [function, total]

  syntax Bool ::= allInts(ValSeq) [function, total]

  // The intended stable ordering, conditional on the supplied semantics'
  // contract for the external Python primitive sorted(..., key=...).
  syntax ValSeq ::= expectedOrder(ValSeq) [function, total]
endmodule

module VERIFICATION
  imports VERIFICATION-SYNTAX

  rule magnitude(N:Int) => N
    requires N >=Int 0
  rule magnitude(N:Int) => 0 -Int N
    requires N <Int 0

  rule leadingDigit(N:Int) => N
    requires 0 <=Int N andBool N <Int 10
  rule leadingDigit(N:Int)
    => leadingDigit((N -Int pyMod(N, 10)) /Int 10)
    requires N >=Int 10
  rule leadingDigit(N:Int) => leadingDigit(0 -Int N)
    requires N <Int 0

  rule lowerDigitSum(N:Int) => lowerDigitSumAcc(N, 0)
    requires N >=Int 0
  rule lowerDigitSum(N:Int) => lowerDigitSumAcc(0 -Int N, 0)
    requires N <Int 0

  rule lowerDigitSumAcc(N:Int, S:Int) => S
    requires 0 <=Int N andBool N <Int 10
  rule lowerDigitSumAcc(N:Int, S:Int)
    => lowerDigitSumAcc(
         (N -Int pyMod(N, 10)) /Int 10,
         S +Int pyMod(N, 10))
    requires N >=Int 10
  rule lowerDigitSumAcc(N:Int, S:Int)
    => lowerDigitSumAcc(0 -Int N, S)
    requires N <Int 0

  rule signedDigitSum(N:Int)
    => lowerDigitSum(magnitude(N)) +Int leadingDigit(magnitude(N))
    requires N >=Int 0
  rule signedDigitSum(N:Int)
    => lowerDigitSum(magnitude(N)) -Int leadingDigit(magnitude(N))
    requires N <Int 0

  rule allInts(.ValSeq) => true
  rule allInts(vCons(_:Int, REST:ValSeq)) => allInts(REST)
  rule allInts(vCons(V:Val, _:ValSeq)) => false
    requires notBool isInt(V)

  rule expectedOrder(VS:ValSeq)
    => sortKeyVS(
         VS,
         closureVal("number", digitSumBody, 0))
endmodule
