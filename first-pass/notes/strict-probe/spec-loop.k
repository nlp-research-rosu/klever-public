requires "verif-strict.k"

module SPEC-LOOP-SPEC
  imports VERIF-STRICT

  // the circularity: strict-body loop over a symbolic cons list folds to the summary
  claim <k> #sum(VS:ValSeq) => .K ... </k>
        <acc> A:Int => clampSum(VS, A) </acc>
        [all-path]
endmodule
