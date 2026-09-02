requires "verification-body-mutant.k"

module SPEC-BODY-SENSITIVITY
  imports MPY-VERIFICATION-BODY-MUTANT

  // The original theorem says empty input returns true. The body mutant
  // returns false, so this must build and then fail at the reachable result.
  claim [empty-original-result]:
        <mpy>
          <k> Run(mutatedSolutionProgram, "correct_bracketing", "")
            => boolVal(true) </k>
          <functions> .Map => ?_FS:Map </functions>
          <env> .Map => ?_ENV:Map </env>
        </mpy>
endmodule
