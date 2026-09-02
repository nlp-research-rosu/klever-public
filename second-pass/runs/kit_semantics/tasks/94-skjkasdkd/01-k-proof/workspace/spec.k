requires "verification.k"

module SPEC
  imports VERIFICATION

  // The primality loop preserves whether the already-visited divisor prefix
  // was clean and appends the exact remaining divisor predicate.
  claim [prime-loop]:
    <k>
      #while(
        Compare(Name("divisor"), CmpOp("<", Name("value"))),
        primeLoopBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ( "lst"       |-> list(ALL:ValSeq)
          "largest"   |-> M:Int
          "value"     |-> V:Val
          "candidate" |-> (C:Bool
                           => C andBool
                              primeTail(projectIntTotal(V), D))
          "divisor"   |-> (D:Int
                           => maxInt(D, projectIntTotal(V))) ),
        parent(0))
      ...
    </scopes>
    requires isInt(V)
      andBool D >=Int 2

  // Symbolic, unbounded traversal of the input list.  The three scratch
  // variables are intentionally existential on exit; only largest is
  // observable after this loop.
  claim [scan-loop]:
    <k>
      #loop(list(VS:ValSeq), Name("value"), scanBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ( "lst"       |-> list(ALL:ValSeq)
          "largest"   |-> (M:Int => largestPrime(VS, M))
          "value"     |-> (V0:Val => ?VF:Val)
          "candidate" |-> (C0:Bool => ?CF:Bool)
          "divisor"   |-> (D0:Int => ?DF:Int) ),
        parent(0))
      ...
    </scopes>
    requires M >=Int 0
      andBool allInts(VS)

  // Decimal decomposition invariant for every nonnegative value produced by
  // the list scan.
  claim [digit-loop]:
    <k>
      #while(
        Compare(Name("largest"), CmpOp(">", Int(0))),
        digitLoopBody)
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ( "lst"       |-> list(ALL:ValSeq)
          "largest"   |-> (N:Int => 0)
          "value"     |-> V:Val
          "candidate" |-> C:Bool
          "divisor"   |-> D:Int
          "total"     |-> (T:Int => T +Int digitSum(N)) ),
        parent(0))
      ...
    </scopes>
    requires N >=Int 0

  // Required target theorem: load the exact translated definition, invoke its
  // required entry point, and cover every finite ValSeq whose elements are Int.
  claim [target]:
    <k>
      #loadAll(
        Module(
          FuncDef("skjkasdkd", Params("lst"), targetBody)))
      ~> Call(Name("skjkasdkd"), list(VS:ValSeq))
      => digitSum(largestPrime(VS, 0))
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        .Map
        => "skjkasdkd" |->
             closureVal(("lst", .ParamNames), targetBody, 0),
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
    requires allInts(VS)
endmodule
