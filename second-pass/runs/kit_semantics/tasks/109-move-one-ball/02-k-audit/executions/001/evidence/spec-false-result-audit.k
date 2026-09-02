requires "verification.k"

module SPEC-FALSE-RESULT-AUDIT
  imports VERIFICATION

  // Fresh non-vacuity probe.  This keeps the exact submitted body but changes
  // the result obligation for a satisfying, nonempty prompt input from true to
  // false.  The expected residual is the unmet true-versus-false result.
  claim [false-prompt-true-result]:
    <k> Call(
          Name("move_one_ball"),
          (list(vCons(3, vCons(4, vCons(5, vCons(1, vCons(2, .ValSeq)))))), .Exprs))
        => false </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope(
         "move_one_ball" |-> closureVal("arr", moveOneBallBody, 0),
         parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
