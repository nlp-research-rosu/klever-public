requires "verification.k"

module AUDITOR-FALSE-SPEC
  imports VERIFICATION

  // Fresh auditor mutation: n=1000 actually returns (48, 60), not (49, 60).
  claim [fresh-false-result-at-maximum]:
    <k> Call(solutionClosure(), Int(N))
      => tuple(vCons(49, vCons(60, .ValSeq)))
    </k>
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
    requires N ==Int 1000
endmodule
