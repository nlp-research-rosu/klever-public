requires "verification.k"

module TRIANGLE-SPEC-VACUITY-FRESH
  imports TRIANGLE-VERIFICATION

  // Deliberately false: (1,2,3) satisfies the precondition, but the real
  // function and the unmodified proof both return -1, not -2.
  claim [false-invalid-first]:
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => -2
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
    requires A +Int B <=Int C
endmodule
