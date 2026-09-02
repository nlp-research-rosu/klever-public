// (C) iterate str(N)=digitCodes(N) for a SYMBOLIC integer N — does the frozen seq unfold?
requires "verif.k"
module ITER-INT-SPEC
  imports VERIF
  claim <k> #iter(digitCodes(N:Int), 0) => evenSeq(digitCodes(N), 0) </k> requires N >=Int 0 [all-path]
endmodule
