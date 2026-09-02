requires "oracle-witness-verification.k"

module ORACLE-WITNESS-SPEC
  imports ORACLE-WITNESS-VERIFICATION

  // Python compare_one(1.0, 2.0) returns 2.0, not None.
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
    [label(wrong-same-float)]

  // Python compare_one("2,3", 0.0) returns "2,3", not None.
  claim <k> runCompare(
              str(iCons(50, iCons(44, iCons(51, .IntSeq)))),
              0.0)
          => noneV </k>
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
    [label(wrong-comma-decimal)]
endmodule
