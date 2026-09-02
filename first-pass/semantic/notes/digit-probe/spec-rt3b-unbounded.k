requires "verif3b.k"
module RT3BU-SPEC
  imports VERIF3B
  claim <k> #intOf(DS:IntSeq, 0) => DS </k> requires validDec(DS) [all-path]
endmodule
