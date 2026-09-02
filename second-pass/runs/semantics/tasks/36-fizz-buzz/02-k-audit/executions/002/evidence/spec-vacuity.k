requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Fresh false mutation: the real program and canonical implementation both
  // return 2 at n=78, so changing only the result obligation to 3 must fail.
  claim [false-entry-78]:
    <k> Call(FIZZ-BUZZ-CLOSURE, 78) => 3 </k>
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
