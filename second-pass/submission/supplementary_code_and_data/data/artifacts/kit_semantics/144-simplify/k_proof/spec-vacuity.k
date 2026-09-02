requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [false-result]:
    <k>
      #applyK(
        toCall(closureVal(("x", "n"), simplifyBody, 0)),
        (str(iCons(49, iCons(47, iCons(53, .IntSeq)))),
         str(iCons(53, iCons(47, iCons(49, .IntSeq)))),
         .Vals))
      =>
      false
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
endmodule
