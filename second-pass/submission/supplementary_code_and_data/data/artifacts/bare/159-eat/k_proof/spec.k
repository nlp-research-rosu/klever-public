requires "verification.k"

module SPEC
  imports VERIFICATION

  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => carrotContract(NUMBER, NEED, REMAINING)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool NEED <=Int REMAINING

  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => carrotContract(NUMBER, NEED, REMAINING)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool REMAINING <Int NEED

  claim <mpy>
          <k> run(solutionProgram, args(5, 6, 10))
            => result(11, 4)
          </k>
        </mpy>

  claim <mpy>
          <k> run(solutionProgram, args(4, 8, 9))
            => result(12, 1)
          </k>
        </mpy>

  claim <mpy>
          <k> run(solutionProgram, args(1, 10, 10))
            => result(11, 0)
          </k>
        </mpy>

  claim <mpy>
          <k> run(solutionProgram, args(2, 11, 5))
            => result(7, 0)
          </k>
        </mpy>
endmodule
