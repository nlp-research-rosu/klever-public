requires "verif3.k"
module RT3U-SPEC
  imports VERIF3
  claim <k> #intOf(DS:IntSeq, 0) => DS </k> requires validDec(DS) [all-path]
endmodule
