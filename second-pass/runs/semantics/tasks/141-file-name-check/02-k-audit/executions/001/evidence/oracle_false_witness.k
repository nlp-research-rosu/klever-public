requires "verification.k"

module ORACLE-FALSE-WITNESS
  imports VERIFICATION

  // The real candidate and canonical Python functions both return "No" for
  // "a.pdf".  The proof extension can nonetheless interpret its unconstrained
  // observations so that the acceptance path is taken.
  claim [a-pdf-wrongly-accepted]:
    <k>
      runFileNameCheck(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
      => str(iCons(89, iCons(101, iCons(115, .IntSeq))))
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
    requires
      charCount(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))),
        46) ==Int 1
      andBool isLen(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
        >=Int 5
      andBool latinCode(
        headCode(
          iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq)))))))
      andBool allowedSuffix(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
      andBool digitCount(
        iCons(97, iCons(46, iCons(112, iCons(100, iCons(102, .IntSeq))))))
        <=Int 3
endmodule
