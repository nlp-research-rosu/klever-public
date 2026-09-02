requires "verif3.k"
module SPEC3 imports BF-PROBE3
  claim <k> d8(P:IntSeq) => res(?R:Int) </k> ensures ?R ==Int idx8(P) [all-path]
endmodule
