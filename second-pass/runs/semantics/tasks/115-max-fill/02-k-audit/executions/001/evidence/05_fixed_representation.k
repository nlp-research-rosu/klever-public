requires "verification.k"

// Independent validation module: no MAX-FILL-BRIDGES import.  It runs the
// same submitted AST on the ordinary rowVals/gridVals representation that is
// reduced solely by MAX-FILL-DATA plus the supplied MPY semantics.
module MAX-FILL-FIXED-REPRESENTATION
  imports MAX-FILL-DATA

  syntax Val ::= fixedFinalRow(GridRows, Val) [function, total]
  syntax Int ::= fixedFinalWater(GridRows, Int) [function, total]

  rule fixedFinalRow(.GridRows, V:Val) => V
  rule fixedFinalRow(gCons(IS:IntSeq, GS:GridRows), _V:Val)
    => fixedFinalRow(GS, list(rowVals(IS)))

  rule fixedFinalWater(.GridRows, W:Int) => W
  rule fixedFinalWater(gCons(IS:IntSeq, GS:GridRows), _W:Int)
    => fixedFinalWater(GS, rowSum(IS))

  syntax KItem ::= #runMaxFillFixed(GridRows, Int)
  rule <k> #runMaxFillFixed(GS:GridRows, C:Int)
        => #loadAll(
             Module(
               FuncDef(
                 "max_fill",
                 Params("grid", "capacity"),
                 Assign(Name("result"), Int(0))
                 Assign(Name("row"), Int(0))
                 Assign(Name("water"), Int(0))
                 For(
                   Name("row"),
                   Name("grid"),
                   MAX_FILL_LOOP_BODY)
                 Return(Name("result")))))
           ~> Call(Name("max_fill"), list(gridVals(GS)), C)
           ...
       </k>
endmodule

module MAX-FILL-FIXED-REPRESENTATION-SPEC
  imports MAX-FILL-FIXED-REPRESENTATION

  claim [fixed-sum-fold]:
    <k> #sumAcc(list(rowVals(IS:IntSeq)), A:Int) ~> K:K
     => rowTotal(A, IS) ~> K
    </k>

  claim [fixed-fill-loop]:
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
        "row" |-> fixedFinalRow(GS, RV)
        "water" |-> fixedFinalWater(GS, W),
        parent(0))
    </scopes>
    requires C >Int 0

  claim [fixed-max-fill-correct]:
    <k> #runMaxFillFixed(GS:GridRows, C:Int)
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
