requires "verification.k"

module SPEC-GROUND
  imports VERIFICATION

  claim <mpy>
          <k> invoke("is_prime_from", intVal(2), intVal(2), solutionDefs)
            => boolVal(true) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("is_prime", intVal(1), solutionDefs)
            => boolVal(false) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("choose_prime", intVal(5), intVal(3), solutionDefs)
            => intVal(5) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("largest_prime",
                     listVal(intVal(4), intVal(11), intVal(3)),
                     solutionDefs)
            => intVal(11) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> invoke("digit_sum", intVal(123), solutionDefs)
            => intVal(6) ...
          </k>
          <result> _R:Result </result>
        </mpy>

  claim <mpy>
          <k> init(solutionProgram,
                   listVal(intVal(4), intVal(11), intVal(3))) => .K
          </k>
          <result> noResult => result(intVal(2)) </result>
        </mpy>
endmodule
