// CONTRAST (FAILS): the kernel as a bare function lemma. L sits buried inside isSorted(insert(X,L)),
// a function argument — not a position any execution rule matches — so kprove never case-splits L,
// insert(X,L) stays unreduced, and the proof is stuck. The fix is spec.k: an execution driver that
// splits L in the <k> open (a circularity), the SAME lesson as val-cast / spec-control-seq.
requires "verif.k"
module SORT-BURIED-SPEC
  imports SORT
  claim <k> run(isSorted(insert(X:Int, L:IntSeq))) => true </k> requires isSorted(L) [all-path]
endmodule
