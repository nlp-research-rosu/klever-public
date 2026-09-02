requires "verification.k"

module SPEC-AUDITOR-BODY-SENSITIVITY
  imports VERIFICATION

  // The executed closure really changes: the For statement is removed.
  claim [removed-loop-body]:
    <k>
      Call(
        Name("filter_integers"),
        (list(vCons(1, .ValSeq)), .Exprs))
      =>
      ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope(
        "filter_integers" |->
          closureVal(
            ("values", .ParamNames),
            (Expr(
               Str("Filter a list to the values that are instances of ``int``."))
             Assign(Name("result"), ListExpr(.Exprs))
             Return(Name("result"))
             .Stmts),
            0),
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(1, .ValSeq))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
