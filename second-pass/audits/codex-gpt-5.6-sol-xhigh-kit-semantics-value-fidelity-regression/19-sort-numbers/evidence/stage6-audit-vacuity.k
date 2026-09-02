requires "verification.k"

module AUDIT-VACUITY
  imports VERIFICATION

  // Fresh auditor mutation: prefix the actual symbolic result with '!'.
  // For the satisfying witness "three one five", this demands
  // "!one three five" instead of "one three five".
  claim [auditor-wrong-prefixed-result]:
    <k> #loadAll(solutionProgram)
         ~> Call(
              Name("sort_numbers"),
              (str(strToCodes("three one five")), .Exprs))
      => str(
           iCons(
             33,
             sortNumbersResult(strToCodes("three one five")))) </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
        => scope(
             .Map
               [ "_number_rank" <- numberRankClosure ]
               [ "sort_numbers" <- sortNumbersClosure ],
             parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
                  splitWS(
                    strToCodes("three one five"),
                    .IntSeq,
                    .ValSeq))
         1 |-> list(
                  sortKeyVS(
                    splitWS(
                      strToCodes("three one five"),
                      .IntSeq,
                      .ValSeq),
                    numberRankClosure))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validNumberInput(strToCodes("three one five"))
endmodule
