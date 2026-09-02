requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated body: it omits `item not in result`, so [1, 1]
  // intersected with [1] returns [1, 1], not the original theorem's [1].
  claim [duplicate-mutant]:
    <k>
      #loadAll(Module(
        FuncDef(
          "common",
          Params("l1", "l2"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("item"), Int(0))
          For(
            Name("item"),
            Name("l1"),
            If(
              Compare(Name("item"), CmpOp("in", Name("l2"))),
              Expr(Call(
                Attribute(Name("result"), "append"),
                Name("item"))),
              .Stmts))
          Return(Call(Name("sorted"), Name("result"))))
      ))
      ~> Call(
           Name("common"),
           list(vCons(1, vCons(1, .ValSeq))),
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
          For(
            Name("item"),
            Name("l1"),
            If(
              Compare(Name("item"), CmpOp("in", Name("l2"))),
              Expr(Call(
                Attribute(Name("result"), "append"),
                Name("item"))),
              .Stmts))
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
