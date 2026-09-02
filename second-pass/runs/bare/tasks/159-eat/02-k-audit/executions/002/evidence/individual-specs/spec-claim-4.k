requires "verification.k"

module SPEC-CLAIM-4
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(4, 8, 9))
            => result(12, 1)
          </k>
        </mpy>
endmodule
