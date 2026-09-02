requires "reference-semantics/semantics.k"

module EXCHANGE-VERIFICATION-REAL
  imports MPY

  // Auditor replacement: a pure, structural embedding into the supplied
  // semantics' ordinary list constructors. No #iterNext rule is added.
  syntax ValSeq ::= intSeqVals(IntSeq) [function, total]
  rule intSeqVals(.IntSeq) => .ValSeq
  rule intSeqVals(iCons(I:Int, R:IntSeq)) => vCons(I, intSeqVals(R))

  // Accumulator-form counts mirror the program's AugAssign exactly.  Besides
  // avoiding any reliance on algebraic normalization, oddAcc(0, VS) and
  // evenAcc(0, VS) are the ordinary odd/even element counts.
  syntax Int ::= oddAcc(Int, IntSeq) [function, total]
  rule oddAcc(A:Int, .IntSeq) => A
  rule oddAcc(A:Int, iCons(I:Int, R:IntSeq)) => oddAcc(A, R)
    requires pyMod(I, 2) ==Int 0
  rule oddAcc(A:Int, iCons(I:Int, R:IntSeq)) => oddAcc(A +Int 1, R)
    requires pyMod(I, 2) =/=Int 0

  syntax Int ::= evenAcc(Int, IntSeq) [function, total]
  rule evenAcc(A:Int, .IntSeq) => A
  rule evenAcc(A:Int, iCons(I:Int, R:IntSeq)) => evenAcc(A +Int 1, R)
    requires pyMod(I, 2) ==Int 0
  rule evenAcc(A:Int, iCons(I:Int, R:IntSeq)) => evenAcc(A, R)
    requires pyMod(I, 2) =/=Int 0

  syntax Val ::= exchangeResult(IntSeq, IntSeq) [function, total]
  rule exchangeResult(A:IntSeq, B:IntSeq)
    => str(iCons(89, iCons(69, iCons(83, .IntSeq))))
    requires oddAcc(0, A) <=Int evenAcc(0, B)
  rule exchangeResult(A:IntSeq, B:IntSeq)
    => str(iCons(78, iCons(79, .IntSeq)))
    requires oddAcc(0, A) >Int evenAcc(0, B)

  // These macros are the exact constructor form generated in solution.mpy.
  // Factoring the loop bodies makes the induction claims readable.
  syntax Stmts ::= "ODD-BODY" [macro]
  rule ODD-BODY
    => If(
         Compare(BinOp("%", Name("number"), Int(2)),
                 CmpOp("!=", Int(0))),
         AugAssign(Name("odd"), "+", Int(1)),
         .Stmts)

  syntax Stmts ::= "EVEN-BODY" [macro]
  rule EVEN-BODY
    => If(
         Compare(BinOp("%", Name("number"), Int(2)),
                 CmpOp("==", Int(0))),
         AugAssign(Name("even"), "+", Int(1)),
         .Stmts)

  syntax Stmt ::= "exchangeDef" [macro]
  rule exchangeDef
    => FuncDef(
         "exchange",
         Params("lst1", "lst2"),
         Assign(Name("odd"), Int(0))
         Assign(Name("even"), Int(0))
         Assign(Name("number"), Int(0))
         For(Name("number"), Name("lst1"), ODD-BODY)
         For(Name("number"), Name("lst2"), EVEN-BODY)
         If(Compare(Name("odd"), CmpOp("<=", Name("even"))),
            Return(Str("YES")),
            .Stmts)
         Return(Str("NO")))
endmodule
