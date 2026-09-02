requires "verif3.k"
module SORT-SPEC
  imports SORT
  // B <= X and B <= head(L) and L sorted  ⟹  insert(X,L) sorted and B <= head(insert(X,L)).
  claim <k> ind(B:Int, X:Int, L:IntSeq) => .K </k>
    requires isSorted(L) andBool B <=Int X andBool lbHead(B, L)
    ensures  isSorted(insert(X, L)) andBool B <=Int ihead(insert(X, L)) [all-path]
endmodule
