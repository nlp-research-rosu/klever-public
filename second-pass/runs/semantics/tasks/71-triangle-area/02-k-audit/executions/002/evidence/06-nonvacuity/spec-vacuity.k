requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports TRIANGLE-VERIFICATION

  // Deliberately false: (A,B,C)=(3,4,5) satisfies the precondition, while the
  // real candidate and canonical Python functions both return 6.0, not -1.
  claim
    <k> Call(triangleAreaClosure, (A:Int, B:Int, C:Int, .Exprs))
      => -1
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
    requires A +Int B >Int C
     andBool A +Int C >Int B
     andBool B +Int C >Int A
endmodule
