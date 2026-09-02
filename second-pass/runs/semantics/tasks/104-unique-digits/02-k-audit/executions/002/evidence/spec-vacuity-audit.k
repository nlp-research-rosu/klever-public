requires "verification.k"

module UNIQUE-DIGITS-VACUITY-AUDIT
  imports UNIQUE-DIGITS-VERIFICATION

  // Fresh false mutation: the source allocates the accumulator at ref(0) and
  // the sorted return list at ref(1), so requiring the returned value ref(0)
  // is false. INPUT = vCons(1, .ValSeq) satisfies the unchanged precondition.
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
      ~> Call(Name("unique_digits"), list(INPUT:ValSeq))
    =>
      ref(0)
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
      0 |-> list(filterOddAcc(.ValSeq, INPUT))
      1 |-> list(sortVS(filterOddAcc(.ValSeq, INPUT)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires positiveInts(INPUT)
endmodule
