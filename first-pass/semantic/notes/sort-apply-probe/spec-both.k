requires "verif.k"
module APPLY-BOTH
  imports APPLY
  // (1) loop invariant over a FRESH variable S, cell-framed (...) so it can apply mid-execution.
  claim <k> sumLoop(S:IntSeq, A:Int) => A +Int sumOf(S) ... </k> [all-path]
  // (2) entry: loop over the OPAQUE sorted output. Can kprove discharge it via claim (1), S:=sortI(L)?
  claim <k> sumLoop(sortI(L:IntSeq), 0) => sumOf(sortI(L)) ... </k> [all-path]
endmodule
