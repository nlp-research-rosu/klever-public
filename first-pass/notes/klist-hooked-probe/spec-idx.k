requires "verif-klist-idx.k"

module SPEC-IDX-SPEC
  imports VERIF-KLIST-IDX

  // index-loop invariant over a SYMBOLIC builtin List of Vals: the circularity case-splits
  // on I vs size(L) (opaque Int), elements come through getTotal + the Int cast
  claim <k> #isum(L:List, I:Int) => .K ... </k>
        <acc> A:Int => A +Int sumFrom(L, I) </acc>
        requires 0 <=Int I andBool allIntFrom(L, I)
        [all-path]
endmodule
