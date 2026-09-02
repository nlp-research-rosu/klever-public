requires "verif4.k"
module PARTIAL4-SPEC
  imports PARTIAL4
  claim <k> loop(N:Int, C:Int) => cAcc(N, C) </k> requires N >=Int 1 [all-path]
endmodule
