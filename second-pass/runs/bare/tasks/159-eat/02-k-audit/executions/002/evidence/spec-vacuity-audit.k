requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh reviewer mutation of symbolic claim 1: the first result component is
  // deliberately one too large. The precondition is satisfiable, for example
  // NUMBER=5, NEED=6, REMAINING=10; the real result is result(11,4), not
  // result(12,4).
  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => result(NUMBER +Int NEED +Int 1, REMAINING -Int NEED)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool NEED <=Int REMAINING
endmodule
