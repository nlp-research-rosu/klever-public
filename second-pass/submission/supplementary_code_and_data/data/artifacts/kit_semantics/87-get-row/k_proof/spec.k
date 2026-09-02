requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [inner-loop]:
    <k> #loop(list(VS:ValSeq), Name("value"), INNERBODY)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "coordinates" |-> ref(OUT:Int)
        "column_index" |-> (CI:Int => advanceIndex(CI, VS))
        "lst" |-> LST:Val
        "row" |-> ROW:Val
        "row_index" |-> RI:Int
        "value" |-> (_OLD:Val => ?LAST:Val)
        "x" |-> X:Int,
        parent(0))
    </scopes>
    <heap>
      OUT |-> list(ACC:ValSeq
                    => scanAppend(ACC, VS, X, RI, CI))
      H:Map
    </heap>

  claim [outer-loop]:
    <k> #loop(list(RS:ValSeq), Name("row"), OUTERBODY)
        => .K ... </k>
    <env> L:Int </env>
    <scopes>
      SC:Map
      L |-> scope(
        "column_index" |-> (_CI:Int => ?FINALCI:Int)
        "coordinates" |-> ref(OUT:Int)
        "lst" |-> LST:Val
        "row" |-> (_OLDROW:Val => ?FINALROW:Val)
        "row_index" |-> (RI:Int => advanceIndex(RI, RS))
        "value" |-> (_OLDVALUE:Val => ?FINALVALUE:Val)
        "x" |-> X:Int,
        parent(0))
    </scopes>
    <heap>
      OUT |-> list(ACC:ValSeq
                    => rowsAppend(
                         ACC,
                         RS,
                         X,
                         RI))
      H:Map
    </heap>
    requires listRows(RS)

  claim [column-key]:
    <k> Call(Name("_column_desc"),
             (tuple(vCons(RI:Int, vCons(CI:Int, .ValSeq))), .Exprs))
        => 0 -Int CI </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("_column_desc" |-> COLUMNCLOSURE
                  "_row_asc" |-> ROWCLOSURE,
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

  claim [row-key]:
    <k> Call(Name("_row_asc"),
             (tuple(vCons(RI:Int, vCons(CI:Int, .ValSeq))), .Exprs))
        => RI </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope("_column_desc" |-> COLUMNCLOSURE
                  "_row_asc" |-> ROWCLOSURE,
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

  claim [get-row]:
    <k> Call(Name("get_row"), (list(RS:ValSeq), X:Int, .Exprs))
        => ref(2) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_column_desc" |-> COLUMNCLOSURE
        "_row_asc" |-> ROWCLOSURE
        "get_row" |-> closureVal(("lst", "x", .ParamNames),
                                  GETROWBODY,
                                  0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(rowsAppend(.ValSeq, RS, X, 0))
         1 |-> list(sortKeyVS(
                      rowsAppend(.ValSeq, RS, X, 0),
                      COLUMNCLOSURE))
         2 |-> list(sortKeyVS(
                      sortKeyVS(
                        rowsAppend(.ValSeq, RS, X, 0),
                        COLUMNCLOSURE),
                      ROWCLOSURE))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires listRows(RS)
endmodule
