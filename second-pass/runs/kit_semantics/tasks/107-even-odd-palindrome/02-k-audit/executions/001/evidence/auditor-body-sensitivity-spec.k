requires "auditor-body-mutation.k"

module AUDITOR-BODY-SENSITIVITY-SPEC
  imports VERIFICATION

  // The original n=1 result must fail after mutating the executed closure body.
  claim [body-sensitivity]:
    <k> Call(solutionClosure(), Int(N))
      => tuple(vCons(0, vCons(1, .ValSeq)))
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
