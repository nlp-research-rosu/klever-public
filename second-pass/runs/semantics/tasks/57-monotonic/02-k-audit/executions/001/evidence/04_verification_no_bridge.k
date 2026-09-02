requires "reference-semantics/semantics.k"

module MONOTONIC-VERIFICATION-NO-BRIDGE
  imports MPY

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

  syntax Bool ::= isMonotonic(ValSeq) [function, total]
  rule isMonotonic(VS:ValSeq)
    => nondecreasing(VS) orBool nonincreasing(VS)
endmodule
