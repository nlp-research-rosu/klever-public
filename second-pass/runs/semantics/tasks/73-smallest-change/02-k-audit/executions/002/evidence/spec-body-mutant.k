requires "verification-body-mutant.k"

module SPEC
  imports VERIFICATION

  claim [public-entry-bridge]:
    <k>
      #applyK(toCall(#mainClosure), (ref(H), .Vals)) ~> CONT
    =>
      #targetCall(mainCall, ref(H), 0, 0) ~> CONT
    </k>

  claim [helper-entry-bridge]:
    <k>
      #applyK(
        toCall(#helperClosure),
        (ref(H), L, R, .Vals))
      ~> CONT
    =>
      #targetCall(helperCall, ref(H), L, R) ~> CONT
    </k>

  claim [smallest-change-correct]:
    <k>
      #targetCall(KIND:TargetCall, ref(H), L, R) ~> CONT
    =>
      targetAnswer(KIND, VS, L, R) ~> CONT
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
