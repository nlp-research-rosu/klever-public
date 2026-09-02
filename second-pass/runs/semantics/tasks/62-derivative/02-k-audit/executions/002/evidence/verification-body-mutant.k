requires "reference-semantics/semantics.k"

module VERIFICATION-BODY-MUTANT
  imports MPY
  imports MAP-SYMBOLIC

  // A recursively typed sequence represents every finite list of integer
  // polynomial coefficients and gives the prover a genuine induction sort.
  syntax IntVals ::= ".IntVals"
                   | ivCons(Int, IntVals)
  syntax ValSeq ::= asValSeq(IntVals) [function, total]
  rule asValSeq(.IntVals) => .ValSeq
  rule asValSeq(ivCons(I:Int, REST:IntVals))
    => vCons(I, asValSeq(REST))

  // Executable mathematical fold for the derivative. N is the original
  // coefficient index and ACC is the prefix already produced.
  syntax ValSeq ::= derivativeAcc(ValSeq, IntVals, Int) [function]
                  | derivativeSeq(IntVals) [function]
  rule derivativeSeq(VS:IntVals)
    => derivativeAcc(.ValSeq, VS, 0)
  rule derivativeAcc(ACC:ValSeq, .IntVals, _:Int)
    => ACC
  rule derivativeAcc(ACC:ValSeq, ivCons(_:Int, REST:IntVals), 0)
    => derivativeAcc(ACC, REST, 1)
  rule derivativeAcc(ACC:ValSeq, ivCons(I:Int, REST:IntVals), N:Int)
    => derivativeAcc(
         valSeqConcat(ACC, vCons(N *Int I, .ValSeq)),
         REST,
         N +Int 1
       )
    requires N >Int 0

  // enumerate is eager in the supplied semantics.  The symbolic constructor
  // below is an equivalent lazy representation; the simplification equation
  // and its two iterator equations are obtained directly by composing enumVS
  // with the supplied list iterator rules.  Exposing one coefficient at a
  // time lets the reachability claim use a structural loop invariant.
  syntax ValSeq ::= enumIntSeq(IntVals, Int)
  rule enumVS(asValSeq(VS:IntVals), N:Int)
    => enumIntSeq(VS, N)
    [simplification]

  rule <k> #iterNext(list(enumIntSeq(.IntVals, _:Int)))
        => #iterDone ... </k>
  rule <k> #iterNext(list(enumIntSeq(ivCons(I:Int, REST:IntVals), N:Int)))
        => #iterYield(
             tuple(vCons(N, vCons(I, .ValSeq))),
             list(enumIntSeq(REST, N +Int 1))
           )
        ... </k>

  syntax Expr ::= "derivativeTarget" [macro]
  rule derivativeTarget
    => TupleExpr(Name("i"), Name("x"))

  syntax Stmt ::= "derivativeLoopStep" [macro]
  rule derivativeLoopStep
    => If(
         Compare(Name("i"), CmpOp(">", Int(0))),
         Expr(
           Call(
             Attribute(Name("result"), "append"),
             BinOp("+", Name("i"), Name("x"))
           )
         )
         .Stmts,
         .Stmts
       )

  // The closure below is exactly the translated body in solution.mpy.
  syntax Val ::= "derivativeClosure" [macro]
  rule derivativeClosure
    => closureVal(
         ("xs", .ParamNames),
         Expr(Str("Return the coefficients of the derivative of a polynomial."))
         Assign(Name("result"), ListExpr(.Exprs))
         For(
           derivativeTarget,
           Call(Name("enumerate"), Name("xs")),
           derivativeLoopStep
           .Stmts
         )
         Return(Name("result"))
         .Stmts,
         0
       )
endmodule
