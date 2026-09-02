requires "verification.k"

module SAME-CHARS-SPEC
  imports SAME-CHARS-VERIFICATION

  // For arbitrary strings, the result is equality of their distinct
  // character-code sets.  sameSet is mutual membership, as defined by MPY-SET.
  claim
    <k>
      #sameChars(S0:IntSeq, S1:IntSeq)
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
