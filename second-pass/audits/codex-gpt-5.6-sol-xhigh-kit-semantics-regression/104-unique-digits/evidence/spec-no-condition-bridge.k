requires "audit-no-condition-bridge.k"

module NO-CONDITION-BRIDGE-GROUND-SPEC
  imports AUDIT-NO-CONDITION-BRIDGE

  claim [accepted-one]:
    <k> #loadAll(uniqueDigitsModule)
        ~> Call(Name("unique_digits"),
             (list(intsToVals(iCons(1, .IntSeq))), .Exprs))
        => ref(1) </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("unique_digits" |-> uniqueDigitsClosure, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => (0 |-> list(vCons(1, .ValSeq))
          1 |-> list(sortVS(vCons(1, .ValSeq))))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [rejected-two]:
    <k> #loadAll(uniqueDigitsModule)
        ~> Call(Name("unique_digits"),
             (list(intsToVals(iCons(2, .IntSeq))), .Exprs))
        => ref(1) </k>
    <env> 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
      =>
      (0 |-> scope("unique_digits" |-> uniqueDigitsClosure, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => (0 |-> list(.ValSeq)
          1 |-> list(sortVS(.ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
