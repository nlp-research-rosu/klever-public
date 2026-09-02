requires "verification.k"

module TOTAL-MATCH-ENTRY-LEFT-SPEC
  imports TOTAL-MATCH-VERIFICATION

  claim
    <k> runTotalMatch(A:StrSeq, B:StrSeq)
      => list(strVals(A))
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires totalChars(A) <=Int totalChars(B)
endmodule
