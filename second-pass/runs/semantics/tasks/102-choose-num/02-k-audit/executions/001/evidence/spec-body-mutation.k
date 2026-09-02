requires "verification-body-mutation.k"

module CHOOSE-NUM-SPEC-BODY-MUTATION
  imports CHOOSE-NUM-VERIFICATION-BODY-MUTATION

  claim [mutated-body-must-not-prove-original-result]:
    <k> #chooseNumBodyMutation(X:Int, Y:Int) => largestEvenBodyMutation(X, Y) </k>
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
