requires "verification.k"

module FRESH-VACUITY-SPEC
  imports VERIFICATION

  // Fresh audit mutation: 27 is a cube, so requiring false is meaningful and
  // false for this fully concrete state satisfying the entry precondition.
  claim [twenty-seven-is-not-a-cube]:
    <k> Call(Name("iscube"), Int(27)) => false </k>
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
