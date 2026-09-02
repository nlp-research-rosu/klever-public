requires "verification.k"

module ROUNDED-AVG-SPEC-INVERTED
  imports ROUNDED-AVG-VERIFICATION

  claim
    <k> roundedAvgCall(N:Int, M:Int) => -1 </k>
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
    requires N >Int 0 andBool M >Int 0 andBool N >Int M
endmodule
