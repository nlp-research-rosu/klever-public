requires "verification.k"

module FRESH-FALSE-SPEC
  imports VERIFICATION

  // Preserve the genuine loop circularity so the mutation reaches the final
  // result obligation rather than attempting unbounded concrete unfolding.
  claim [fresh-loop-invariant]:
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

  // Deliberately false: [1,2] satisfies allInts but returns 2, not noneV.
  claim [fresh-false-result]:
    <k> #loadAll(solutionProgram)
         ~> Call(Name("next_smallest"), (list(VS:ValSeq), .Exprs))
        => noneV </k>
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
