requires "verification-body-mutant.k"

module WILL-IT-FLY-SPEC-BODY-MUTANT
  imports HUMAN-EVAL-VERIFICATION-BODY-MUTANT

  // False witness: IS=nil and W=-1 makes the mutated body true but mutCanFly false.
  claim [body-sensitivity]:
    <k> run(mutatedSolutionProgram, pyList(IS:IntList), pyInt(W:Int))
        => pyBool(mutCanFly(IS, W)) </k>
    <generatedCounter> 0 </generatedCounter>
endmodule
