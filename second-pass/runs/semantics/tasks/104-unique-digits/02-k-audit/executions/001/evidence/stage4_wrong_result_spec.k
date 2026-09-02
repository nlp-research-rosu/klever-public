requires "stage4-wrong-oracle-verification.k"

module UNIQUE-DIGITS-WRONG-RESULT
  imports UNIQUE-DIGITS-WRONG-ORACLE

  // False of the real program: on [2], this claims the filtered list contains 2.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "_all_digits_odd",
            Params("n"),
            oddDigitsBody)
          FuncDef(
            "unique_digits",
            Params("x"),
            uniqueDigitsBody)))
      ~> Call(Name("unique_digits"), list(vCons(2, .ValSeq)))
    =>
      ref(1)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
    =>
      0 |-> scope(
        "_all_digits_odd" |->
          closureVal(("n", .ParamNames), oddDigitsBody, 0)
        "unique_digits" |->
          closureVal(("x", .ParamNames), uniqueDigitsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(2, .ValSeq))
      1 |-> list(sortVS(vCons(2, .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
