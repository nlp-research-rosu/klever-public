requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports CHOOSE-NUM-VERIFICATION

  // Deliberately false: at X=1, Y=2 the program returns 2, not 4.
  claim [false-result-plus-two]:
    <k> #chooseNum(X:Int, Y:Int)
      => largestEvenInRange(X, Y) +Int 2
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
