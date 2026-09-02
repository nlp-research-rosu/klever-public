requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: the even accumulator starts one too high.
  // At n=1 the actual result is (0,1), but this demands (1,1).
  claim
    <mpy>
      <k> verifyRange(solutionProgram, 1, 1000, 1, 0)
        => verified </k>
      <env> .Map </env>
      <return> noReturn </return>
    </mpy>
endmodule
