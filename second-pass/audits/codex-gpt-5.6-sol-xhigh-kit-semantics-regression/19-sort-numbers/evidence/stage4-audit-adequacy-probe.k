requires "verification.k"

module AUDIT-ADEQUACY-PROBE
  imports VERIFICATION

  // This is true of Python and of MPY-CONCRETE, but intentionally asks whether
  // the Haskell proof theory itself can derive the concrete HumanEval result
  // instead of retaining the supplied opaque sortKeyVS term.
  claim [concrete-example-result]:
    <k> Call(
          Name("sort_numbers"),
          (str(joinCodes(
                 iCons(32, .IntSeq),
                 vCons(str(strToCodes("three")),
                   vCons(str(strToCodes("one")),
                     vCons(str(strToCodes("five")), .ValSeq))))),
           .Exprs))
      => str(strToCodes("one three five")) </k>
    <env> 0 </env>
    <scopes> 0  |-> scope("sort_numbers" |-> sortNumbersFunction, parent(-1))
             -1 |-> builtinsScope </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map
      => 0 |-> list(
           vCons(str(strToCodes("three")),
             vCons(str(strToCodes("one")),
               vCons(str(strToCodes("five")), .ValSeq))))
         1 |-> list(
           vCons(str(strToCodes("one")),
             vCons(str(strToCodes("three")),
               vCons(str(strToCodes("five")), .ValSeq)))) </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
