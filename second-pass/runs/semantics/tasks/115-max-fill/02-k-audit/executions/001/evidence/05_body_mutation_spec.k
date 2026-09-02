requires "05_body_mutation_verification.k"

module MAX-FILL-BRIDGE-SPEC
  imports MAX-FILL-DATA

  // These finite claims justify every symbolic bridge in
  // MAX-FILL-BRIDGES directly from the supplied MPY rules.
  claim [bridge-sum-empty]:
    <k> #sumAcc(list(rowVals(.IntSeq)), A:Int) ~> K:K
     => #iterNext(list(.ValSeq)) ~> #sumCont(A) ~> K
    </k>

  claim [bridge-sum-step]:
    <k> #sumAcc(
          list(rowVals(iCons(I:Int, IS:IntSeq))),
          A:Int)
          ~> K:K
     => #iterNext(list(vCons(I, rowVals(IS))))
        ~> #sumCont(A)
        ~> K
    </k>

  claim [bridge-loop-empty]:
    <k> #loop(
          list(gridVals(.GridRows)),
          T:Expr,
          B:Stmts)
          ~> K:K
     => #iterNext(list(.ValSeq))
        ~> #loopStep(T, B)
        ~> K
    </k>

  claim [bridge-loop-step]:
    <k> #loop(
          list(gridVals(gCons(IS:IntSeq, GS:GridRows))),
          T:Expr,
          B:Stmts)
          ~> K:K
     => #iterNext(
          list(vCons(list(rowVals(IS)), gridVals(GS))))
        ~> #loopStep(T, B)
        ~> K
    </k>
endmodule

module MAX-FILL-SPEC
  imports MAX-FILL-VERIFICATION

  // Auxiliary induction: MPY's iterator-based sum agrees with rowSum.
  claim [sum-fold]:
    <k> #sumAcc(list(symRow(IS:IntSeq)), A:Int) ~> K:K
     => rowTotal(A, IS) ~> K
    </k>

  // Main loop invariant.  The frame's grid binding is part of M; capacity and
  // the accumulator are exposed so each iteration updates them symbolically.
  claim [fill-loop]:
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

  // Universal functional correctness of the loaded Python entry point.
  claim [max-fill-correct]:
    <k> #runMaxFill(GS:GridRows, C:Int)
     => maxFillSpec(GS, C)
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
