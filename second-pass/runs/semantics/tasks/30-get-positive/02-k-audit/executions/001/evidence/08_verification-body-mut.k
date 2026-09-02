requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUT
  imports MPY

  syntax Stmts ::= "getPositiveBodyMut" [macro]
  rule getPositiveBodyMut
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("x"), Name("l"), positiveLoopBodyMut)
       Return(Name("result"))

  syntax Stmts ::= "positiveLoopBodyMut" [macro]
  rule positiveLoopBodyMut
    => If(
         Compare(Name("x"), CmpOp(">", Int(1))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("x"))),
         .Stmts)

  syntax ValSeq ::= intValsMut(IntSeq)
  rule <k> #iterNext(list(intValsMut(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intValsMut(iCons(I, IS))))
        => #iterYield(I, list(intValsMut(IS))) ... </k>

  syntax ValSeq ::= filterPositiveMut(ValSeq, IntSeq) [function]
  rule filterPositiveMut(ACC, .IntSeq) => ACC
  rule filterPositiveMut(ACC, iCons(I, IS))
    => filterPositiveBranchMut(I >Int 0, ACC, I, IS)

  syntax ValSeq ::= filterPositiveBranchMut(Bool, ValSeq, Int, IntSeq)
                    [function, total]
  rule filterPositiveBranchMut(true, ACC, I, IS)
    => filterPositiveMut(
         valSeqConcat(ACC, vCons(I, .ValSeq)),
         IS)
  rule filterPositiveBranchMut(false, ACC, _I, IS)
    => filterPositiveMut(ACC, IS)
endmodule

