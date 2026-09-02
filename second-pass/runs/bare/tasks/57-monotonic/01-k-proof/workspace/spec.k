requires "verification.k"

module SPEC
  imports VERIFICATION

  // Universal functional-correctness claim over every finite integer list.
  claim <k>
          #run(solutionProgram, listVal(L))
        => #monotonicSpec(L)
        </k>

  // Prompt examples, proved through the same translated-program semantics.
  claim <k>
          #run(
            solutionProgram,
            listVal(cons(1, cons(2, cons(4, cons(20, nil))))))
        => boolVal(true)
        </k>

  claim <k>
          #run(
            solutionProgram,
            listVal(cons(1, cons(20, cons(4, cons(10, nil))))))
        => boolVal(false)
        </k>

  claim <k>
          #run(
            solutionProgram,
            listVal(cons(4, cons(1, cons(0, cons(-10, nil))))))
        => boolVal(true)
        </k>
endmodule
