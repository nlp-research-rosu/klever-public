requires "verification-body-mutated.k"

module SAME-CHARS-BODY-MUTATED-SPEC
  imports SAME-CHARS-BODY-MUTATED

  claim
    <k>
      #sameCharsBodyMut(S0:IntSeq, S1:IntSeq)
      =>
      sameSet(dedupCodes(S0), dedupCodes(S1))
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
    <exit-code> 0 </exit-code>
endmodule
