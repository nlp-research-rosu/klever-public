requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: demand (high, high) instead of (low, high).
  // The satisfying input [1.0, 2.0] has original/model result (1.0, 2.0).
  claim [false-first-component]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(floatVals(fCons(A, fCons(B, FS)))), .Vals))
      => tuple(vCons(
           closestHighVS(
             floatVals(fCons(A, fCons(B, FS))), 0, 1,
             pairLow(orderPairState(A, B)),
             pairHigh(orderPairState(A, B))),
           vCons(
             closestHighVS(
               floatVals(fCons(A, fCons(B, FS))), 0, 1,
               pairLow(orderPairState(A, B)),
               pairHigh(orderPairState(A, B))),
             .ValSeq)))
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
    requires 0 <=Int floatSeqLen(FS)
endmodule
