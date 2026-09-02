requires "verification.k"

module SUM-FOLD-SPEC
  imports SUM-FOLD-VERIFICATION

  // Fold invariant (circularity): #sumAcc(list(VS), ACC) folds to sumOf(VS, ACC).
  // The <k>-cell fold must narrow the symbolic VS structurally — the whole point of
  // making sum a rewrite, not a [function].
  claim <k> #sumAcc(list(VS:ValSeq), ACC:Int) => ?R:Int ... </k>
        requires allInt(VS)
        ensures  ?R ==Int sumOf(VS, ACC)
        [all-path]

  // Entry: `sum` resolves like any name (the -1 builtins scope), the call dispatches
  // on the builtinV value to the fold — a symbolic-list sum() is provable.
  claim <k> Call(Name("sum"), list(VS:ValSeq)) => ?R:Int ... </k>
        <env> 0 </env>
        <scopes> -1 |-> builtinsScope 0 |-> scope(.Map, parent(-1)) </scopes>
        requires allInt(VS)
        ensures  ?R ==Int sumOf(VS, 0)
        [all-path]
endmodule
