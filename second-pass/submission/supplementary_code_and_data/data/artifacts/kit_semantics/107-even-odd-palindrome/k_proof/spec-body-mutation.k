requires "verification-mutation.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // The mutated N=1 return must not establish the original result.
  claim [body-sensitive]:
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
