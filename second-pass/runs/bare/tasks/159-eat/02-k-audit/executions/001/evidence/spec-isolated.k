requires "/tmp/audit-work/159-eat/candidate-src/verification.k"

module SPEC-CLAIM-1
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => carrotContract(NUMBER, NEED, REMAINING)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool NEED <=Int REMAINING
endmodule

module SPEC-CLAIM-2
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(NUMBER, NEED, REMAINING))
            => carrotContract(NUMBER, NEED, REMAINING)
          </k>
        </mpy>
    requires validInput(NUMBER, NEED, REMAINING)
             andBool REMAINING <Int NEED
endmodule

module SPEC-CLAIM-3
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(5, 6, 10))
            => result(11, 4)
          </k>
        </mpy>
endmodule

module SPEC-CLAIM-4
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(4, 8, 9))
            => result(12, 1)
          </k>
        </mpy>
endmodule

module SPEC-CLAIM-5
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(1, 10, 10))
            => result(11, 0)
          </k>
        </mpy>
endmodule

module SPEC-CLAIM-6
  imports VERIFICATION
  claim <mpy>
          <k> run(solutionProgram, args(2, 11, 5))
            => result(7, 0)
          </k>
        </mpy>
endmodule
