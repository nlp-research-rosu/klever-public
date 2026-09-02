requires "verif.k"
module FP-MAIN
  imports FP
  claim <k> loop(FS:FloatSeq, LO:Float, D:Float, ACC:FloatSeq) => mapFA(FS, LO, D, ACC) ... </k> [all-path]
endmodule
