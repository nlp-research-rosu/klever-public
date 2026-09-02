requires "real-verification.k"

module REAL-UNIVERSAL-SPEC
  imports REAL-VERIFICATION

  claim [real-sum-fold]:
    <k> #sumAcc(list(rowVals(IS:IntSeq)), A:Int) ~> K:K
     => rowTotal(A, IS) ~> K
    </k>

  claim [real-fill-loop]:
    <k> #loop(
          list(gridVals(GS:GridRows)),
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
        "grid" |-> list(gridVals(INPUT:GridRows))
        "capacity" |-> C:Int
        "result" |-> A:Int
        "row" |-> RV:Val
        "water" |-> W:Int,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope("max_fill" |-> F, parent(-1))
      1 |-> scope(
        "grid" |-> list(gridVals(INPUT))
        "capacity" |-> C
        "result" |-> fillTotal(A, GS, C)
        "row" |-> realFinalRow(GS, RV)
        "water" |-> realFinalWater(GS, W),
        parent(0))
    </scopes>
    requires C >Int 0

  claim [real-max-fill-correct]:
    <k> #runMaxFillReal(GS:GridRows, C:Int)
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
