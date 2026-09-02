// baseline: fold-vs-loop equivalence over a SYMBOLIC digit sequence DS (the "back half").
requires "verif.k"
module SEQFOLD-SPEC
  imports VERIF
  claim <k> #iter(DS:IntSeq, A:Int) => evenSeq(DS, A) </k> [all-path]
endmodule
