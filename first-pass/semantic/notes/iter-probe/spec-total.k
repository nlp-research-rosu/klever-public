requires "verif-total.k"

module ITER-TOTAL-SPEC
  imports ITER-TOTAL

  // Same shape of claim as spec-fn.k: walk a symbolic ValSeq to completion.
  claim <k> #drive(VS:ValSeq) => .K </k> [all-path]
endmodule
