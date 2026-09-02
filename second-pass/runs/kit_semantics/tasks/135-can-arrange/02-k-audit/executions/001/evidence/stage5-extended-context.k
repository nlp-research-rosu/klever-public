requires "verification.k"

module REVIEWER-EXTENDED-CONTEXT
  imports VERIFICATION

  // With the bridge enabled, the same observable continuation must remain.
  claim [extended-observable-context]:
    <k>
      If(
        Compare(Int(2), CmpOp(">=", Int(1))),
        Assign(Name("x"), Int(7)),
        Assign(Name("x"), Int(9)))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope("x" |-> (0 => 7), parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
