requires "verif.k"
module PEEL-NV-SPEC
  imports VERIF
  claim <k> #peel(N:Int, A:Int) => evenOfInt(N, A) +Int 1 </k> requires N >=Int 0 [all-path]
endmodule
