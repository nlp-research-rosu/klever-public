requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [digit-sum-loop]:
    <k>
      #while(
        Compare(Name("number"), CmpOp(">=", Int(10))),
        digitSumLoopBody
      ) => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      ...
      1 |-> scope(
        "number" |-> (N:Int => leadingDigit(N))
        "sign"   |-> SIGN:Int
        "total"  |-> (S:Int => lowerDigitSumAcc(N, S)),
        parent(0))
      ...
    </scopes>
    requires N >=Int 0

  claim [digit-sum-function]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("digit_sum"), (N:Int, .Exprs))
      => signedDigitSum(N)
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
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [order-by-points]:
    <k>
      #loadAll(solutionModule)
      ~> Call(Name("order_by_points"), (list(VS:ValSeq), .Exprs))
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
    <heap> .Map => 0 |-> list(expectedOrder(VS)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allInts(VS)
endmodule
