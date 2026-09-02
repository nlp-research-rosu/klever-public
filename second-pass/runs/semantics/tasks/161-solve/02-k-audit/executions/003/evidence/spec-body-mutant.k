requires "verification-body-mutant.k"

module SPEC-BODY-MUTANT
  imports VERIFICATION-BODY-MUTANT

  claim [mutated-body-must-not-prove-swapcase]:
    <k> #runSolveMutant(CS:IntSeq) => str(mapSwap(CS)) </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map => "solve" |-> solutionClosureMutant(), parent(-1))
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
endmodule
