requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim <mpy>
          <k> invoke("is_prime_from", intVal(N), intVal(D), solutionDefs)
            => boolVal(refPrimeFrom(N, D)) ...
          </k>
          <result> _R:Result </result>
        </mpy>
    requires N >=Int 2 andBool D >=Int 2

  claim <mpy>
          <k> invoke("is_prime", intVal(N), solutionDefs)
            => boolVal(refPrime(N)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("choose_prime", intVal(N), intVal(BEST), solutionDefs)
            => intVal(refChoose(N, BEST)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("largest_prime", listVal(VS), solutionDefs)
            => intVal(refLargest(VS)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("digit_sum", intVal(N), solutionDefs)
            => intVal(refDigitSum(N)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> init(solutionProgram, listVal(VS)) => .K </k>
          <result> noResult
                => result(intVal(refAnswer(VS) +Int 1))
          </result>
        </mpy>
endmodule
