requires "verification.k"

module REVIEWER-BODY-MUTATION
  imports VERIFICATION

  // Materially mutate the executed body: initialize count to 1.  For "b", 1
  // that program returns [], so the original literal ["b"] result must fail.
  claim [body-mutation]:
    <k>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"),
          Assign(Name("result"), ListExpr(.Exprs))
          Assign(Name("word"), Str(""))
          Assign(Name("count"), Int(1))
          Assign(Name("ch"), Str(""))
          For(Name("ch"), Name("s"), charLoopBody)
          afterCharLoop)))
      ~> Call(Name("select_words"), str(iCons(98, .IntSeq)), 1)
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
      0 |-> list(vCons(str(iCons(98, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
