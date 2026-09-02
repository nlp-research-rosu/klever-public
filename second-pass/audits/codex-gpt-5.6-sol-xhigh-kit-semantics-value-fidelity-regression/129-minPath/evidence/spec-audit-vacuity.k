requires "verification.k"

module SPEC-AUDIT-VACUITY
  imports VERIFICATION

  claim [find-one-loop]:
    <k> #loop(list(VS:ValSeq),
              Name("value"),
              FIND-ONE-BODY)
      => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "row" |-> list(ORIGINAL:ValSeq)
        "col_index" |-> (COL:Int => COL +Int vsLen(VS))
        "value" |-> (OLD_VALUE:Val => lastValOr(VS, OLD_VALUE))
        "answer" |-> (ANSWER:Int => scanOneCol(VS, COL, ANSWER)),
        parent(0))
      ...
    </scopes>
    requires intsOnly(VS) andBool intsOnly(ORIGINAL)

  claim [locate-one-loop]:
    <k> #loop(list(GS:ValSeq),
              Name("row"),
              LOCATE-ONE-BODY)
      => .K ... </k>
    <env> L:Int </env>
    <scopeLoc> NEWL:Int </scopeLoc>
    <scopes>
      L |-> scope(
        "grid" |-> list(ORIGINAL_GRID:ValSeq)
        "row_index" |->
          (ROW_INDEX:Int => ROW_INDEX +Int vsLen(GS))
        "row" |-> (OLD_ROW:Val => lastValOr(GS, OLD_ROW))
        "one_row" |->
          (ONE_ROW:Int => locateRow(GS, ROW_INDEX, ONE_ROW))
        "one_col" |-> (ONE_COL:Int => locateCol(GS, ONE_COL))
        "found_col" |->
          (OLD_FOUND:Int => lastFoundCol(GS, OLD_FOUND)),
        parent(0))
      0 |-> scope(
        "find_one" |->
          closureVal(("row", .ParamNames),
                     FIND-ONE-FUNCTION-BODY,
                     0)
        MODULE:Map,
        parent(-1))
      -1 |-> builtinsScope
      OTHER:Map
    </scopes>
    requires intRows(GS) andBool intRows(ORIGINAL_GRID)
      andBool notBool ("find_one" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))
      andBool L =/=Int 0 andBool L =/=Int -1
      andBool notBool (L in_keys(OTHER))
      andBool notBool (0 in_keys(OTHER))
      andBool notBool (-1 in_keys(OTHER))
      andBool NEWL =/=Int L
      andBool NEWL =/=Int 0
      andBool NEWL =/=Int -1
      andBool notBool (NEWL in_keys(OTHER))

  claim [scan-row-loop]:
    <k> #loop(list(VS:ValSeq),
              Name("value"),
              SCAN-ROW-BODY)
      => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "row" |-> list(ORIGINAL:ValSeq)
        "row_index" |-> ROW_INDEX:Int
        "one_row" |-> ONE_ROW:Int
        "one_col" |-> ONE_COL:Int
        "neighbor" |->
          (NEIGHBOR:Int =>
           scanNeighbor(
             VS, COL, ROW_INDEX, ONE_ROW, ONE_COL, NEIGHBOR))
        "col_index" |-> (COL:Int => COL +Int vsLen(VS))
        "value" |-> (OLD_VALUE:Val => lastValOr(VS, OLD_VALUE)),
        parent(0))
      0 |-> scope(MODULE:Map, parent(-1))
      -1 |-> builtinsScope
      ...
    </scopes>
    requires intsOnly(VS) andBool intsOnly(ORIGINAL)
      andBool notBool ("abs" in_keys(MODULE))
      andBool notBool ("min" in_keys(MODULE))

  claim [find-neighbor-loop]:
    <k> #loop(list(GS:ValSeq),
              Name("row"),
              FIND-NEIGHBOR-BODY)
      => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "grid" |-> list(ORIGINAL_GRID:ValSeq)
        "one_row" |-> ONE_ROW:Int
        "one_col" |-> ONE_COL:Int
        "n" |-> N:Int
        "neighbor" |->
          (NEIGHBOR:Int =>
           scanGridNeighbor(
             GS, ROW_INDEX, ONE_ROW, ONE_COL, NEIGHBOR))
        "row_index" |->
          (ROW_INDEX:Int => ROW_INDEX +Int vsLen(GS))
        "row" |-> (OLD_ROW:Val => lastValOr(GS, OLD_ROW)),
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
    requires intRows(GS) andBool intRows(ORIGINAL_GRID)
      andBool notBool ("scan_row" in_keys(MODULE))
      andBool notBool ("$cells" in_keys(MODULE))

  claim [result-loop]:
    <k> #loop(rangeObj(I:Int, K:Int, 1), Name("step"), RESULT-BODY)
      => .K ... </k>
    <env> L:Int </env>
    <scopes>
      ... L |-> scope(
        "k" |-> K
        "result" |-> ref(H:Int)
        "neighbor" |-> NEIGHBOR:Int
        "step" |-> (_:Int => K -Int 1),
        parent(0))
      ...
    </scopes>
    <heap>
      ... H |-> (list(VS:ValSeq)
              => list(valSeqConcat(VS, alternatingSeq(I, K, NEIGHBOR))))
      ...
    </heap>
    requires 0 <=Int I andBool I <Int K

  claim [minpath-entry]:
    <k> #applyK(
          toCall(
            closureVal(
              ("grid", "k", .ParamNames),
              MINPATH-FUNCTION-BODY,
              0)),
          (list(GRID:ValSeq), K:Int, .Vals))
      => ref(0) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "find_one" |->
          closureVal(
            ("row", .ParamNames),
            FIND-ONE-FUNCTION-BODY,
            0)
        "locate_one" |->
          closureVal(
            ("grid", .ParamNames),
            LOCATE-ONE-FUNCTION-BODY,
            0)
        "scan_row" |->
          closureVal(
            ("row", "row_index", "one_row", "one_col", "neighbor",
             .ParamNames),
            SCAN-ROW-FUNCTION-BODY,
            0)
        "find_neighbor" |->
          closureVal(
            ("grid", "one_row", "one_col", .ParamNames),
            FIND-NEIGHBOR-FUNCTION-BODY,
            0)
        "build_path" |->
          closureVal(
            ("k", "neighbor", .ParamNames),
            BUILD-PATH-FUNCTION-BODY,
            0)
        "minPath" |->
          closureVal(
            ("grid", "k", .ParamNames),
            MINPATH-FUNCTION-BODY,
            0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map =>
      0 |-> list(
        vCons(0, alternatingSeq(
          0,
          K,
          scanGridNeighbor(
            GRID,
            0,
            locateRow(GRID, 0, 0),
            locateCol(GRID, 0),
            vsLen(GRID) *Int vsLen(GRID)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    requires validGrid(GRID) andBool intRows(GRID)
      andBool K >Int 0
endmodule
