requires "verification.k"

// Same first entry claim, but without importing the candidate's loop bridge.
module SPEC-NO-BRIDGE
  imports VERIFICATION

  claim <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => lengthResult(B -Int A)
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C <=Int A andBool D >=Int B
endmodule
