requires "verif-partial.k"

module ITER-PARTIAL-SPEC
  imports ITER-PARTIAL

  // Same shape of claim as spec-fn.k: walk a symbolic ValSeq to completion.
  claim <k> #drive(VS:ValSeq) => .K </k> [all-path]
endmodule
