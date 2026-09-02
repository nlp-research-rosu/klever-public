requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the realizable witness N = 1.
  claim [false-result]:
    <k> Call(solutionClosure(), Int(N))
      => tuple(vCons(1, vCons(1, .ValSeq)))
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
    requires N ==Int 1
endmodule
