requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: (3,4,5) satisfies the precondition, but the submitted
  // program returns true, not false.
  claim [false-positive-c]:
    <k> #runRightAngleTriangle(A:Int, B:Int, C:Int) => false </k>
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
    requires A >Int 0 andBool B >Int 0 andBool C >Int 0
      andBool A *Int A +Int B *Int B ==Int C *Int C
endmodule
