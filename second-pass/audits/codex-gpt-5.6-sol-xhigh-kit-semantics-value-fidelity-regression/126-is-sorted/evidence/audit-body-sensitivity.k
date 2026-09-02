requires "verification.k"

module AUDIT-BODY-SENSITIVITY
  imports VERIFICATION

  // This is deliberately not isSortedFunctionBody. It returns false without
  // sorting. If the entry proof bypassed the loaded body, this true target
  // could incorrectly inherit the original empty-list result.
  claim [changed-body-must-not-inherit-summary]:
    <k>
      #loadAll(Module(
        FuncDef(
          "is_sorted",
          Params("lst"),
          Assign(Name("result"), Bool(false))
          Return(Name("result"))
          .Stmts)
        .Stmts))
      ~> Call(Name("is_sorted"), list(.ValSeq), .Exprs)
      =>
      true
    </k>
    <env> 0 </env>
    <scopes>
      ( -1 |-> builtinsScope
        0 |-> scope(.Map, parent(-1))
      )
      =>
      ( -1 |-> builtinsScope
        0 |-> scope(
          "is_sorted" |->
            closureVal(
              "lst",
              Assign(Name("result"), Bool(false))
              Return(Name("result"))
              .Stmts,
              0),
          parent(-1))
      )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
