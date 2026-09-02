requires "verification.k"

module SPEC
  imports VERIFICATION

  // Loop circularity: scanVS describes exactly the accumulator state after
  // consuming the arbitrary finite suffix VS.
  claim [loop-invariant]:
    <k> #loop(list(VS:ValSeq), Name("x"), nextSmallestLoopBody)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "lst" |-> list(ORIG:ValSeq)
        "found_smallest" |->
          (HA:Bool => scanFoundSmallest(scanVS(VS, A, HA, B, HB)))
        "found_second" |->
          (HB:Bool => scanFoundSecond(scanVS(VS, A, HA, B, HB)))
        "smallest" |->
          (A:Int => scanSmallest(scanVS(VS, A, HA, B, HB)))
        "second" |->
          (B:Int => scanSecond(scanVS(VS, A, HA, B, HB)))
        "x" |-> (X0:Int => lastInt(VS, X0)),
        parent(0)) ...
    </scopes>
    requires allInts(VS)

  // Whole-function target theorem, from exact name binding and exact body.
  claim [next-smallest]:
    <k> #loadAll(solutionProgram)
         ~> Call(Name("next_smallest"), (list(VS:ValSeq), .Exprs))
        => nextSmallestSpec(VS) </k>
    <env> 0 </env>
    <scopes>
      0 |-> (scope(.Map, parent(-1))
             => scope(
                  "next_smallest" |->
                    closureVal(("lst", .ParamNames), nextSmallestBody, 0),
                  parent(-1)))
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
