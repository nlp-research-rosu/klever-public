requires "verif5.k"
module CANONNV-SPEC
  imports VERIF5
  claim <k> #strFold(SEQ:IntSeq, A:Int) => evenSeq(SEQ, A) </k> [all-path]
  claim <k> #strFold(strCodes(intOf(CS:IntSeq)), 0) => evenSeq(CS, 0) +Int 1 </k> [all-path]
endmodule
