requires "verification.k"

// Fresh reviewer mutation.  Case 1 normally returns lengthResult(B-A).
// Replacing that result by constant "YES" is false for the satisfying witness
// A=0,B=4,C=-1,D=5, whose intersection length is the composite number 4.
module SPEC-VACUITY-AUDIT
  imports VERIFICATION-WITH-LOOP-LEMMA

  claim <mpy>
          <k>
            solutionProgram
            ~> runWith(
                 TupleExpr(Int(A), Int(B)),
                 TupleExpr(Int(C), Int(D)))
            => strVal("YES")
          </k>
          <functions> .Map => ?_FUNCTIONS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
        requires A <=Int B andBool C <=Int D
          andBool C <=Int A andBool D >=Int B
endmodule
