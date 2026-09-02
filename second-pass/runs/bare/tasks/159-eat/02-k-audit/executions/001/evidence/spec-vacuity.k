requires "/tmp/audit-work/159-eat/candidate-src/verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation of symbolic branch 1: the first result component is
  // deliberately one too large. Witness (5,6,10) satisfies the precondition
  // and the real result is result(11,4), not result(12,4).
  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => result(NUMBER +Int NEED +Int 1, REMAINING -Int NEED)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool NEED <=Int REMAINING
endmodule
