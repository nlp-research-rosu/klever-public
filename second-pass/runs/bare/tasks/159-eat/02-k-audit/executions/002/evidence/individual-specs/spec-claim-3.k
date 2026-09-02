requires "verification.k"

module SPEC-CLAIM-3
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(5, 6, 10))
            => result(11, 4)
          </k>
        </mpy>
endmodule
