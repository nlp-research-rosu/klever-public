requires "verification.k"

module SPEC-CLAIM-6
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(2, 11, 5))
            => result(7, 0)
          </k>
        </mpy>
endmodule
