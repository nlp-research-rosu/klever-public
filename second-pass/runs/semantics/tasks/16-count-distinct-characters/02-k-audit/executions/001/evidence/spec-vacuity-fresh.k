requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Fresh reviewer mutation: the real formal result plus one.
  // CS = .IntSeq satisfies the original precondition and yields 0, so the
  // mutated obligation demands the demonstrably false result 1.
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
