requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION-WITH-LOOP-LEMMA

  // Both intervals are [0,2], whose intersection has prime length 2.
  // The original program returns YES, so the mutated NO postcondition is false.
  claim <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(0), Int(2)),
                 TupleExpr(Int(0), Int(2)))
            => strVal("NO")
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
endmodule
