requires "verif4.k"
module SPEC4-REFORM imports BF-PROBE4
  claim <k> dispatchC(P:IntSeq) => res(?R:Int) </k>
    ensures ?I:Int ==Int idx(P) andBool ?R ==Int combWith(?I) [all-path]
endmodule
