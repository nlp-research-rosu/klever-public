requires "verification.k"

module SPEC-AUDIT-VACUITY-GROUND
  imports VERIFICATION

  // Fresh ground off-by-one mutation. The source state is satisfiable and the
  // target recurrence evaluates to 1 for [1,2]; this false destination asks 2.
  claim [false-ground-off-by-one]:
    <k>
      #targetCall(mainCall, ref(0), 0, 0)
    =>
      2
    </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      0 |-> list(vCons(1, vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
