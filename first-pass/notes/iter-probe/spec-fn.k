requires "verif-fn.k"

module ITER-FN-SPEC
  imports ITER-FN

  // Drive ANY (symbolic) list to completion. To prove it, kprove must case-split
  // the symbolic VS into .ValSeq / vCons. The claim is its own [all-path] circularity.
  claim <k> #drive(list(VS:ValSeq)) => .K </k> [all-path]
endmodule
