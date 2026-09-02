requires "verif4.k"
module SPEC4-CNB imports BF-PROBE4
  // rule-based idxCNB buried in combCNB's guard -> does it reduce to a bare Int and discharge?
  claim <k> dispatchC(P:IntSeq) => res(?R:Int) </k> ensures ?R ==Int combCNB(P) [all-path]
endmodule
