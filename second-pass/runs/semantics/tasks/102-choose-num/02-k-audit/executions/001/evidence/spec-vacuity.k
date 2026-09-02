requires "verification.k"

module CHOOSE-NUM-SPEC-VACUITY
  imports CHOOSE-NUM-VERIFICATION

  // Fresh reviewer mutation: the real result is falsely required to be two
  // greater than the proven largest-even result.
  claim [false-off-by-two]:
    <k> #chooseNum(X:Int, Y:Int) => largestEvenInRange(X, Y) +Int 2 </k>
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
