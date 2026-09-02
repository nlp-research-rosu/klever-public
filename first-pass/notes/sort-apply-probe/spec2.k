requires "verif.k"
module APPLY-SPEC2
  imports APPLY
  claim <k> sumLoop(sortI(L:IntSeq), A:Int) => ?R:Int </k> ensures ?R ==Int A +Int sumOf(sortI(L)) [all-path]
endmodule
