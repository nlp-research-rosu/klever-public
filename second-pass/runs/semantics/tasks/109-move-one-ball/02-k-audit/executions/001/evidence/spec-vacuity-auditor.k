requires "verification.k"

module SPEC-VACUITY-AUDITOR
  imports VERIFICATION

  // Fresh false result mutation. The entry precondition is fully satisfiable:
  // [] is an intended input, and both Python implementations return true.
  claim [empty-wrongly-returns-false]:
    <k>
      Call(Name("move_one_ball"), list(intVals(.IntSeq)))
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              "move_one_ball" |-> MOVE-ONE-BALL-CLOSURE,
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
