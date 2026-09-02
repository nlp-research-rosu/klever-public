requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for positive A,B,C with A^2+B^2=C^2, the
  // implementation's first equality branch returns true, not false.
  // Satisfying witness: A=3, B=4, C=5.
  claim [false-pythagorean-c]:
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
