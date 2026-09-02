requires "reference-semantics/semantics.k"

module VERIFICATION-NO-BRIDGE
  imports MPY
  imports MAP-SYMBOLIC

  syntax IntVals ::= ".IntVals"
                   | ivCons(Int, IntVals)
  syntax ValSeq ::= asValSeq(IntVals) [function, total]
  rule asValSeq(.IntVals) => .ValSeq
  rule asValSeq(ivCons(I:Int, REST:IntVals))
    => vCons(I, asValSeq(REST))

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
             BinOp("*", Name("i"), Name("x"))
           )
         )
         .Stmts,
         .Stmts
       )

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
