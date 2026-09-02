requires "verification.k"

module ISCUBE-SPEC-VACUITY-AUDIT
  imports ISCube-VERIFICATION

  // Fresh false-postcondition mutation. The precondition is satisfiable at
  // N=1, where the submitted extended theory evaluates iscube(1) to true.
  // Changing the required result to false must leave an unmet obligation.
  claim [positive-cube-wrong-result]:
    <k>
      Call(Name("iscube"),
        (Int(N *Int N *Int N), .Exprs))
      => false
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("iscube" |-> iscubeClosure, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires N >=Int 0
endmodule
