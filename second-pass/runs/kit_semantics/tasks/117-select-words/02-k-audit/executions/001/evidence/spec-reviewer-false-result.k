requires "verification.k"

module REVIEWER-FALSE-RESULT
  imports VERIFICATION

  // Fresh false obligation.  For s = "a b" and n = 1, the real result is
  // ["b"]; this mutation demands ["a"].
  claim [fresh-false-result]:
    <k>
      #loadAll(Module(
        FuncDef("select_words", Params("s", "n"), selectWordsBody)
        .Stmts))
      ~> Call(
           Name("select_words"),
           str(iCons(97, iCons(32, iCons(98, .IntSeq)))),
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
          closureVal(("s", "n", .ParamNames), selectWordsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(str(iCons(97, .IntSeq)), .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
