requires "wrong-decimal-oracle.k"

module SPEC-WRONG-DECIMAL-ORACLE
  imports WRONG-DECIMAL-ORACLE

  // False for real Python: compare_one("1", 2.0) returns 2.0, not "1".
  claim <k> runCompare(str(iCons(49, .IntSeq)), 2.0)
          => str(iCons(49, .IntSeq)) </k>
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
