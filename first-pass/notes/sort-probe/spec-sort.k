// FULL SORT CORRECTNESS: sortL(L) is SORTED and a PERMUTATION of L (count matches for the symbolic
// witness Y = every element). Both halves in one claim, by induction on L, using the insert kernels.
requires "verif-full.k"
module SORT-FULL-SPEC
  imports SORT-FULL
  claim <k> sortInd(Y:Int, L:IntSeq) => .K </k>
    ensures isSorted(sortL(L)) andBool count(Y, sortL(L)) ==Int count(Y, L) [all-path]
endmodule
