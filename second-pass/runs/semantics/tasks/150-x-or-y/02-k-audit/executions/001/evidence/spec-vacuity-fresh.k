requires "verification.k"

module X-OR-Y-AUDIT-VACUITY
  imports X-OR-Y-SUMMARY

  // Deliberately false: 7 is prime, so x_or_y(7, 34, 12) returns 34, not 12.
  // The initial configuration satisfies the candidate entry precondition.
  claim
    <k> #xOrY(7, 34, 12) => 12 </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    [label(false_result_n7)]
endmodule
