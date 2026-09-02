requires "verification.k"

module SPEC-CLAIM-5
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(1, 10, 10))
            => result(11, 0)
          </k>
        </mpy>
endmodule
