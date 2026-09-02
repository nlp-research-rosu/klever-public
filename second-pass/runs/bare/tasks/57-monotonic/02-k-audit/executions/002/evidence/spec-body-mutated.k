requires "verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports VERIFICATION-BODY-MUTATED

  // [2, 1] is decreasing, so the intended monotonic result is true. The
  // body-mutated program returns false because both branches test ascending.
  claim <k>
          #run(bodyMutatedProgram, listVal(cons(2, cons(1, nil))))
        => boolVal(true)
        </k>
endmodule
