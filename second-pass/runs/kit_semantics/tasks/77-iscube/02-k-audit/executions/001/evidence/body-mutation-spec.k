requires "verification.k"

module BODY-MUTATION-SPEC
  imports VERIFICATION

  // With the executed increment changed from +1 to +2, 27 is skipped.
  claim [twenty-seven-remains-a-cube]:
    <k> Call(Name("iscube"), Int(27)) => true </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
       0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
