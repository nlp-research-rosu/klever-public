requires "verif.k"
module APPLY-VAR-SPEC
  imports APPLY
  // Same loop over a symbolic VARIABLE S, accumulator generalized so the recursion is a circularity.
  claim <k> sumLoop(S:IntSeq, A:Int) => ?R:Int </k> ensures ?R ==Int A +Int sumOf(S) [all-path]
endmodule
