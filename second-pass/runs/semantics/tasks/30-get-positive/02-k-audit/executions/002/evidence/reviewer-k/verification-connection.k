requires "reference-semantics/semantics.k"

module VERIFICATION-CONNECTION
  imports MPY

  syntax Stmts ::= "connectionGetPositiveBody" [macro]
  rule connectionGetPositiveBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("x"), Name("l"), connectionPositiveLoopBody)
       Return(Name("result"))

  syntax Stmts ::= "connectionPositiveLoopBody" [macro]
  rule connectionPositiveLoopBody
    => If(
         Compare(Name("x"), CmpOp(">", Int(0))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("x"))),
         .Stmts)

  // Transparent materialization into the fixed semantics' native ValSeq.
  // Unlike the candidate's intVals iterator rules, these equations do not
  // intercept #iterNext; the fixed list iterator rules execute afterward.
  syntax ValSeq ::= materializeInts(IntSeq) [function, total]
  rule materializeInts(.IntSeq) => .ValSeq
  rule materializeInts(iCons(I, IS))
    => vCons(I, materializeInts(IS))

  syntax ValSeq ::= connectionFilter(ValSeq, IntSeq) [function]
  rule connectionFilter(ACC, .IntSeq) => ACC
  rule connectionFilter(ACC, iCons(I, IS))
    => connectionFilterBranch(I >Int 0, ACC, I, IS)

  syntax ValSeq ::= connectionFilterBranch(Bool, ValSeq, Int, IntSeq)
                    [function, total]
  rule connectionFilterBranch(true, ACC, I, IS)
    => connectionFilter(
         valSeqConcat(ACC, vCons(I, .ValSeq)),
         IS)
  rule connectionFilterBranch(false, ACC, _I, IS)
    => connectionFilter(ACC, IS)
endmodule
