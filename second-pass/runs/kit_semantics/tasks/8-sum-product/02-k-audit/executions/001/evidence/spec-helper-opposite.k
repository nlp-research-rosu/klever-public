requires "verification.k"

module SPEC-HELPER-OPPOSITE
  imports VERIFICATION

  // Deliberately opposite interpretation; must be rejected with residual 2.
  claim [projection-opposite]:
    <k> projectIntTotal(2) => 3 </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
