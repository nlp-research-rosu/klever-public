requires "verif4.k"
module ORIGRT-SPEC
  imports VERIF4
  syntax Bool ::= validDec(IntSeq) [function, total]
  rule validDec(iCons(C:Int, T:IntSeq)) => (49 <=Int C andBool C <=Int 57) andBool allDig(T)
  rule validDec(.IntSeq) => false
  claim <k> #intOf(DS:IntSeq, 0) => DS </k> requires validDec(DS) [all-path]
endmodule
