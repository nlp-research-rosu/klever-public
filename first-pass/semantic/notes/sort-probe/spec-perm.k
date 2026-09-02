// PERMUTATION: insert(X,L) has the same multiset as X::L (for a symbolic witness Y = all elements).
// Proven by structural induction on L (self-circularity); no bound needed — count sees past the
// opaque recursive insert because the outer cons is always visible.
requires "verif.k"
module SORT-PERM-SPEC
  imports SORT
  claim <k> permInd(Y:Int, X:Int, L:IntSeq) => .K </k>
    ensures count(Y, insert(X, L)) ==Int count(Y, iCons(X, L)) [all-path]
endmodule
