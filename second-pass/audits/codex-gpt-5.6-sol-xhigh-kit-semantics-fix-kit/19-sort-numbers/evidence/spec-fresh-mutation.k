requires "verification.k"

module SPEC-FRESH-MUTATION
  imports VERIFICATION

  claim [false-hyphen-separator]:
    <k>
      Call(Name("sort_numbers"), str(CS:IntSeq))
      => str(joinCodes(
           iCons(45, .IntSeq),
           sortKeyVS(
             splitWS(CS, .IntSeq, .ValSeq),
             boundMethodV(numberOrder, "index"))))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "sort_numbers" |-> closureVal(
          "numbers", .ParamNames,
          Assign(
            Name("order"),
            TupleExpr(
              Str("zero"), Str("one"), Str("two"), Str("three"), Str("four"),
              Str("five"), Str("six"), Str("seven"), Str("eight"), Str("nine")))
          Return(
            Call(
              Attribute(Str(" "), "join"),
              Call(
                Name("sorted"),
                Call(Attribute(Name("numbers"), "split"), .Exprs),
                KwArg("key", Attribute(Name("order"), "index"))))),
          0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(splitWS(CS, .IntSeq, .ValSeq))
         1 |-> list(sortKeyVS(
           splitWS(CS, .IntSeq, .ValSeq),
           boundMethodV(numberOrder, "index")))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validNumeralTokens(splitWS(CS, .IntSeq, .ValSeq))
endmodule
