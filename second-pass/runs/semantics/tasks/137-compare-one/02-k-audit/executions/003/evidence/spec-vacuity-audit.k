requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Deliberately false: compare_one(1, 2) returns 2, not 1.
  claim <k> runCompare(1, 2) => 1 </k>
        <env> 0 </env>
        <scopes> 0 |-> scope(.Map, parent(-1))
                  -1 |-> builtinsScope </scopes>
        <scopeLoc> 1 </scopeLoc>
        <heap> .Map </heap>
        <heapLoc> 0 </heapLoc>
        <stack> .List </stack>
        <ret> noRet </ret>
        <exc> NoExc </exc>
        <exit-code> 0 </exit-code>
endmodule
