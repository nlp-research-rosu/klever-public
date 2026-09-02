requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false: for CS = .IntSeq the implementation returns 0, not 1.
  claim
    <k>
      #callCountDistinct(CS:IntSeq)
      =>
      isLen(dedupCodes(mapLower(CS))) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
