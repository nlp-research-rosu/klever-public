requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [is-prime-from]:
        <mpy>
          <k> invoke("is_prime_from", intVal(N), intVal(D), solutionDefs)
            => boolVal(refPrimeFrom(N, D)) ...
          </k>
          <result> _R:Result </result>
        </mpy>
    requires N >=Int 2 andBool D >=Int 2

  claim [is-prime]:
        <mpy>
          <k> invoke("is_prime", intVal(N), solutionDefs)
            => boolVal(refPrime(N)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim [choose-prime]:
        <mpy>
          <k> invoke("choose_prime", intVal(N), intVal(BEST), solutionDefs)
            => intVal(refChoose(N, BEST)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim [largest-prime]:
        <mpy>
          <k> invoke("largest_prime", listVal(VS), solutionDefs)
            => intVal(refLargest(VS)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim [digit-sum]:
        <mpy>
          <k> invoke("digit_sum", intVal(N), solutionDefs)
            => intVal(refDigitSum(N)) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  // Deliberately false: for satisfying witness VS = intVal(2), the actual
  // result is 2 while this mutation requires 3.
  claim [entry-off-by-one]:
        <mpy>
          <k> init(solutionProgram, listVal(VS)) => .K </k>
          <result>
            noResult => result(intVal(refAnswer(VS) +Int 1))
          </result>
        </mpy>
endmodule
