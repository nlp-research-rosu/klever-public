requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports VERIFICATION-BODY-MUTATED

  // At this satisfying input the submitted body returns result(11,4), while
  // the reviewer-mutated constructor body returns result(-1,4).
  claim <mpy>
          <k> run(solutionProgram, args(5, 6, 10))
            => result(11, 4)
          </k>
        </mpy>
endmodule
