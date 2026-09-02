requires "verification.k"

module AUDIT-FALSE-RESULT
  imports VERIFICATION

  // Fresh false mutation: [9,8,3] actually returns [3,8,9], but this claim
  // demands that the result at heap location 0 remain [9,8,3].
  claim [wrong-unchanged-result]:
    <k>
      #loadAll(Module(FuncDef("sort_even", Params("l"), sortEvenBody)))
      ~> Call(
           Name("sort_even"),
           list(vCons(9, vCons(8, vCons(3, .ValSeq)))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0 |-> scope(
          "sort_even" |-> closureVal("l", sortEvenBody, 0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      ( 0 |-> list(vCons(9, vCons(8, vCons(3, .ValSeq))))
        1 |-> list(vCons(9, vCons(3, .ValSeq)))
        2 |-> list(vCons(3, vCons(9, .ValSeq))) )
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
