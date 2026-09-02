requires "verification.k"

module AUDIT-SPEC-VACUITY
  imports VERIFICATION

  // False for a satisfiable pristine call state: both Python implementations
  // return 0 for n=0, while this mutation requires the K execution to return 1.
  claim [false-entry-zero]:
    <k> Call(FIZZ-BUZZ-CLOSURE, 0) => 1 </k>
    <env> 0 </env>
    <scopes> 0 |-> scope(.Map, parent(-1)) -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
