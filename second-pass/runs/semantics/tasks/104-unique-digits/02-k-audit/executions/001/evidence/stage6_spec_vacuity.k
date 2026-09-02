requires "verification.k"

module UNIQUE-DIGITS-FALSE-RETURN-REF
  imports UNIQUE-DIGITS-VERIFICATION

  // Fresh false mutation: the real function always returns the separately
  // allocated sorted list at ref(1), never its mutable accumulator at ref(0).
  // The empty input is a concrete state satisfying positiveInts(.ValSeq).
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
