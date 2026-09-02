requires "verification.k"

module AUDIT-NONVACUITY
  imports VERIFICATION

  // Satisfying input: [1, 11, -1, -11, -12].
  // Correct output under the supplied sortKeyVS contract:
  // [-1, -11, 1, -12, 11].
  // This mutation requires its reverse [11, -12, 1, -11, -1], which is false.
  claim [reversed-target-result]:
    <k>
      #loadAll(solutionModule)
      ~> Call(
           Name("order_by_points"),
           (list(
             vCons(1,
             vCons(11,
             vCons(-1,
             vCons(-11,
             vCons(-12, .ValSeq)))))), .Exprs))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
        0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0 |-> scope(
          "digit_sum" |-> closureVal("number", digitSumBody, 0)
          "order_by_points" |->
            closureVal("nums", orderByPointsBody, 0),
          parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        revVS(
          expectedOrder(
            vCons(1,
            vCons(11,
            vCons(-1,
            vCons(-11,
            vCons(-12, .ValSeq))))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
