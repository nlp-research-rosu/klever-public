requires "verification.k"

module SAME-CHARS-SPEC-VACUITY
  imports SAME-CHARS-VERIFICATION

  // Deliberately false: equal input strings (for example both empty) make
  // sameSet(dedupCodes(S0), dedupCodes(S1)) true, so its negation is false.
  claim
    <k>
      #sameChars(S0:IntSeq, S1:IntSeq)
      =>
      notBool sameSet(dedupCodes(S0), dedupCodes(S1))
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
