requires "verif.k"
module NEST-SPEC
  imports NEST
  claim <k> innerLoop(J:Int, HI:Int, C:Int) => innerAcc(J, HI, C) ... </k> [all-path]
  claim <k> outerLoop(I:Int, HI:Int, C:Int) => outerAcc(I, HI, C) ... </k> [all-path]
endmodule
