requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable empty-list input: the real body
  // takes its early return and produces true.
  claim [false-empty-result]:
    <k> Call(Name("move_one_ball"), (list(.ValSeq), .Exprs))
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
