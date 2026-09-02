requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [filter-loop]:
    <k>
      #loop(list(REST:ValSeq), Name("value"), filterLoopBody)
      ~> (Return(Name("result")) .Stmts)
      ~> #endcall
      => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(("values", .ParamNames), filterBody, 0),
        parent(-1))
      1 |-> scope(
        "values" |-> list(ORIGINAL:ValSeq)
        "result" |-> ref(0)
        "value" |-> OLD:Val,
        parent(0))
      =>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(("values", .ParamNames), filterBody, 0),
        parent(-1))
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap>
      0 |-> list(ACC:ValSeq)
      =>
      0 |-> list(filterAcc(REST, ACC))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack>
      ListItem(frame(.K, 0, 1))
      =>
      .List
    </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>

  claim [filter-entry]:
    <k>
      Call(
        Name("filter_integers"),
        (list(INPUT:ValSeq), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(("values", .ParamNames), filterBody, 0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(filterAcc(INPUT, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
