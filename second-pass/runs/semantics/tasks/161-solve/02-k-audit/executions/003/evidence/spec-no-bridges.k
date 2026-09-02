requires "verification-no-bridges.k"

module SPEC-NO-BRIDGES
  imports VERIFICATION-NO-BRIDGES

  claim [swap-without-proof-bridges]:
    <k> #runSolveNoBridges(CS:IntSeq) => str(mapSwap(CS)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosureNoBridges(), parent(-1))
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

  claim [reverse-without-proof-bridges]:
    <k> #runSolveNoBridges(CS:IntSeq) => str(revIS(CS)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosureNoBridges(), parent(-1))
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
