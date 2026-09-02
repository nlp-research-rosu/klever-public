requires "reference-semantics/semantics.k"

module VERIFICATION
  imports MPY

  // The translated body of solution.py.  Keeping it as a macro makes the
  // correspondence between the executable .mpy term and the proof term
  // explicit while allowing the specification to call the closure directly.
  syntax Stmts ::= "getPositiveBody" [macro]
  rule getPositiveBody
    => Assign(Name("result"), ListExpr(.Exprs))
       For(Name("x"), Name("l"), positiveLoopBody)
       Return(Name("result"))

  syntax Stmts ::= "positiveLoopBody" [macro]
  rule positiveLoopBody
    => If(
         Compare(Name("x"), CmpOp(">", Int(0))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             Name("x"))),
         .Stmts)

  // `intVals` is an isomorphic, symbolic embedding of arbitrary finite integer
  // sequences.  These two iterator rules expose exactly one constructor per
  // proof step, allowing the loop claim in spec.k to serve as the induction
  // hypothesis.
  syntax ValSeq ::= intVals(IntSeq)
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intVals(iCons(I, IS))))
        => #iterYield(I, list(intVals(IS))) ... </k>

  // Mathematical left-to-right filter, generalized over an accumulator so
  // that its recursive call is exactly the program loop invariant.
  syntax ValSeq ::= filterPositive(ValSeq, IntSeq) [function]
  rule filterPositive(ACC, .IntSeq) => ACC
  rule filterPositive(ACC, iCons(I, IS))
    => filterPositiveBranch(I >Int 0, ACC, I, IS)

  syntax ValSeq ::= filterPositiveBranch(Bool, ValSeq, Int, IntSeq)
                    [function, total]
  rule filterPositiveBranch(true, ACC, I, IS)
    => filterPositive(
         valSeqConcat(ACC, vCons(I, .ValSeq)),
         IS)
  rule filterPositiveBranch(false, ACC, _I, IS)
    => filterPositive(ACC, IS)
endmodule
