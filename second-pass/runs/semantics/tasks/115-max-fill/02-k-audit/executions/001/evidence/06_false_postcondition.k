requires "verification.k"

module MAX-FILL-SPEC-VACUITY
  imports MAX-FILL-VERIFICATION

  claim [sum-fold-vacuity]:
    <k> #sumAcc(list(symRow(IS:IntSeq)), A:Int) ~> K:K
     => rowTotal(A, IS) ~> K
    </k>

  claim [fill-loop-vacuity]:
    <k> #loop(
          list(symGrid(GS:GridRows)),
          Name("row"),
          MAX_FILL_LOOP_BODY)
          ~> K:K
     => K
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope("max_fill" |-> F:Val, parent(-1))
      1 |-> scope(
        "grid" |-> list(symGrid(INPUT:GridRows))
        "capacity" |-> C:Int
        "result" |-> A:Int
        "row" |-> RV:Val
        "water" |-> W:Int,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope("max_fill" |-> F, parent(-1))
      1 |-> scope(
        "grid" |-> list(symGrid(INPUT))
        "capacity" |-> C
        "result" |-> fillTotal(A, GS, C)
        "row" |-> finalRow(GS, RV)
        "water" |-> finalWater(GS, W),
        parent(0))
    </scopes>
    requires C >Int 0

  // Deliberately false: every legitimate result is required to be one larger.
  // Satisfying witness: GS=.GridRows, C=1; execution returns 0, destination is 1.
  claim [max-fill-false-plus-one]:
    <k> #runMaxFill(GS:GridRows, C:Int)
     => maxFillSpec(GS, C) +Int 1
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      ?FINALSCOPES:Map
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires C >Int 0
endmodule
