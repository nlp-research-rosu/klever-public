requires "/audit-output/evidence/verification-no-bridge.k"

module SHADOWED-LEN-WITNESS-NO-BRIDGE
  imports VERIFICATION

  claim [fixed-semantics-is-stuck]:
    <k>
      While(findClosestLoopCondition, findClosestLoopBody) => .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("numbers"   |-> list(floatVals(fCons(A, fCons(B, .FloatSeq)))))
        ("i"         |-> (0 => 1))
        ("j"         |-> (1 => 2))
        ("best_low"  |-> (A => closestLowVS(
          floatVals(fCons(A, fCons(B, .FloatSeq))), 0, 1, A, B)))
        ("best_high" |-> (B => closestHighVS(
          floatVals(fCons(A, fCons(B, .FloatSeq))), 0, 1, A, B)))
        ("low"       |-> (A => closestLowVS(
          floatVals(fCons(A, fCons(B, .FloatSeq))), 0, 1, A, B)))
        ("high"      |-> (B => closestHighVS(
          floatVals(fCons(A, fCons(B, .FloatSeq))), 0, 1, A, B))),
        parent(0))
      0 |-> scope("len" |-> builtinV("abs"), parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
