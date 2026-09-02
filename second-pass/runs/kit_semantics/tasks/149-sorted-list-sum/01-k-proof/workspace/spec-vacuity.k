requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: ["aa"] must survive, but this claims an empty result.
  claim [wrong-result]:
    <k>
      #loadAll(sortedListSumModule)
      ~> Call(
           Name("sorted_list_sum"),
           list(
             vCons(
               str(iCons(97, iCons(97, .IntSeq))),
               .ValSeq)))
      => ref(2)
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "sorted_list_sum"
                  |-> closureVal(
                        ("lst", .ParamNames),
                        sortedListSumBody,
                        0),
                  parent(-1)))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
             vCons(
               str(iCons(97, iCons(97, .IntSeq))),
               .ValSeq))
      1 |-> list(
             vCons(
               str(iCons(97, iCons(97, .IntSeq))),
               .ValSeq))
      2 |-> list(.ValSeq)
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
