requires "verif4.k"
module GENNV-SPEC
  imports VERIF4
  claim <k> #intOf(DS:IntSeq, A:Int) => cat(digitCodes(A +Int 1), DS) </k>
    requires A >=Int 1 andBool allDig(DS) [all-path]
endmodule
