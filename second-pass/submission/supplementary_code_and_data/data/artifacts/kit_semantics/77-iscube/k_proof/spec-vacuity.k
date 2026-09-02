requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  // Deliberately false for the satisfiable witness INPUT = 8.
  claim [iscube-eight-is-false]:
    <k> Call(Name("iscube"), Int(8)) => false </k>
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
