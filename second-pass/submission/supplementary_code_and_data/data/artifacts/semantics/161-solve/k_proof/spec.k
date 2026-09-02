requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [swaps-when-a-letter-exists]:
    <k> #runSolve(CS:IntSeq) => str(mapSwap(CS)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires notBool (CS ==K mapSwap(CS))

  claim [reverses-when-no-letter-exists]:
    <k> #runSolve(CS:IntSeq) => str(revIS(CS)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosure(), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires CS ==K mapSwap(CS)
endmodule
