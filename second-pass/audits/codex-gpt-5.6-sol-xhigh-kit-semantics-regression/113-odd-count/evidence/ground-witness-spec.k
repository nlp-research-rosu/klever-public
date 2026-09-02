requires "verification.k"

module AUDITOR-GROUND-WITNESS-SPEC
  imports VERIFICATION

  claim [entry-empty]:
    <k> #loadAll(oddCountModule)
         ~> Call(Name("odd_count"), list(.ValSeq))
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
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires digitStrings(.ValSeq)

  claim [entry-documented-example]:
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
               "the number of odd elements 4n the str4ng 4 of the 4nput.")),
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
