requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [simplify-full-domain]:
    <k>
      #applyK(
        toCall(closureVal(("x", "n"), simplifyBody, 0)),
        (str(iCons(XHEAD, XTAIL)),
         str(iCons(NHEAD, NTAIL)),
         .Vals))
      =>
      scanResult(
        seqConcat(
          seqConcat(iCons(XHEAD, XTAIL), iCons(47, .IntSeq)),
          iCons(NHEAD, NTAIL)),
        0,
        0,
        0,
        0,
        0)
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
    requires isDigitC(XHEAD)
     andBool validScan(
      seqConcat(
        seqConcat(XTAIL, iCons(47, .IntSeq)),
        iCons(NHEAD, NTAIL)),
      0,
      XHEAD -Int 48,
      0,
      0,
      0)
endmodule
