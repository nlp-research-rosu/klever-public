requires "verif2.k"
module SPEC2-IF imports BF-PROBE2
  // idxIf pinned in the POSTCONDITION; path cond from the #branch dispatch (faithful to full spec)
  claim <k> dispatch(P:IntSeq) => res(?R:Int) </k> ensures ?R ==Int idxIf(P) [all-path]
endmodule
