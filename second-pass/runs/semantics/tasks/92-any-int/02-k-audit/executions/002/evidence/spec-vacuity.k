requires "verification.k"

module ANY-INT-SPEC-VACUITY
  imports ANY-INT-VERIFICATION

  // False at the satisfying state X=5, Y=2, Z=7:
  // execution returns true, while notBool sumCondition(5,2,7) is false.
  claim
    <k> #anyInt(X:Int, Y:Int, Z:Int)
      => notBool sumCondition(X, Y, Z)
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
endmodule
