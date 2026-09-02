requires "verification.k"

module WILL-IT-FLY-SPEC-VACUITY-AUDIT
  imports HUMAN-EVAL-VERIFICATION

  // Deliberately false: the submitted program returns true for [3], 5.
  claim [false-singleton-result]:
    <k> run(solutionProgram, pyList(cons(3, nil)), pyInt(5))
        => pyBool(false) </k>
    <generatedCounter> 0 </generatedCounter>
endmodule
