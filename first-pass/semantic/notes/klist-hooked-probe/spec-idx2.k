requires "verif-klist-idx.k"

module SPEC-IDX2-SPEC
  imports VERIF-KLIST-IDX

  // container mechanics only: index-recursion vs opaque size(L), no domain premise
  claim <k> #isum(L:List, I:Int) => .K ... </k>
        <acc> A:Int => A +Int sumFrom(L, I) </acc>
        requires 0 <=Int I
        [all-path]
endmodule
