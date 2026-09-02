requires "verification.k"

module X-OR-Y-SPEC-VACUITY
  imports X-OR-Y-SUMMARY

  // Deliberately false result obligation. The precondition is the ordinary
  // initial state and is satisfied by n=7,x=34,y=12. Both Python programs
  // return 34, while this mutation requires 12.
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
    [label(false_prime_result)]
endmodule
