requires "verif-klist.k"

module SPEC-CONSUME-SPEC
  imports VERIF-KLIST

  // the narrowing question: symbolic L:List consumed head-first by a circularity
  claim <k> #sum(L:List) => .K ... </k>
        <acc> A:Int => A +Int sumL(L) </acc>
        [all-path]
endmodule
