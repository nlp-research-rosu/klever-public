requires "/tmp/audit-work/verification.k"

module REVIEWER-FRESH-VACUITY-SPEC
  imports PAIRS-VERIFICATION-LEMMAS

  // Deliberately false complement of the real result. The empty satisfying
  // witness INPUT=.IntSeq makes the program return false while this destination
  // requires notBool false = true.
  claim [wrong-complement]:
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
