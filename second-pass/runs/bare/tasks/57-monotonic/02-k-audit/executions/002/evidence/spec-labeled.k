requires "verification.k"

module SPEC-LABELED
  imports VERIFICATION

  claim [label(universal)]:
        <k>
          #run(solutionProgram, listVal(L))
        => #monotonicSpec(L)
        </k>

  claim [label(prompt-increasing)]:
        <k>
          #run(
            solutionProgram,
            listVal(cons(1, cons(2, cons(4, cons(20, nil))))))
        => boolVal(true)
        </k>

  claim [label(prompt-nonmonotonic)]:
        <k>
          #run(
            solutionProgram,
            listVal(cons(1, cons(20, cons(4, cons(10, nil))))))
        => boolVal(false)
        </k>

  claim [label(prompt-decreasing)]:
        <k>
          #run(
            solutionProgram,
            listVal(cons(4, cons(1, cons(0, cons(-10, nil))))))
        => boolVal(true)
        </k>
endmodule
