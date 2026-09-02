requires "/audit-output/evidence/verification-body-mutated.k"

module SPEC-BODY-MUTATED
  imports VERIFICATION

  // For every float list of length at least two, executing the actual
  // translated entry point returns the exhaustive scan specification.
  claim [entry-point]:
    <k>
      #applyK(
        toCall(closureVal(("numbers", .ParamNames), findClosestBody, 0)),
        (list(floatVals(fCons(A, fCons(B, FS)))), .Vals))
      => tuple(vCons(
           closestLowVS(
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
