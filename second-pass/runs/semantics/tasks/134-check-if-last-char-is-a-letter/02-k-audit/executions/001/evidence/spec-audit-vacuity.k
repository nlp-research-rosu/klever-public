requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the original empty-string claim requires false.
  // The starting state is concrete and satisfiable, but the destination is true.
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
