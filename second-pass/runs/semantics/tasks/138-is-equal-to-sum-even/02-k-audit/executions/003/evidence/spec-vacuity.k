requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation. N=8 satisfies the precondition, while the actual
  // program returns true; demanding false is therefore a meaningful false goal.
  claim
    <k> #isEqualToSumEven(N:Int) => false </k>
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
    requires N ==Int 8
endmodule
