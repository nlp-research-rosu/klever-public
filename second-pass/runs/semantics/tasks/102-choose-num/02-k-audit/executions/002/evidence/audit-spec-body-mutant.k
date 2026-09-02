requires "audit-verification-body-mutant.k"

module AUDIT-SPEC-BODY-MUTANT
  imports AUDIT-BODY-MUTANT

  claim [original-result-after-body-mutation]:
    <k> #chooseNumMutant(X:Int, Y:Int)
      => largestEvenInRangeMutant(X, Y)
    </k>
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
    requires X >Int 0 andBool Y >Int 0
endmodule
