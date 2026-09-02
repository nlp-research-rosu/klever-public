requires "verification.k"

module SPEC-VACUITY
  imports VERIFICATION

  claim [wrong-return]:
    <k> Call(Name("get_row"), (list(.ValSeq), 1, .Exprs))
        => ref(99) </k>
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
    <heap> .Map </heap>
    <heapLoc> 0 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
