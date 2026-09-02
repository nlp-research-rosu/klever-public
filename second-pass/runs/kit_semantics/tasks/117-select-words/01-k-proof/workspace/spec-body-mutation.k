requires "spec.k"

module SPEC-BODY-MUTATION
  imports SPEC

  // Gate A body-sensitivity probe: changing count's initialization from 0 to
  // 1 must invalidate the original postcondition for s = "b", n = 1.
  claim [mutated-body]:
    <k>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("word"), Str(""))
          Assign(Name("count"), Int(1))
          Assign(Name("ch"), Str(""))
          For(Name("ch"), Name("s"), charLoopBody)
          afterCharLoop)))
      ~> Call(
           Name("select_words"),
           str(iCons(98, .IntSeq)),
           1)
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        =>
        "select_words" |->
          closureVal(
            ("s", "n", .ParamNames),
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(Name("word"), Str(""))
            Assign(Name("count"), Int(1))
            Assign(Name("ch"), Str(""))
            For(Name("ch"), Name("s"), charLoopBody)
            afterCharLoop,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        selectScan(iCons(98, .IntSeq), 1, .IntSeq, 0, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
