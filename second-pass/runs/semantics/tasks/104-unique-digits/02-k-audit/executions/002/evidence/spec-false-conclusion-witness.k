requires "witness-verification.k"

module UNIQUE-DIGITS-FALSE-CONCLUSION-WITNESS
  imports UNIQUE-DIGITS-FALSE-WITNESS

  // The mutated helper returns false, so real execution on [1] returns [].
  // The candidate loop bridge skips that binding and proves the false [1]
  // heap result once the intended, true ground meanings of oddDigits/sortVS
  // are supplied.
  claim
    <k>
      #loadAll(
        Module(
          FuncDef(
            "_all_digits_odd",
            Params("n"),
            Return(Bool(false)))
          FuncDef(
            "unique_digits",
            Params("x"),
            uniqueDigitsBody)))
      ~> Call(
           Name("unique_digits"),
           list(vCons(1, .ValSeq)))
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
          closureVal(("n", .ParamNames), Return(Bool(false)) .Stmts, 0)
        "unique_digits" |->
          closureVal(("x", .ParamNames), uniqueDigitsBody, 0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      0 |-> list(vCons(1, .ValSeq))
      1 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
