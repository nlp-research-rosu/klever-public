requires "verification.k"

module SPEC-VACUITY-AUDIT
  imports VERIFICATION

  // Fresh false result mutation: compare_one(1, 2) returns 2, never None.
  claim <k> runCompare(1, 2) => noneV </k>
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
    [label(false-int-result)]
endmodule
