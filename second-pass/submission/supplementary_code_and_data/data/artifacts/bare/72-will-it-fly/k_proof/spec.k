requires "verification.k"

module WILL-IT-FLY-SPEC
  imports HUMAN-EVAL-VERIFICATION

  // The universal contract: for every integer list and every weight bound,
  // execution is exactly palindrome(IS) AND sum(IS) <= W.
  claim [universal]:
    <k> run(solutionProgram, pyList(IS:IntList), pyInt(W:Int))
        => pyBool(canFly(IS, W)) </k>
    <generatedCounter> 0 </generatedCounter>

  // All four examples from prompt.py are retained as concrete regression
  // claims, so failures are easy to diagnose independently of the theorem.
  claim [example-unbalanced]:
    <k> run(solutionProgram,
            pyList(cons(1, cons(2, nil))), pyInt(5))
        => pyBool(false) </k>
    <generatedCounter> 0 </generatedCounter>

  claim [example-overweight]:
    <k> run(solutionProgram,
            pyList(cons(3, cons(2, cons(3, nil)))), pyInt(1))
        => pyBool(false) </k>
    <generatedCounter> 0 </generatedCounter>

  claim [example-balanced]:
    <k> run(solutionProgram,
            pyList(cons(3, cons(2, cons(3, nil)))), pyInt(9))
        => pyBool(true) </k>
    <generatedCounter> 0 </generatedCounter>

  claim [example-singleton]:
    <k> run(solutionProgram,
            pyList(cons(3, nil)), pyInt(5))
        => pyBool(true) </k>
    <generatedCounter> 0 </generatedCounter>
endmodule
