// FAIL — 3-way differential, leg 2 (SUBSORT ONLY): the same bare VS:ValSeq claim breaks as
// soon as the IntVs subsort merely EXISTS in the definition: narrowing VS now leaves an
// uncovered third branch VS = inj(IntVs) that no rule matches (the disjoint-copy junk).
requires "verif-subsort.k"
module LEN-SUBSORT-SPEC
  imports VERIF-SUBSORT
  claim <k> cloop(list(VS:ValSeq)) => .K </k> <acc> A:Int => lenAcc(VS, A) </acc> [all-path]
endmodule
