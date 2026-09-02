requires "mutation.k"

module SPEC-BODY-MUTATION
  imports MUTATION

  claim [body-must-matter]:
    <k> Call(Name("get_row"),
             (list(vCons(list(vCons(5, .ValSeq)), .ValSeq)),
              5,
              .Exprs))
        => ref(2) </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(
        "_column_desc" |-> COLUMNCLOSURE
        "_row_asc" |-> ROWCLOSURE
        "get_row" |-> closureVal(("lst", "x", .ParamNames),
                                  GETROWBODYMUTANT,
                                  0),
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(
                      tuple(vCons(0, vCons(0, .ValSeq))),
                      .ValSeq))
         1 |-> list(sortKeyVS(
                      vCons(tuple(vCons(0, vCons(0, .ValSeq))),
                            .ValSeq),
                      COLUMNCLOSURE))
         2 |-> list(sortKeyVS(
                      sortKeyVS(
                        vCons(tuple(vCons(0, vCons(0, .ValSeq))),
                              .ValSeq),
                        COLUMNCLOSURE),
                      ROWCLOSURE))
    </heap>
    <heapLoc> 0 => 3 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
