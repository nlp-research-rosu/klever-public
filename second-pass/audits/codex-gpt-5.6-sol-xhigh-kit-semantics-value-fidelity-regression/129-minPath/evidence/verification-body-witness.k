requires "reference-semantics/semantics.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX

  syntax Stmts ::= "FIND-ONE-BODY" [macro]
  rule FIND-ONE-BODY
    => If(
         Compare(Name("value"), CmpOp("==", Int(1))),
         Assign(Name("answer"), Name("col_index")) .Stmts,
         .Stmts)
       Assign(
         Name("col_index"),
         BinOp("+", Name("col_index"), Int(1)))
       .Stmts

  syntax Stmts ::= "FIND-ONE-FUNCTION-BODY" [macro]
  rule FIND-ONE-FUNCTION-BODY
    => Assign(Name("col_index"), Int(0))
       Assign(Name("value"), Int(0))
       Assign(Name("answer"), UnaryOp("-", Int(1)))
       For(Name("value"), Name("row"), FIND-ONE-BODY)
       Return(Name("answer"))
       .Stmts

  syntax Stmts ::= "LOCATE-ONE-BODY" [macro]
  rule LOCATE-ONE-BODY
    => Assign(
         Name("found_col"),
         Call(Name("find_one"), Name("row")))
       If(
         Compare(Name("found_col"), CmpOp(">=", Int(0))),
         Assign(Name("one_row"), Name("row_index"))
         Assign(Name("one_col"), Name("found_col"))
         .Stmts,
         .Stmts)
       Assign(
         Name("row_index"),
         BinOp("+", Name("row_index"), Int(1)))
       .Stmts

  syntax Stmts ::= "LOCATE-ONE-FUNCTION-BODY" [macro]
  rule LOCATE-ONE-FUNCTION-BODY
    => Assign(Name("row_index"), Int(0))
       Assign(Name("row"), Int(0))
       Assign(Name("one_row"), Int(0))
       Assign(Name("one_col"), Int(0))
       Assign(Name("found_col"), UnaryOp("-", Int(1)))
       For(Name("row"), Name("grid"), LOCATE-ONE-BODY)
       Return(TupleExpr(Name("one_row"), Name("one_col")))
       .Stmts

  syntax Stmts ::= "SCAN-ROW-BODY" [macro]
  rule SCAN-ROW-BODY
    => If(
         Compare(
           BinOp(
             "+",
             Call(
               Name("abs"),
               BinOp("-", Name("row_index"), Name("one_row"))),
             Call(
               Name("abs"),
               BinOp("-", Name("col_index"), Name("one_col")))),
           CmpOp("==", Int(1))),
         Assign(
           Name("neighbor"),
           Call(Name("min"), Name("neighbor"), Name("value")))
         .Stmts,
         .Stmts)
       Assign(
         Name("col_index"),
         BinOp("+", Name("col_index"), Int(1)))
       .Stmts

  syntax Stmts ::= "SCAN-ROW-FUNCTION-BODY" [macro]
  rule SCAN-ROW-FUNCTION-BODY
    => Assign(Name("col_index"), Int(0))
       Assign(Name("value"), Int(0))
       For(Name("value"), Name("row"), SCAN-ROW-BODY)
       Return(Name("neighbor"))
       .Stmts

  syntax Stmts ::= "FIND-NEIGHBOR-BODY" [macro]
  rule FIND-NEIGHBOR-BODY
    => Assign(
         Name("neighbor"),
         Call(
           Name("scan_row"),
           Name("row"),
           Name("row_index"),
           Name("one_row"),
           Name("one_col"),
           Name("neighbor")))
       Assign(
         Name("row_index"),
         BinOp("+", Name("row_index"), Int(1)))
       .Stmts

  syntax Stmts ::= "FIND-NEIGHBOR-FUNCTION-BODY" [macro]
  rule FIND-NEIGHBOR-FUNCTION-BODY
    => Return(Int(999))
       .Stmts

  syntax Stmts ::= "RESULT-BODY" [macro]
  rule RESULT-BODY
    => If(
         Compare(BinOp("%", Name("step"), Int(2)), CmpOp("==", Int(0))),
         Expr(Call(Attribute(Name("result"), "append"), Int(1))) .Stmts,
         Expr(Call(Attribute(Name("result"), "append"), Name("neighbor"))) .Stmts)
       .Stmts

  syntax Stmts ::= "BUILD-PATH-FUNCTION-BODY" [macro]
  rule BUILD-PATH-FUNCTION-BODY
    => Assign(Name("result"), ListExpr(.Exprs))
       Assign(Name("step"), Int(0))
       For(
         Name("step"),
         Call(Name("range"), Name("k")),
         RESULT-BODY)
       Return(Name("result"))
       .Stmts

  syntax Stmts ::= "MINPATH-FUNCTION-BODY" [macro]
  rule MINPATH-FUNCTION-BODY
    => Assign(
         TupleExpr(Name("one_row"), Name("one_col")),
         Call(Name("locate_one"), Name("grid")))
       Assign(
         Name("neighbor"),
         Call(
           Name("find_neighbor"),
           Name("grid"),
           Name("one_row"),
           Name("one_col")))
       Return(Call(Name("build_path"), Name("k"), Name("neighbor")))
       .Stmts
endmodule

module VERIFICATION
  imports MPY
  imports VERIFICATION-SYNTAX

  syntax Bool ::= intsOnly(ValSeq) [function, total]
  rule intsOnly(.ValSeq) => true
  rule intsOnly(vCons(V:Val, VS))
    => isInt(V) andBool intsOnly(VS)

  rule applyCmp("==", V:Val, I:Int) => {V}:>Int ==Int I
    requires isInt(V)

  rule minVals(I:Int, (V:Val, .Vals))
    => minInt(I, {V}:>Int)
    requires isInt(V)
    [simplification]

  syntax ValSeq ::= rowContents(Val) [function, total]
  rule rowContents(list(VS)) => VS
  rule rowContents(_:Val) => .ValSeq [owise]

  syntax Bool ::= isIntList(Val) [function, total]
  rule isIntList(list(VS)) => intsOnly(VS)
  rule isIntList(_:Val) => false [owise]

  rule intsOnly(rowContents(V:Val)) => true
    requires isIntList(V)
    [simplification]

  syntax Bool ::= intRows(ValSeq) [function, total]
  rule intRows(.ValSeq) => true
  rule intRows(vCons(V, VS)) => isIntList(V) andBool intRows(VS)

  rule <k> For(T:Expr, V:Val, BODY:Stmts)
        => For(T, list(rowContents(V)), BODY) ... </k>
    requires isIntList(V)
    [priority(35)]

  rule <k> Call(Name("find_one"), (Name("row"), .Exprs))
        => foundCol(ROW) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "grid" |-> _GRID:Val
           "row_index" |-> _ROW_INDEX:Val
           "row" |-> ROW:Val
           "one_row" |-> _ONE_ROW:Val
           "one_col" |-> _ONE_COL:Val
           "found_col" |-> _FOUND_COL:Val,
           parent(0))
         0 |-> scope(
           "find_one" |->
             closureVal(("row", .ParamNames),
                        FIND-ONE-FUNCTION-BODY,
                        0)
           MODULE:Map,
           parent(-1))
         ...
       </scopes>
    requires isIntList(ROW)
      andBool notBool ("find_one" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
    [priority(35)]

  rule <k> Call(
          Name("scan_row"),
          (Name("row"),
           Name("row_index"),
           Name("one_row"),
           Name("one_col"),
           Name("neighbor"),
           .Exprs))
        => scanNeighbor(
             rowContents(ROW),
             0,
             ROW_INDEX,
             ONE_ROW,
             ONE_COL,
             NEIGHBOR) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "grid" |-> _GRID:Val
           "one_row" |-> ONE_ROW:Int
           "one_col" |-> ONE_COL:Int
           "n" |-> _N:Val
           "neighbor" |-> NEIGHBOR:Int
           "row_index" |-> ROW_INDEX:Int
           "row" |-> ROW:Val,
           parent(0))
         0 |-> scope(
           "scan_row" |->
             closureVal(
               ("row", "row_index", "one_row", "one_col", "neighbor",
                .ParamNames),
               SCAN-ROW-FUNCTION-BODY,
               0)
           MODULE:Map,
           parent(-1))
         ...
       </scopes>
    requires isIntList(ROW)
      andBool notBool ("scan_row" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
    [priority(35)]

  rule <k> Call(Name("locate_one"), (Name("grid"), .Exprs))
        => tuple(
             vCons(
               locateRow(GRID, 0, 0),
               vCons(locateCol(GRID, 0), .ValSeq))) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "grid" |-> list(GRID:ValSeq)
           "k" |-> _K:Val,
           parent(0))
         0 |-> scope(
           "locate_one" |->
             closureVal(
               ("grid", .ParamNames),
               LOCATE-ONE-FUNCTION-BODY,
               0)
           MODULE:Map,
           parent(-1))
         ...
       </scopes>
    requires intRows(GRID)
      andBool notBool ("locate_one" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
    [priority(35)]

  rule <k> Call(
          Name("find_neighbor"),
          (Name("grid"), Name("one_row"), Name("one_col"), .Exprs))
        => scanGridNeighbor(
             GRID,
             0,
             ONE_ROW,
             ONE_COL,
             vsLen(GRID) *Int vsLen(GRID)) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "grid" |-> list(GRID:ValSeq)
           "k" |-> _K:Val
           "one_row" |-> ONE_ROW:Int
           "one_col" |-> ONE_COL:Int,
           parent(0))
         0 |-> scope(
           "find_neighbor" |->
             closureVal(
               ("grid", "one_row", "one_col", .ParamNames),
               FIND-NEIGHBOR-FUNCTION-BODY,
               0)
           MODULE:Map,
           parent(-1))
         ...
       </scopes>
    requires intRows(GRID)
      andBool notBool ("find_neighbor" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
    [priority(35)]

  rule <k> Call(
          Name("build_path"),
          (Name("k"), Name("neighbor"), .Exprs))
        => #alloc(list(alternatingSeq(0, K, NEIGHBOR))) ... </k>
       <env> L:Int </env>
       <scopes>
         ... L |-> scope(
           "grid" |-> _GRID:Val
           "k" |-> K:Int
           "one_row" |-> _ONE_ROW:Val
           "one_col" |-> _ONE_COL:Val
           "neighbor" |-> NEIGHBOR:Int,
           parent(0))
         0 |-> scope(
           "build_path" |->
             closureVal(
               ("k", "neighbor", .ParamNames),
               BUILD-PATH-FUNCTION-BODY,
               0)
           MODULE:Map,
           parent(-1))
         ...
       </scopes>
    requires K >Int 0
      andBool notBool ("build_path" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
    [priority(35)]

  syntax Val ::= lastValOr(ValSeq, Val) [function, total]
  rule lastValOr(.ValSeq, DEFAULT) => DEFAULT
  rule lastValOr(vCons(V:Val, VS), _) => lastValOr(VS, V)

  syntax Int ::= scanOneCol(ValSeq, Int, Int) [function, total]
  rule scanOneCol(.ValSeq, _, ANSWER) => ANSWER
  rule scanOneCol(vCons(V:Val, VS), COL, _)
    => scanOneCol(VS, COL +Int 1, COL)
    requires isInt(V) andBool {V}:>Int ==Int 1
    [simplification]
  rule scanOneCol(vCons(V:Val, VS), COL, ANSWER)
    => scanOneCol(VS, COL +Int 1, ANSWER)
    requires isInt(V) andBool {V}:>Int =/=Int 1
    [simplification]
  rule scanOneCol(vCons(V:Val, VS), COL, ANSWER)
    => scanOneCol(VS, COL +Int 1, ANSWER)
    requires notBool isInt(V)
    [simplification]

  rule (A:Int +Int 1) +Int B:Int => A +Int (B +Int 1)
    [simplification]

  syntax Int ::= gridDistance(Int, Int, Int, Int)
    [function, total]
  rule gridDistance(ROW, COL, ONE_ROW, ONE_COL)
    => absInt(ROW -Int ONE_ROW) +Int absInt(COL -Int ONE_COL)

  syntax Int ::= scanNeighbor(
    ValSeq, Int, Int, Int, Int, Int) [function, total]
  rule scanNeighbor(
         .ValSeq, _, _, _, _, NEIGHBOR)
    => NEIGHBOR
  rule scanNeighbor(
         vCons(V:Val, VS), COL, ROW, ONE_ROW, ONE_COL, NEIGHBOR)
    => scanNeighbor(
         VS, COL +Int 1, ROW, ONE_ROW, ONE_COL,
         minInt(NEIGHBOR, {V}:>Int))
    requires isInt(V)
      andBool gridDistance(ROW, COL, ONE_ROW, ONE_COL) ==Int 1
    [simplification]
  rule scanNeighbor(
         vCons(V:Val, VS), COL, ROW, ONE_ROW, ONE_COL, NEIGHBOR)
    => scanNeighbor(
         VS, COL +Int 1, ROW, ONE_ROW, ONE_COL, NEIGHBOR)
    requires isInt(V)
      andBool gridDistance(ROW, COL, ONE_ROW, ONE_COL) =/=Int 1
    [simplification]
  rule scanNeighbor(
         vCons(V:Val, VS), COL, ROW, ONE_ROW, ONE_COL, NEIGHBOR)
    => scanNeighbor(
         VS, COL +Int 1, ROW, ONE_ROW, ONE_COL, NEIGHBOR)
    requires notBool isInt(V)
    [simplification]

  syntax Int ::= foundCol(Val) [function, total]
  rule foundCol(V)
    => scanOneCol(rowContents(V), 0, -1)

  syntax Int ::= locateRow(ValSeq, Int, Int) [function, total]
  rule locateRow(.ValSeq, _, ONE_ROW) => ONE_ROW
  rule locateRow(vCons(V, VS), ROW_INDEX, _)
    => locateRow(VS, ROW_INDEX +Int 1, ROW_INDEX)
    requires foundCol(V) >=Int 0
    [simplification]
  rule locateRow(vCons(V, VS), ROW_INDEX, ONE_ROW)
    => locateRow(VS, ROW_INDEX +Int 1, ONE_ROW)
    requires foundCol(V) <Int 0
    [simplification]

  syntax Int ::= locateCol(ValSeq, Int) [function, total]
  rule locateCol(.ValSeq, ONE_COL) => ONE_COL
  rule locateCol(vCons(V, VS), _)
    => locateCol(VS, foundCol(V))
    requires foundCol(V) >=Int 0
    [simplification]
  rule locateCol(vCons(V, VS), ONE_COL)
    => locateCol(VS, ONE_COL)
    requires foundCol(V) <Int 0
    [simplification]

  syntax Int ::= lastFoundCol(ValSeq, Int) [function, total]
  rule lastFoundCol(.ValSeq, DEFAULT) => DEFAULT
  rule lastFoundCol(vCons(V, VS), _)
    => lastFoundCol(VS, foundCol(V))

  syntax Int ::= scanGridNeighbor(
    ValSeq, Int, Int, Int, Int) [function, total]
  rule scanGridNeighbor(
         .ValSeq, _, _, _, NEIGHBOR)
    => NEIGHBOR
  rule scanGridNeighbor(
         vCons(V, VS), ROW_INDEX, ONE_ROW, ONE_COL, NEIGHBOR)
    => scanGridNeighbor(
         VS,
         ROW_INDEX +Int 1,
         ONE_ROW,
         ONE_COL,
         scanNeighbor(
           rowContents(V),
           0,
           ROW_INDEX,
           ONE_ROW,
           ONE_COL,
           NEIGHBOR))
    [simplification]

  syntax ValSeq ::= flattenRows(ValSeq) [function, total]
  rule flattenRows(.ValSeq) => .ValSeq
  rule flattenRows(vCons(V, VS))
    => valSeqConcat(rowContents(V), flattenRows(VS))

  syntax Bool ::= squareRows(ValSeq, Int) [function, total]
  rule squareRows(.ValSeq, _) => true
  rule squareRows(vCons(V, VS), N)
    => (vsLen(rowContents(V)) ==Int N)
       andBool squareRows(VS, N)

  syntax Bool ::= cellsInRange(ValSeq, Int) [function, total]
  rule cellsInRange(.ValSeq, _) => true
  rule cellsInRange(vCons(V:Val, VS), LIMIT)
    => (1 <=Int {V}:>Int
        andBool {V}:>Int <=Int LIMIT)
       andBool cellsInRange(VS, LIMIT)
    requires isInt(V)
  rule cellsInRange(vCons(V:Val, _), _)
    => false
    requires notBool isInt(V)

  syntax Bool ::= valMember(Val, ValSeq) [function, total]
  rule valMember(_, .ValSeq) => false
  rule valMember(V, vCons(W, VS))
    => (V ==K W) orBool valMember(V, VS)

  syntax Bool ::= distinctVals(ValSeq) [function, total]
  rule distinctVals(.ValSeq) => true
  rule distinctVals(vCons(V, VS))
    => notBool valMember(V, VS) andBool distinctVals(VS)

  syntax Bool ::= validGrid(ValSeq) [function, total]
  rule validGrid(GRID)
    => (vsLen(GRID) >=Int 2)
       andBool intRows(GRID)
       andBool squareRows(GRID, vsLen(GRID))
       andBool cellsInRange(
         flattenRows(GRID),
         vsLen(GRID) *Int vsLen(GRID))
       andBool distinctVals(flattenRows(GRID))

  syntax Int ::= alternatingValue(Int, Int) [function, total]
  rule alternatingValue(I, _) => 1
    requires pyMod(I, 2) ==Int 0
  rule alternatingValue(I, NEIGHBOR) => NEIGHBOR
    requires pyMod(I, 2) =/=Int 0

  syntax ValSeq ::= alternatingSeq(Int, Int, Int) [function, total]
  rule alternatingSeq(I, K, _) => .ValSeq
    requires I >=Int K
  rule alternatingSeq(I, K, NEIGHBOR)
    => vCons(alternatingValue(I, NEIGHBOR),
             alternatingSeq(I +Int 1, K, NEIGHBOR))
    requires I <Int K

  rule valSeqConcat(valSeqConcat(A:ValSeq, B:ValSeq), C:ValSeq)
    => valSeqConcat(A, valSeqConcat(B, C))
    [simplification]

endmodule
