requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Fresh reviewer mutation: demand an off-by-one result. This is false for,
  // among many witnesses, mainCall on the satisfying heap list [1, 2]:
  // targetAnswer = 1, while this destination requires 2.
  claim [false-off-by-one]:
    <k>
      #targetCall(KIND:TargetCall, ref(H), L, R) ~> CONT
    =>
      (targetAnswer(KIND, VS, L, R) +Int 1) ~> CONT
    </k>
    <env> CALLER </env>
    <scopes> SCOPES </scopes>
    <scopeLoc> NEXTSCOPE </scopeLoc>
    <heap>
      (H |-> list(VS) HEAPREST)
    </heap>
    <heapLoc> NEXTHEAP </heapLoc>
    <stack> STACK </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires targetValid(KIND, VS, L, R)
endmodule
