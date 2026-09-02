requires "verif-opaque.k"
module NESTOP-SPEC
  imports NESTOP
  claim <k> innerLoop(J:Int, HI:Int, A:Int) => innerAcc(J, HI, A) ... </k> [all-path]
  claim <k> outerLoop(I:Int, HI:Int, A:Int) => outerAcc(I, HI, A) ... </k> [all-path]
endmodule
