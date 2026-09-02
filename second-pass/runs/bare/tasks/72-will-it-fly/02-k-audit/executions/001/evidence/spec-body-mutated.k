requires "verification-body-mutated.k"

module WILL-IT-FLY-BODY-MUTATED-SPEC
  imports HUMAN-EVAL-VERIFICATION-BODY-MUTATED

  claim [body-sensitivity]:
    <k> run(solutionProgramBodyMutated, pyList(IS:IntList), pyInt(W:Int))
        => pyBool(canFlyMut(IS, W)) </k>
    <generatedCounter> 0 </generatedCounter>
endmodule
