requires "audit-context-probe.k"

module AUDIT-CONTEXT-PROBE-SPEC
  imports AUDIT-CONTEXT-PROBE

  // The continuation after #chooseNum observes the returned 2 and yields 102.
  claim [continuation-preserved]:
    <k> #chooseNum(1, 2) ~> #observeResult => 102 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
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
