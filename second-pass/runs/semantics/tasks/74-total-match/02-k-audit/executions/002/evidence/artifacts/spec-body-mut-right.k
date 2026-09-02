requires "verification-body-mut.k"

module TOTAL-MATCH-BODY-MUT-RIGHT-SPEC
  imports TOTAL-MATCH-VERIFICATION

  // Same right-branch theorem, but runTotalMatch's first loop now adds zero.
  // The satisfying witness A=["ab"], B=[] makes the original result B while
  // the mutated executable term returns A.
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
    requires totalChars(A) >Int totalChars(B)
endmodule
