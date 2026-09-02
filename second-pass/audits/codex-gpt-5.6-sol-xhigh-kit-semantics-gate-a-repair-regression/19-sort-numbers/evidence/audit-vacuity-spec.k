requires "verification.k"

module AUDIT-VACUITY-SPEC
  imports VERIFICATION

  // Fresh false result mutation.  "three one five" satisfies the original
  // domain, while both Python implementations and concrete K return
  // "one three five", not the reversed string below.
  claim [wrong-ground-result]:
    <k> #loadAll(solutionModule())
         ~> Call(
              Name("sort_numbers"),
              str(strToCodes("three one five")))
      => str(strToCodes("five three one"))
    </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    =>
      solutionScopes()
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
    =>
      (0 |-> list(
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
                  numberValueClosure())))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires validNumberInput(strToCodes("three one five"))
endmodule
