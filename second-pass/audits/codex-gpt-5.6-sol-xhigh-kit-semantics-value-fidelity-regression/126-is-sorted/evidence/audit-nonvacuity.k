requires "verification.k"

module AUDIT-NONVACUITY
  imports VERIFICATION

  // [0, 0] satisfies nonNegativeInts. Both the real program and the claimed
  // intendedSorted summary return true, so demanding false is meaningful.
  claim [pair-must-not-be-false]:
    <k>
      #loadAll(Module(
        FuncDef("is_sorted", Params("lst"), isSortedFunctionBody)
        .Stmts))
      ~> Call(
           Name("is_sorted"),
           list(vCons(0, vCons(0, .ValSeq))),
           .Exprs)
      =>
      false
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "is_sorted" |-> closureVal("lst", isSortedFunctionBody, 0),
          parent(-1))
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(sortVS(vCons(0, vCons(0, .ValSeq))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
