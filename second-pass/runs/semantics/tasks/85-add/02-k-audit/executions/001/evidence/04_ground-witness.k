requires "verification.k"

module GROUND-WITNESS
  imports VERIFICATION

  claim [entry-documented-example]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("add"),
           (list(intVals(iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq)))))), .Exprs))
      =>
      2
    </k>
    <scopes>
      (0 |-> scope(.Map, parent(-1)))
      (-1 |-> builtinsScope)
      =>
      ?FINALSCOPES:Map
    </scopes>
    <env> 0 </env>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [loop-satisfying-state]:
    <k>
      #loop(
        list(intVals(iCons(2, iCons(3, .IntSeq)))),
        Name("value"),
        addLoopBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      (1 |-> scope(
        ("lst" |-> list(.ValSeq))
        ("total" |-> 5)
        ("odd_index" |-> true)
        ("value" |-> 99),
        parent(0)))
      (-1 |-> builtinsScope)
      =>
      (1 |-> scope(
        ("lst" |-> list(.ValSeq))
        ("total" |-> 7)
        ("odd_index" |-> true)
        ("value" |-> 3),
        parent(0)))
      (-1 |-> builtinsScope)
    </scopes>
endmodule
