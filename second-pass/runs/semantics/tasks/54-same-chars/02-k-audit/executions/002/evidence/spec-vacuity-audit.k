requires "verification.k"

module SAME-CHARS-SPEC-VACUITY-AUDIT
  imports SAME-CHARS-VERIFICATION

  // Deliberately false result obligation: invert the required Boolean result.
  // Satisfying witness S0 = S1 = .IntSeq makes the program return true while
  // this postcondition requires false.
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
