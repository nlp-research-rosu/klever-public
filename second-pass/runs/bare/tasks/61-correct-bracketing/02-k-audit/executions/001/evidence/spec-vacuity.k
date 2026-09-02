requires "verification.k"

module SPEC-VACUITY
  imports MPY-VERIFICATION

  // Fresh reviewer mutation: the real program returns true on the satisfying
  // empty-string input, so requiring false must leave an unmet result.
  claim [false-empty-result]:
        <mpy>
          <k> Run(solutionProgram, "correct_bracketing", "")
            => boolVal(false) </k>
          <functions> .Map => ?_FS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
endmodule
