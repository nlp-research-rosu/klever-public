requires "verification.k"

module AUDITOR-FALSE-RESULT-MUTATION
  imports VERIFICATION

  // False for the satisfying input ["1234567"]: its odd-digit count is 4,
  // while this mutation requires the observable returned heap string to use 5.
  claim [wrong-documented-result]:
    <k> #loadAll(oddCountModule)
         ~> Call(
               Name("odd_count"),
               list(vCons(str(strToCodes("1234567")), .ValSeq)))
      => ref(0) </k>
    <env> 0 </env>
    <scopes>
        0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      => 0 |-> scope(.Map [ "odd_count" <- closureVal("lst", oddCountBody, 0) ],
                      parent(-1))
         -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(
           vCons(
             str(strToCodes(
               "the number of odd elements 5n the str5ng 5 of the 5nput.")),
             .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitStrings(
               vCons(str(strToCodes("1234567")), .ValSeq))
endmodule
