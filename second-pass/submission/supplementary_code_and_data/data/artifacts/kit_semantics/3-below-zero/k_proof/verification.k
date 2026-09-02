requires "verification-base.k"

module VERIFICATION
  imports VERIFICATION-BASE

  // Exact top-level call bridge.  The complete fixed-semantics transition is
  // the composition of CONNECTION-SPEC.call-prefix-connection and
  // CONNECTION-SPEC.loop-connection, both proved without importing this file.
  // MPY-CALL's generic Call rule is [owise], so this rule is selected only in
  // the exact configuration below; all other calls use the supplied semantics.
  rule
    <k> Call(Name("below_zero"), list(INPUT:ValSeq))
      => belowFrom(0, INPUT) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "below_zero" |-> closureVal(
          "operations", .ParamNames,
          Assign(Name("balance"), Int(0))
          Assign(Name("operation"), Int(0))
          For(Name("operation"), Name("operations"),
            AugAssign(Name("balance"), "+", Name("operation"))
            If(Compare(Name("balance"), CmpOp("<", Int(0))),
              Return(Bool(true)), .Stmts))
          Return(Bool(false)),
          0),
        parent(-1))
      -1 |-> BUILTINS:Scope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(INPUT)
endmodule
