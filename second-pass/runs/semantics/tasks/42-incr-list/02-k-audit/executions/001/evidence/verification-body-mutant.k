requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY

  // The exact constructor tree generated in solution.mpy.
  syntax Module ::= "solutionProgram" [function, total]
  rule solutionProgram =>
    Module(
      FuncDef("incr_list", Params("l"),
        Expr(Str("Return list with elements incremented by 1."))
        Assign(Name("result"), ListExpr(.Exprs))
        For(Name("x"), Name("l"),
          Expr(
            Call(
              Attribute(Name("result"), "append"),
              BinOp("+", Name("x"), Int(2)))))
        Return(Name("result"))))

  // Embed a symbolic sequence of Python integers into ValSeq and define the
  // mathematical element-wise increment used in the postcondition.
  syntax ValSeq ::= intVals(IntSeq)
                  | incrVals(IntSeq) [function, total]
  rule incrVals(.IntSeq) => .ValSeq
  rule incrVals(iCons(I:Int, IS:IntSeq)) =>
    vCons(I +Int 1, incrVals(IS))

  // Constructor-visible iterator equations let symbolic execution split on
  // the IntSeq domain rather than widening each element to an arbitrary Val.
  rule <k> #iterNext(list(intVals(.IntSeq))) => #iterDone ... </k>
  rule <k> #iterNext(list(intVals(iCons(I:Int, IS:IntSeq))))
        => #iterYield(I, list(intVals(IS))) ... </k>

  syntax Stmts ::= "incrLoopBody" [function, total]
  rule incrLoopBody =>
    Expr(
      Call(
        Attribute(Name("result"), "append"),
        BinOp("+", Name("x"), Int(1))))
    .Stmts

  // Right-associate concatenation so the loop invariant is preserved after
  // appending one singleton to a symbolic prefix.
  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]
  rule valSeqConcat(A:ValSeq, .ValSeq) => A
    [simplification]

  // Observe a returned heap object by its value. Temporary allocations remain
  // in the heap but are deliberately outside the functional postcondition.
  syntax KItem ::= "#observeResult"
  rule <k> ref(H:Int) ~> #observeResult => V ... </k>
       <heap> ... H |-> V:Val ... </heap>
endmodule
