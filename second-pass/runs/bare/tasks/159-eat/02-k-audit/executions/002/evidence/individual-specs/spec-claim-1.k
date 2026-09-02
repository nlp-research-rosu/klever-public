requires "verification.k"

module SPEC-CLAIM-1
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => carrotContract(NUMBER, NEED, REMAINING)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool NEED <=Int REMAINING
endmodule
