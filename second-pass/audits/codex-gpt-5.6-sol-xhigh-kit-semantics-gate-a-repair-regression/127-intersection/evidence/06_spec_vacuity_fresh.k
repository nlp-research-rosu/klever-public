requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // Ordered intervals satisfy the entry precondition. Their intersection is
  // [10,13], whose coordinate length 3 is prime, so the real result is "YES".
  // This deliberately false mutation requires "NO".
  claim [wrong-length-three-result]:
    <k>
      Call(
        Name("intersection"),
        tuple(vCons(10, vCons(13, .ValSeq))),
        tuple(vCons(0, vCons(20, .ValSeq))))
      => str(strToCodes("NO"))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(
              "intersection" |->
                closureVal(("interval1", "interval2"), intersectionBody, 0),
              parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
