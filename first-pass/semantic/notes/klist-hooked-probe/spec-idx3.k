requires "verif-klist-idx.k"

module SPEC-IDX3-SPEC
  imports VERIF-KLIST-IDX

  // production style: declare-then-guard summary; the fold must pull isInt(getTotal(L,I))
  // out of the allIntFrom premise
  claim <k> #isum(L:List, I:Int) => .K ... </k>
        <acc> A:Int => A +Int sumFromG(L, I) </acc>
        requires 0 <=Int I andBool allIntFrom(L, I)
        [all-path]
endmodule
