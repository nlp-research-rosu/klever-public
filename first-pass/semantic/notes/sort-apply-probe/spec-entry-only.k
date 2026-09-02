requires "verif.k"
module APPLY-ENTRY-ONLY
  imports APPLY
  // entry claim ALONE (no variable loop-invariant lemma). Prior finding: stuck.
  claim <k> sumLoop(sortI(L:IntSeq), 0) => sumOf(sortI(L)) ... </k> [all-path]
endmodule
