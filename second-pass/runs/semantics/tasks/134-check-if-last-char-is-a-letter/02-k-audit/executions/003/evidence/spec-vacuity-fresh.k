requires "verification.k"

module SPEC-VACUITY-FRESH
  imports VERIFICATION

  // Deliberately false result mutation. The precondition is realized by "".
  // The submitted program and the trusted canonical both return false.
  claim
    <k> #checkIfLastChar(str(.IntSeq)) => true </k>
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
