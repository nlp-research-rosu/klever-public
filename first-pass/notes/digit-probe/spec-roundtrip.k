// (B) the round-trip bridge: is digitCodes(intOf(DS)) == DS PROVABLE for valid symbolic DS?
requires "verif.k"
module ROUNDTRIP-SPEC
  imports VERIF
  claim <k> digitCodes(intOf(DS:IntSeq)) => DS </k> requires validDec(DS) [all-path]
endmodule
