requires "verification.k"

module BODY-SENSITIVITY
  imports MPY-VERIFICATION

  // Deliberately changes balance += operation to balance -= operation.
  // For the satisfying ground state B=0, remaining=[1], fixed execution
  // returns true, while the original prefixBelow(0,[1]) is false.
  claim
    <k> #loop(
          list(asValSeq(intCons(1, .IntVals))),
          Name("operation"),
          AugAssign(Name("balance"), "-", Name("operation"))
          If(Compare(Name("balance"), CmpOp("<", Int(0))),
            Return(Bool(true)) .Stmts,
            .Stmts))
         ~> (Return(Bool(false)) .Stmts) ~> #endcall
      => prefixBelow(0, intCons(1, .IntVals))
    </k>
    <env> 1 => 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      1 |-> scope(
        "operations" |-> list(asValSeq(intCons(1, .IntVals)))
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
