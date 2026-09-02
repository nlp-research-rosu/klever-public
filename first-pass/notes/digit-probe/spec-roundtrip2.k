requires "verif2.k"
module ROUNDTRIP2-SPEC
  imports VERIF2
  claim <k> digitCodes(intOf(DS:IntSeq)) => DS </k> requires validDec(DS) [all-path]
endmodule
