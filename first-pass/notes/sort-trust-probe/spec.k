requires "verif.k"
module SORTTRUST-SPEC
  imports SORTTRUST
  // running sorted(L) yields an output ?R that is provably sorted — via the trusted lemma, SYMBOLIC L.
  claim <k> prog(L:IntSeq) => done(?R:IntSeq) </k> ensures isSorted(?R) [all-path]
endmodule
