requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports ANY-INT-VERIFICATION

  // Deliberately false: the real claim returns sumCondition, not its negation.
  // Satisfying counterexample: X=5, Y=2, Z=7, where sumCondition is true.
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
