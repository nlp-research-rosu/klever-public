requires "verification-vacuity.k"

module SPEC-VACUITY
  imports VERIFICATION-VACUITY

  claim
    <mpy>
      <k> verifyRange(solutionProgram, 1, 1000, 0, 0)
        => verified </k>
      <env> .Map </env>
      <return> noReturn </return>
    </mpy>
endmodule
