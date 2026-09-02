requires "verif3.k"
module PARTIAL3-SPEC
  imports PARTIAL3
  // PARTIAL correctness: IF loop(N,C) halts, result == stepAcc(N,C). No termination proof.
  claim <k> loop(N:Int, C:Int) => stepAcc(N, C) </k> requires N >=Int 1 [all-path]
endmodule
