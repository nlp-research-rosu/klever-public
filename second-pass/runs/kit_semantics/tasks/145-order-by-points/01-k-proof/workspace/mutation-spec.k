requires "verification.k"

module MUTATION-SPEC
  imports VERIFICATION

  // Expected failure: replacing the real helper body by `return 0` must not
  // establish the connection theorem at the realizable witness 12.
  claim [digit-sum-body-mutation]:
    <k>
      #loadAll(
        Module(
          FuncDef("digit_sum", Params("number"), Return(Int(0)))
          FuncDef("order_by_points", Params("nums"), orderByPointsBody)))
      ~> Call(Name("digit_sum"), (Int(12), .Exprs))
      => signedDigitSum(12)
    </k>
    <env> 0 </env>
    <scopes>
        0 |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope
      =>
        0 |-> scope(
          "digit_sum" |->
            closureVal("number", Return(Int(0)), 0)
          "order_by_points" |->
            closureVal("nums", orderByPointsBody, 0),
          parent(-1))
        -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  // Expected failure: the prompt witness cannot satisfy a deliberately wrong
  // output sequence. This checks that the target result is constrained.
  claim [target-postcondition-mutation]:
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
        vCons(1,
        vCons(11,
        vCons(-1,
        vCons(-11,
        vCons(-12, .ValSeq))))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
