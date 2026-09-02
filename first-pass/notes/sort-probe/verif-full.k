// verif-full.k — lift the two PROVEN insert kernels (ordering: spec.k; permutation: spec-perm.k) to
// the full insertion sort: sortL(L) is a sorted permutation of L. The kernels are stated here as
// [simplification] lemmas (SOUND — each is proven in its own spec against module SORT, which this
// module does not touch, so the kernel proofs stay honest).
requires "verif.k"
module SORT-FULL
  imports SORT

  // --- the two proven kernels, as trusted lemmas ---
  rule isSorted(insert(X:Int, L:IntSeq)) => true requires isSorted(L) [simplification]
  rule count(Y:Int, insert(X:Int, L:IntSeq)) => count(Y, iCons(X, L)) [simplification]

  // --- full insertion sort ---
  syntax IntSeq ::= sortL(IntSeq) [function, total]
  rule sortL(.IntSeq) => .IntSeq [simplification]
  rule sortL(iCons(X:Int, R:IntSeq)) => insert(X, sortL(R)) [simplification]

  // driver: structural induction on L
  syntax KItem ::= sortInd(Int, IntSeq)
  rule <k> sortInd(_Y:Int, .IntSeq) => .K ... </k>
  rule <k> sortInd(Y:Int, iCons(_X:Int, R:IntSeq)) => sortInd(Y, R) ... </k>
endmodule
