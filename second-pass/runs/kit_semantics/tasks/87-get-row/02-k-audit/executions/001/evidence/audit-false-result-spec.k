requires "verification.k"

module AUDIT-FALSE-RESULT-SPEC
  imports VERIFICATION

  // Fresh reviewer mutation. For [[5,5]], x=5, ref(0) contains scan order
  // [(0,0),(0,1)], while the submitted function returns ref(2), whose value
  // is column-descending [(0,1),(0,0)] under the supplied sort contract.
  claim [wrong-returned-list]:
    <k> Call(
          Name("get_row"),
          (list(vCons(list(vCons(5, vCons(5, .ValSeq))), .ValSeq)),
           5,
           .Exprs))
        => ref(0) </k>
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
      => 0 |-> list(rowsAppend(
                      .ValSeq,
                      vCons(list(vCons(5, vCons(5, .ValSeq))), .ValSeq),
                      5,
                      0))
         1 |-> list(sortKeyVS(
                      rowsAppend(
                        .ValSeq,
                        vCons(list(vCons(5, vCons(5, .ValSeq))), .ValSeq),
                        5,
                        0),
                      COLUMNCLOSURE))
         2 |-> list(sortKeyVS(
                      sortKeyVS(
                        rowsAppend(
                          .ValSeq,
                          vCons(list(vCons(5, vCons(5, .ValSeq))), .ValSeq),
                          5,
                          0),
                        COLUMNCLOSURE),
                      ROWCLOSURE))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
