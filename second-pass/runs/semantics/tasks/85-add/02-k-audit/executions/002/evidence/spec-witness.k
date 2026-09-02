requires "/tmp/audit-work/85-add/verification.k"

module SPEC-WITNESS
  imports VERIFICATION

  claim [entry-witness]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("add"),
           (list(intVals(
             iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq))))
           )), .Exprs))
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

  claim [loop-precondition-witness]:
    <k>
      #loop(
        list(intVals(
          iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq))))
        )),
        Name("value"),
        addLoopBody)
      =>
      .K
    </k>
    <env> 1 </env>
    <scopes>
      1 |-> scope(
        ("lst" |-> list(intVals(
          iCons(4, iCons(2, iCons(6, iCons(7, .IntSeq))))
        )))
        ("total" |-> 0)
        ("odd_index" |-> false)
        ("value" |-> 0),
        parent(0))
      =>
      1 |-> scope(
        ("total" |-> 2)
        ?FINALBINDINGS:Map,
        parent(0))
    </scopes>
endmodule
