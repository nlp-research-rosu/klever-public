// BRANCH: loop-break over a symbolic list(VS). DECIDES x<0 each step. Works with the TOTAL cast.
requires "verif.k"
module BRANCH-SPEC
  imports VERIF
  claim <k> loop(list(VS:ValSeq)) => .K </k> <acc> A:Int => prefixSumAcc(VS, A) </acc> requires allInt(VS) [all-path]
endmodule
