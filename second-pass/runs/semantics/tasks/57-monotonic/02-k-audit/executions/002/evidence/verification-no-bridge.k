requires "reference-semantics/semantics.k"

module MONOTONIC-VERIFICATION-NO-BRIDGE
  imports MPY

  syntax Module ::= "monotonicProgramNoBridge" [function, total]
  rule monotonicProgramNoBridge
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

  syntax Bool ::= nondecreasingNoBridge(ValSeq) [function, total]
                | nonincreasingNoBridge(ValSeq) [function, total]
  rule nondecreasingNoBridge(.ValSeq) => true
  rule nondecreasingNoBridge(vCons(_:Val, .ValSeq)) => true
  rule nondecreasingNoBridge(vCons(A:Val, vCons(B:Val, REST:ValSeq)))
    => applyCmp("<=", A, B)
       andBool nondecreasingNoBridge(vCons(B, REST))

  rule nonincreasingNoBridge(.ValSeq) => true
  rule nonincreasingNoBridge(vCons(_:Val, .ValSeq)) => true
  rule nonincreasingNoBridge(vCons(A:Val, vCons(B:Val, REST:ValSeq)))
    => applyCmp(">=", A, B)
       andBool nonincreasingNoBridge(vCons(B, REST))
endmodule
