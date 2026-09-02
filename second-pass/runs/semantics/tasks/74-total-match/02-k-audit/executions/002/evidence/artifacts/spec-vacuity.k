requires "verification.k"

module SPEC-VACUITY
  imports TOTAL-MATCH-VERIFICATION

  // Deliberately false result obligation: in the <= branch the real submitted
  // program returns A, but this mutation demands B. A concrete satisfying
  // counterexample is A=[], B=["a"], for which 0 <= 1 and [] != ["a"].
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
