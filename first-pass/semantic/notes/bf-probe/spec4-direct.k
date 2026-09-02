requires "verif4.k"
module SPEC4-DIRECT imports BF-PROBE4
  claim <k> dispatchC(P:IntSeq) => res(?R:Int) </k> ensures ?R ==Int combDirect(P) [all-path]
endmodule
