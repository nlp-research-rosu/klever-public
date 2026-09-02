requires "verification.k"

module CONTEXT-SENSITIVITY-BASE
  imports MPY-VERIFICATION

  // The admitted summary matches only Return(false). With this observable
  // Return(true) suffix it must not match; fixed execution returns true.
  claim
    <k> #loop(
          list(asValSeq(.IntVals)),
          Name("operation"),
          belowZeroLoopBody)
         ~> (Return(Bool(true)) .Stmts) ~> #endcall
      => true
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "operations" |-> list(asValSeq(.IntVals))
        "operation"  |-> 0
        "balance"    |-> 0,
        parent(0))
      =>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
