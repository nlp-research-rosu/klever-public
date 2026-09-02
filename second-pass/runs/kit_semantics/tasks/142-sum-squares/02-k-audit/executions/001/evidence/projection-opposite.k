requires "verification.k"

module PROJECTION-OPPOSITE
  imports VERIFICATION

  // Deliberately false value interpretation: the guarded projection of the
  // ground Int 2 must be 2, not 3.
  claim [wrong-projection]:
    <k> projectIntTotal(2) => 3 </k>
    <env> 0 </env>
    <scopes> .Map </scopes>
    <scopeLoc> 0 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
