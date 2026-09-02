requires "verification.k"

module MEMBER-FOLD-SPEC
  imports MEMBER-FOLD-VERIFICATION

  // `x in list(VS)` folds to memberOf(x, VS) for a symbolic list — the fold must
  // narrow VS structurally (a [total] valInSeq would only narrow the value).
  claim <k> #memberAcc(V:Val, list(VS:ValSeq)) => ?R:Bool ... </k>
        ensures ?R ==Bool memberOf(V, VS)
        [all-path]
endmodule
