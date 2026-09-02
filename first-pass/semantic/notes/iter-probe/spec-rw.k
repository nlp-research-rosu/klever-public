requires "verif-rw.k"

module ITER-RW-SPEC
  imports ITER-RW

  // Same claim as spec-fn.k, verbatim — the only difference between the two runs
  // is the iterNext wiring in the semantics.
  claim <k> #drive(list(VS:ValSeq)) => .K </k> [all-path]
endmodule
