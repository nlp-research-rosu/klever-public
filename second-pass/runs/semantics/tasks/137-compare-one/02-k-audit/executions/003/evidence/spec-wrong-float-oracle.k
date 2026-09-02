requires "wrong-float-oracle.k"

module SPEC-WRONG-FLOAT-ORACLE
  imports WRONG-FLOAT-ORACLE

  // False for real Python: compare_one(1.0, 2.0) returns 2.0, not None.
  claim <k> runCompare(1.0, 2.0) => noneV </k>
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
