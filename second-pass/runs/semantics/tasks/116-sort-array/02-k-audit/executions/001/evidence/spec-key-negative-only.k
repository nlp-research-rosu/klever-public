requires "/tmp/audit-work/rebuild/verification.k"

module REVIEW-SPEC-KEY-NEGATIVE-ONLY
  imports SORT-ARRAY-VERIFICATION

  claim
    <k> Call(popcountKeyClosure, Int(N)) => 0 </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N <Int 0
endmodule
