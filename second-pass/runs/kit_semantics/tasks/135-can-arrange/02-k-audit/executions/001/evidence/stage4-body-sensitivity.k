requires "verification.k"

module REVIEWER-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed function body is materially changed to `return 0`.
  // On the satisfying empty input, the original postcondition is -1.
  claim [mutated-body-wrong-original-result]:
    <k>
      (#loadAll(
        Module(
          FuncDef(
            "can_arrange",
            Params("arr"),
            Return(Int(0))
            .Stmts)
          .Stmts))
      ~> Call(Name("can_arrange"), list(.ValSeq))
      => -1)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        .Map
        => "can_arrange" |->
             closureVal(
               "arr",
               .ParamNames,
               Return(Int(0))
               .Stmts,
               0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
