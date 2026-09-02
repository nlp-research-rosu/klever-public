requires "verif2.k"
module SPEC2-CNB imports BF-PROBE2
  claim <k> dispatch(P:IntSeq) => res(?R:Int) </k> ensures ?R ==Int idxCNB(P) [all-path]
endmodule
