requires "verification-body-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION-BODY-MUTATION

  claim
    <mpy>
      <k> verifyRange(solutionProgram, 1, 1000, 0, 0)
        => verified </k>
      <env> .Map </env>
      <return> noReturn </return>
    </mpy>
endmodule
