requires "reference-semantics/semantics.k"

module MONOTONIC-VERIFICATION
  imports MPY

  // This is the exact AST generated in solution.mpy, factored out so that the
  // proof starts by loading and calling the submitted Python function.
  syntax Module ::= "monotonicProgram" [function, total]
  rule monotonicProgram
    => Module(
         FuncDef(
           "monotonic",
           Params("l"),
           Expr(Str("Return whether l is monotonically nondecreasing or nonincreasing."))
           Return(
             BoolOp(
               "or",
               Compare(
                 Name("l"),
                 CmpOp("==", Call(Name("sorted"), Name("l")))
               ),
               Compare(
                 Name("l"),
                 CmpOp(
                   "==",
                   Call(
                     Name("sorted"),
                     Name("l"),
                     KwArg("reverse", Bool(true))
                   )
                 )
               )
             )
           )
         )
       )

  // Independent, executable definitions of the two adjacent-element order
  // predicates. These equations also document that equality is permitted.
  syntax Bool ::= nondecreasing(ValSeq) [function, total]
                | nonincreasing(ValSeq) [function, total]
  rule nondecreasing(.ValSeq) => true
  rule nondecreasing(vCons(_:Val, .ValSeq)) => true
  rule nondecreasing(vCons(A:Val, vCons(B:Val, REST:ValSeq)))
    => applyCmp("<=", A, B) andBool nondecreasing(vCons(B, REST))

  rule nonincreasing(.ValSeq) => true
  rule nonincreasing(vCons(_:Val, .ValSeq)) => true
  rule nonincreasing(vCons(A:Val, vCons(B:Val, REST:ValSeq)))
    => applyCmp(">=", A, B) andBool nonincreasing(vCons(B, REST))

  // sortVS is explicitly a trusted ascending-sort abstraction in the supplied
  // semantics. sortEquality is a proof-only equality summary, introduced at
  // the same Compare point where MPY-LIST would otherwise use opaque ==K.
  syntax Bool ::= sortEquality(ValSeq, ValSeq)
                  [function, total, symbol(sortEquality), no-evaluators]
  rule <k>
         Compare(list(A:ValSeq), CmpOp("==", list(B:ValSeq)))
         => sortEquality(A, B)
       ... </k>
       [priority(45)]
  rule sortEquality(VS:ValSeq, sortVS(VS))
    => nondecreasing(VS)
    [simplification]
  // revVS unfolds once to revVSAcc before the equality summary sees it.
  rule sortEquality(
         VS:ValSeq,
         revVSAcc(sortVS(VS), .ValSeq)
       )
    => nonincreasing(VS)
    [simplification]

  // The natural-language contract: either adjacent order may hold.
  syntax Bool ::= isMonotonic(ValSeq) [function, total]
  rule isMonotonic(VS:ValSeq)
    => nondecreasing(VS) orBool nonincreasing(VS)
endmodule
