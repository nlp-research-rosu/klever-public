requires "verif5.k"
module CANON-SPEC
  imports VERIF5
  // (1) the fold invariant over a symbolic digit sequence (the reusable back-half)
  claim <k> #strFold(SEQ:IntSeq, A:Int) => evenSeq(SEQ, A) </k> [all-path]
  // (2) the ENTRY: canonical loop over str(intOf(CS)) closes via the bridge, for symbolic CS
  claim <k> #strFold(strCodes(intOf(CS:IntSeq)), 0) => evenSeq(CS, 0) </k> [all-path]
endmodule
