// the STRENGTHENED (generalized-accumulator) claim
requires "verif4.k"
module GEN-SPEC
  imports VERIF4
  claim <k> #intOf(DS:IntSeq, A:Int) => cat(digitCodes(A), DS) </k>
    requires A >=Int 1 andBool allDig(DS) [all-path]
endmodule
