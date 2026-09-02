requires "verification.k"

module SPEC-BODY-SENSITIVITY-AUDIT
  imports VERIFICATION

  // The executed body has an empty loop body, but the post-state deliberately
  // retains the original program's [1] result obligation on input [1], [1].
  claim [empty-loop-body-cannot-prove-original-result]:
    <k>
      #loadAll(Module(
        FuncDef(
          "common",
          Params("l1", "l2"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("item"), Int(0))
          For(Name("item"), Name("l1"), .Stmts)
          Return(Call(Name("sorted"), Name("result"))))
      ))
      ~> Call(
           Name("common"),
           list(vCons(1, .ValSeq)),
           list(vCons(1, .ValSeq)))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0  |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0  |-> scope(
        "common" |-> closureVal(
          ("l1", "l2", .ParamNames),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("item"), Int(0))
          For(Name("item"), Name("l1"), .Stmts)
          Return(Call(Name("sorted"), Name("result"))),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(sortVS(vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
