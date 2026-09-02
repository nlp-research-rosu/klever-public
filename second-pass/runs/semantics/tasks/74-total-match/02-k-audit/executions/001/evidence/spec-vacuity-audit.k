requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports TOTAL-MATCH-VERIFICATION

  // Deliberately false: when A is no longer than B, the function returns A,
  // not B.  Witness A=["a"], B=["bb"] satisfies the precondition.
  claim
    <k> runTotalMatch(A:StrSeq, B:StrSeq)
      => list(strVals(B))
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
