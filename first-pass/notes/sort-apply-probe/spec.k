requires "verif.k"
module APPLY-SPEC
  imports APPLY
  // Sum the SORTED list. Iterates sortI(L). Does the loop consume the opaque sort output?
  claim <k> sumLoop(sortI(L:IntSeq), 0) => ?R:Int </k> ensures ?R ==Int sumOf(sortI(L)) [all-path]
endmodule
