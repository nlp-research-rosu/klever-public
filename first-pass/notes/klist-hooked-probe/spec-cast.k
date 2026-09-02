requires "verif-klist.k"

module SPEC-CAST-SPEC
  imports VERIF-KLIST

  // the cast question: Val elements under an allIntL premise, guarded {V}:>Int in fold + summary
  claim <k> #sumV(L:List) => .K ... </k>
        <acc> A:Int => A +Int sumVL(L) </acc>
        requires allIntL(L)
        [all-path]
endmodule
