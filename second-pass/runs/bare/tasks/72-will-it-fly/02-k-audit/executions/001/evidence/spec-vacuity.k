requires "verification.k"

module WILL-IT-FLY-SPEC-VACUITY
  imports HUMAN-EVAL-VERIFICATION

  // Fresh false result mutation.  The satisfying input q=[3], w=5 returns true.
  claim [false-singleton-result]:
    <k> run(solutionProgram,
            pyList(cons(3, nil)), pyInt(5))
        => pyBool(false) </k>
    <generatedCounter> 0 </generatedCounter>
endmodule
