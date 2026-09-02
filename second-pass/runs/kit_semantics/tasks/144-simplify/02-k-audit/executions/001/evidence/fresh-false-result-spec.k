requires "verification.k"

module FRESH-FALSE-RESULT-SPEC
  imports VERIFICATION

  // Satisfying source input: (1/6) * (2/1) = 1/3, so the real result is false.
  // Requiring true is a deliberate false result-constraining obligation.
  claim [false-input-must-not-return-true]:
    <k>
      #applyK(
        toCall(closureVal(("x", "n"), simplifyBody, 0)),
        (str(iCons(49, iCons(47, iCons(54, .IntSeq)))),
         str(iCons(50, iCons(47, iCons(49, .IntSeq)))),
         .Vals))
      =>
      true
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
