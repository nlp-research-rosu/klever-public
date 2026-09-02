requires "../../tmp/audit-work/pairs-audit/verification.k"

module AUDIT-FALSE-MUTATION
  imports PAIRS-VERIFICATION-LEMMAS

  // Deliberately false: negate the result-constraining obligation while
  // retaining the exact source configuration and every post-state cell.
  // Satisfying witness INPUT=[0,0]: execution returns true, but this target is
  // notBool pairsIS([0,0]) = false.
  claim [negated-result]:
    <k>
      Call(closureVal(("l", .ParamNames), pairsBody, 0),
           (list(intValues(INPUT:IntSeq)), .Exprs))
      =>
      notBool pairsIS(INPUT)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(intValues(seenAfterIS(INPUT, .IntSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
