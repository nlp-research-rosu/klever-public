requires "verif-while.k"
module FPW-SPEC
  imports FPW
  // partial correctness: if it halts, ACC unchanged. Can the opaque-float guard split?
  claim <k> wloop(B:Float, ACC:Float) => ACC ... </k> [all-path]
endmodule
